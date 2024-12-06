from typing import Dict, List, Optional, Union
import torch
from nexus.data import Dataset
from nexus.data.tokenizer import BERTTokenizer

class BERTDataset(Dataset):
    def __init__(
        self,
        texts: List[str],
        tokenizer: BERTTokenizer,
        labels: Optional[List[int]] = None,
        max_length: int = 512,
        return_tensors: bool = True
    ):
        """
        Initialize BERT dataset.
        
        Args:
            texts: List of input texts
            tokenizer: Nexus BERTTokenizer instance
            labels: Optional list of labels for classification
            max_length: Maximum sequence length
            return_tensors: Whether to return PyTorch tensors
        """
        if not texts:
            raise ValueError("texts cannot be empty")
        if not isinstance(tokenizer, BERTTokenizer):
            raise TypeError("tokenizer must be an instance of BERTTokenizer")
            
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.return_tensors = return_tensors
        
        if self.labels is not None and len(self.texts) != len(self.labels):
            raise ValueError("Number of texts and labels must match")
            
    def __len__(self) -> int:
        return len(self.texts)
        
    def __getitem__(self, idx: int) -> Dict[str, Union[torch.Tensor, int]]:
        text = self.texts[idx]
        
        # Tokenize text
        encoding = self.tokenizer(
            text,
            max_length=self.max_length,
            padding='max_length',
            truncation=True,
            return_tensors='pt' if self.return_tensors else None
        )
        
        # Create item dictionary
        item = {
            'input_ids': encoding['input_ids'].squeeze(0) if self.return_tensors else encoding['input_ids'],
            'attention_mask': encoding['attention_mask'].squeeze(0) if self.return_tensors else encoding['attention_mask']
        }
        
        # Add label if available
        if self.labels is not None:
            item['label'] = torch.tensor(self.labels[idx]) if self.return_tensors else self.labels[idx]
            
        return item 