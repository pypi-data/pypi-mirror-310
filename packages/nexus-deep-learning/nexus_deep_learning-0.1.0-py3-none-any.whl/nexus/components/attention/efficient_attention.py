import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Optional, Tuple

class FlashAttention(nn.Module):
    def __init__(
        self,
        hidden_size: int,
        num_heads: int,
        batch_size: int,
        block_size: int = 1024
    ):
        super().__init__()
        self.hidden_size = hidden_size
        self.num_heads = num_heads
        self.head_dim = hidden_size // num_heads
        self.block_size = block_size
        
        self.q_proj = nn.Linear(hidden_size, hidden_size)
        self.k_proj = nn.Linear(hidden_size, hidden_size)
        self.v_proj = nn.Linear(hidden_size, hidden_size)
        self.out_proj = nn.Linear(hidden_size, hidden_size)
        
    def forward(
        self,
        hidden_states: torch.Tensor,
        attention_mask: Optional[torch.Tensor] = None
    ) -> torch.Tensor:
        B, L, _ = hidden_states.size()
        
        # Project queries, keys, and values
        q = self.q_proj(hidden_states)
        k = self.k_proj(hidden_states)
        v = self.v_proj(hidden_states)
        
        # Reshape for multi-head attention
        q = q.view(B, L, self.num_heads, self.head_dim)
        k = k.view(B, L, self.num_heads, self.head_dim)
        v = v.view(B, L, self.num_heads, self.head_dim)
        
        # Compute attention scores in blocks
        output = torch.zeros_like(q)
        
        for block_start in range(0, L, self.block_size):
            block_end = min(block_start + self.block_size, L)
            
            # Load block of queries
            q_block = q[:, block_start:block_end]
            
            # Compute attention scores for this block
            scores = torch.matmul(q_block, k.transpose(-2, -1)) / torch.sqrt(
                torch.tensor(self.head_dim, dtype=torch.float32, device=q.device)
            )
            
            if attention_mask is not None:
                scores = scores.masked_fill(
                    attention_mask[:, block_start:block_end].unsqueeze(1).unsqueeze(2) == 0,
                    float("-inf")
                )
            
            # Apply softmax and compute weighted sum
            attn_probs = F.softmax(scores, dim=-1)
            output[:, block_start:block_end] = torch.matmul(attn_probs, v)
        
        # Reshape and project output
        output = output.reshape(B, L, self.hidden_size)
        return self.out_proj(output) 

class MemoryEfficientAttention(nn.Module):
    def __init__(
        self,
        hidden_size: int,
        num_heads: int,
        dropout: float = 0.1,
        chunk_size: int = 128
    ):
        super().__init__()
        self.hidden_size = hidden_size
        self.num_heads = num_heads
        self.head_dim = hidden_size // num_heads
        self.chunk_size = chunk_size
        self.scale = self.head_dim ** -0.5
        
        self.to_qkv = nn.Linear(hidden_size, hidden_size * 3)
        self.to_out = nn.Sequential(
            nn.Linear(hidden_size, hidden_size),
            nn.Dropout(dropout)
        )
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        batch_size, seq_len, _ = x.shape
        qkv = self.to_qkv(x).chunk(3, dim=-1)
        q, k, v = map(
            lambda t: t.view(batch_size, seq_len, self.num_heads, self.head_dim).transpose(1, 2),
            qkv
        )
        
        # Chunked attention computation
        out = torch.zeros_like(q)
        for i in range(0, seq_len, self.chunk_size):
            chunk_q = q[:, :, i:i+self.chunk_size]
            attn_weights = torch.matmul(chunk_q, k.transpose(-2, -1)) * self.scale
            attn_weights = F.softmax(attn_weights, dim=-1)
            out[:, :, i:i+self.chunk_size] = torch.matmul(attn_weights, v)
            
        out = out.transpose(1, 2).reshape(batch_size, seq_len, self.hidden_size)
        return self.to_out(out) 
