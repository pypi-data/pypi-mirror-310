from pathlib import Path
import json
import torch
from nexus.data import Dataset  
import numpy as np
from PIL import Image
from datasets import load_dataset
import torch.nn.functional as F
from torch.utils.data import DataLoader
import multiprocessing as mp
from typing import Dict, Optional, Tuple
import h5py
from nexus.utils import Logger

logger = Logger(__name__)



class NeRFDataset(Dataset):
    def __init__(self, 
                 root_dir, 
                 split='train', 
                 img_wh=(800, 800),
                 precache_rays=True,
                 num_workers=None):
        logger.info(f"Initializing NeRFDataset with root_dir={root_dir}, split={split}, img_wh={img_wh}")
        super().__init__(data_dir=root_dir)
        self.root_dir = Path(root_dir)
        self.split = split
        self.img_wh = img_wh
        self.precache_rays = precache_rays
        self.num_workers = num_workers or mp.cpu_count()
        logger.info(f"Using {self.num_workers} workers for processing")
        self.data = None
        self.ray_cache = {}
        
        # Set default device to MPS if available
        self.device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
        logger.info(f"Using device: {self.device}")
        
        # Download and prepare dataset
        self._prepare_dataset()
        
        # Precache rays if enabled
        if self.precache_rays:
            self._precache_ray_bundles()
        
    def _prepare_dataset(self):
        """Load NeRF synthetic dataset from local path or download if needed."""
        logger.info("Loading NeRF synthetic dataset...")
        
        # Check if data exists locally first
        data_dir = Path(self.root_dir)
        if data_dir.exists():
            try:
                # Load local data
                self.data = []
                transforms_file = data_dir / 'transforms.json'
                
                if not transforms_file.exists():
                    raise FileNotFoundError(f"transforms.json not found in {data_dir}")
                    
                with open(transforms_file, 'r') as f:
                    transform_data = json.load(f)
                    
                # Process each frame
                logger.info("Processing frames from transforms.json...")
                for i, frame in enumerate(transform_data['frames']):
                    if i % 10 == 0:  # Log progress every 10 frames
                        logger.info(f"Processing frame {i}/{len(transform_data['frames'])}")
                        
                    image_path = data_dir / f"{frame['file_path']}.png"
                    if not image_path.exists():
                        raise FileNotFoundError(f"Image not found: {image_path}")
                        
                    image = np.array(Image.open(image_path))
                    processed_item = {
                        'image': image,
                        'camera_to_world': np.array(frame['transform_matrix']),
                        'camera_intrinsics': np.array([
                            [self.img_wh[0], 0, self.img_wh[0]/2],
                            [0, self.img_wh[1], self.img_wh[1]/2],
                            [0, 0, 1]
                        ])
                    }
                    self.data.append(processed_item)
                    
                logger.info(f"Successfully loaded {len(self.data)} samples from local directory")
                
            except Exception as e:
                logger.error(f"Failed to load local dataset: {str(e)}")
                logger.info("Attempting to download from HuggingFace...")
                self._download_from_huggingface()
        else:
            logger.warning(f"Local directory {data_dir} not found.")
            logger.info("Attempting to download from HuggingFace...")
            self._download_from_huggingface()

    def _download_from_huggingface(self):
        """Download dataset from HuggingFace and save locally."""
        try:
            logger.info("Downloading dataset from HuggingFace...")
            dataset = load_dataset("phuckstnk63/nerf-synthetic", split=self.split)
            logger.info(f"Available fields: {dataset[0].keys()}")
            
            # Create target directory if it doesn't exist
            data_dir = Path(self.root_dir)
            data_dir.mkdir(parents=True, exist_ok=True)
            
            # Create transforms.json with default camera setup
            transforms_data = {"frames": []}
            
            # Process and save each image
            logger.info("Processing and saving images...")
            for idx, item in enumerate(dataset):
                if idx % 10 == 0:  # Log progress every 10 images
                    logger.info(f"Processing image {idx}/{len(dataset)}")
                    
                # Convert PIL image to numpy array if needed
                if isinstance(item['image'], Image.Image):
                    image = np.array(item['image'])
                else:
                    image = item['image']
                    
                # Save image
                image_filename = f"r_{idx}"
                image_path = data_dir / f"{image_filename}.png"
                Image.fromarray(image).save(image_path)
                
                # Create default camera transform
                default_transform = {
                    "file_path": image_filename,
                    "transform_matrix": [
                        [1, 0, 0, 0],
                        [0, 1, 0, 0],
                        [0, 0, 1, 2],  # Camera 2 units away from origin
                        [0, 0, 0, 1]
                    ]
                }
                transforms_data["frames"].append(default_transform)
            
            # Save transforms.json
            logger.info("Saving transforms.json...")
            with open(data_dir / "transforms.json", 'w') as f:
                json.dump(transforms_data, f, indent=2)
                
            logger.info(f"Successfully downloaded and saved {len(dataset)} samples to {data_dir}")
            
            # Now load the saved dataset
            self._prepare_dataset()
            
        except Exception as e:
            error_msg = (f"Failed to download and save dataset: {str(e)}. "
                        "Please check the dataset structure:\n"
                        f"Available fields: {dataset[0].keys() if 'dataset' in locals() else 'Unknown'}")
            logger.error(error_msg)
            raise RuntimeError(error_msg)

    def _precache_ray_bundles(self):
        """Pre-compute ray bundles using multiple processes"""
        logger.info("Starting ray bundle pre-computation...")
        logger.info(f"Processing {len(self.data)} samples with {self.num_workers} workers")
        
        with mp.Pool(self.num_workers) as pool:
            cache_items = pool.map(self._compute_ray_bundle_for_item, 
                                 range(len(self.data)))
        
        logger.info("Storing computed ray bundles in cache...")
        for idx, (origins, directions) in enumerate(cache_items):
            if idx % 10 == 0:  # Log progress every 10 items
                logger.info(f"Caching ray bundle {idx}/{len(self.data)}")
            # Move tensors to MPS device after multiprocessing
            self.ray_cache[idx] = {
                'origins': origins.to(self.device),
                'directions': directions.to(self.device)
            }
        
        logger.info("Ray bundle pre-computation complete")
        logger.info(f"Cache contains {len(self.ray_cache)} ray bundles")

    def _compute_ray_bundle_for_item(self, idx: int) -> Tuple[torch.Tensor, torch.Tensor]:
        """Compute ray bundle for a single item"""
        logger.debug(f"Computing ray bundle for item {idx}")
        sample = self.data[idx]
        
        # Ensure computations are done on CPU
        c2w = torch.tensor(sample['camera_to_world'], dtype=torch.float32)
        intrinsics = torch.tensor(sample['camera_intrinsics'], dtype=torch.float32)
        
        # Get ray bundle on CPU
        ray_origins, ray_directions = self._get_ray_bundle(c2w, intrinsics)
        
        # Ensure outputs are on CPU
        return ray_origins.cpu(), ray_directions.cpu()
        
    def _get_ray_bundle(self, c2w, intrinsics):
        """Generate ray bundle for a single image."""
        W, H = self.img_wh
        
        # Generate pixel coordinates on CPU
        i, j = torch.meshgrid(
            torch.linspace(0, W-1, W),
            torch.linspace(0, H-1, H),
            indexing='ij'
        )
        
        # Convert to normalized device coordinates
        x = (i - intrinsics[0, 2]) / intrinsics[0, 0]
        y = (j - intrinsics[1, 2]) / intrinsics[1, 1]
        
        # Create ray directions in camera space
        directions = torch.stack([x, -y, -torch.ones_like(x)], dim=-1)
        
        # Transform ray directions to world space
        ray_directions = torch.sum(directions[..., None, :] * c2w[:3, :3], dim=-1)
        ray_origins = c2w[:3, -1].expand(ray_directions.shape)
        
        return ray_origins, ray_directions

    @staticmethod
    def collate_fn(batch):
        """Custom collate function for batching data"""
        ray_origins = torch.stack([item['ray_origins'] for item in batch])
        ray_directions = torch.stack([item['ray_directions'] for item in batch])
        target_rgb = torch.stack([item['target_rgb'] for item in batch])
        
        return {
            'ray_origins': ray_origins,
            'ray_directions': ray_directions,
            'target_rgb': target_rgb
        }
        
    def __len__(self):
        return len(self.data)
        
    def __getitem__(self, idx):
        logger.debug(f"Getting item {idx}")
        sample = self.data[idx]
        
        # Load and process image on CPU first
        image = torch.tensor(sample['image'], dtype=torch.float32) / 255.0
        
        # Add batch dimension for interpolation if needed
        if len(image.shape) == 3:  # [H, W, C]
            image = image.permute(2, 0, 1).unsqueeze(0)  # [1, C, H, W]
        else:
            image = image.unsqueeze(0).unsqueeze(0)  # Add batch and channel dims
        
        # Interpolate on CPU
        image = F.interpolate(
            image,
            size=self.img_wh,
            mode='bilinear',
            align_corners=False
        )
        
        # Remove batch dimension and rearrange to [H, W, C]
        image = image.squeeze(0).permute(1, 2, 0)
        
        # Use cached ray bundles if available
        if self.precache_rays and idx in self.ray_cache:
            logger.debug(f"Using cached ray bundle for item {idx}")
            ray_origins = self.ray_cache[idx]['origins']
            ray_directions = self.ray_cache[idx]['directions']
        else:
            logger.debug(f"Computing ray bundle for item {idx}")
            c2w = torch.tensor(sample['camera_to_world'], dtype=torch.float32)
            intrinsics = torch.tensor(sample['camera_intrinsics'], dtype=torch.float32)
            ray_origins, ray_directions = self._get_ray_bundle(c2w, intrinsics)
        
        # Verify image dimensions before reshaping
        H, W, C = image.shape
        expected_size = H * W
        
        # Flatten rays and target RGB values
        ray_origins = ray_origins.reshape(-1, 3)
        ray_directions = ray_directions.reshape(-1, 3)
        target_rgb = image.reshape(expected_size, C)
        
        # Move to device only after all processing is done
        if self.device.type != 'cpu':
            ray_origins = ray_origins.to(self.device)
            ray_directions = ray_directions.to(self.device)
            target_rgb = target_rgb.to(self.device)
        
        return {
            "ray_origins": ray_origins,
            "ray_directions": ray_directions,
            "target_rgb": target_rgb
        }
