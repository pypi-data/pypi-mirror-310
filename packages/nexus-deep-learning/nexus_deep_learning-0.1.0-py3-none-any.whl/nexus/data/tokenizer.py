from typing import List, Dict, Optional, Union
import re
from collections import Counter
from abc import ABC, abstractmethod
import torch

class BaseTokenizer(ABC):
    def __init__(
        self,
        vocab_size: int,
        special_tokens: Optional[List[str]] = None
    ):
        self.vocab_size = vocab_size
        self.special_tokens = special_tokens or ["[PAD]", "[UNK]", "[CLS]", "[SEP]"]
        self.word2idx = {token: idx for idx, token in enumerate(self.special_tokens)}
        self.idx2word = {idx: token for token, idx in self.word2idx.items()}
        
    @abstractmethod
    def fit(self, texts: List[str]) -> None:
        pass
        
    @abstractmethod
    def encode(self, text: str, max_length: Optional[int] = None) -> Union[List[int], torch.Tensor]:
        pass
        
    @abstractmethod
    def decode(self, ids: Union[List[int], torch.Tensor]) -> str:
        pass
        
    def _add_to_vocab(self, token: str) -> int:
        if token not in self.word2idx and len(self.word2idx) < self.vocab_size:
            idx = len(self.word2idx)
            self.word2idx[token] = idx
            self.idx2word[idx] = token
        return self.word2idx.get(token, self.word2idx['[UNK]'])

class SimpleTokenizer(BaseTokenizer):
    def __init__(
        self,
        vocab_size: int = 10000,
        min_freq: int = 2,
        special_tokens: Optional[List[str]] = None
    ):
        super().__init__(vocab_size, special_tokens)
        self.min_freq = min_freq
        
    def _tokenize(self, text: str) -> List[str]:
        text = re.sub(r'([.,!?])', r' \1 ', text)
        return text.lower().split()
        
    def fit(self, texts: List[str]) -> None:
        words = []
        for text in texts:
            words.extend(self._tokenize(text))
            
        word_counts = Counter(words)
        valid_words = [
            word for word, count in word_counts.most_common()
            if count >= self.min_freq and word not in self.word2idx
        ]
        
        for word in valid_words[:self.vocab_size - len(self.word2idx)]:
            self._add_to_vocab(word)
            
    def encode(self, text: str, max_length: Optional[int] = None) -> List[int]:
        tokens = self._tokenize(text)
        if max_length is not None:
            tokens = tokens[:max_length-2]
            
        ids = [self.word2idx.get(token, self.word2idx['[UNK]']) for token in tokens]
        ids = [self.word2idx['[CLS]']] + ids + [self.word2idx['[SEP]']]
        
        if max_length is not None:
            padding_length = max_length - len(ids)
            if padding_length > 0:
                ids.extend([self.word2idx['[PAD]']] * padding_length)
                
        return ids
        
    def decode(self, ids: List[int]) -> str:
        tokens = [self.idx2word.get(idx, '[UNK]') for idx in ids]
        tokens = [t for t in tokens if t not in self.special_tokens]
        return ' '.join(tokens)

class BERTTokenizer(BaseTokenizer):
    def __init__(
        self,
        vocab_size: int = 30000,
        special_tokens: Optional[List[str]] = None,
        wordpiece_vocab: Optional[Dict[str, int]] = None
    ):
        super().__init__(vocab_size, special_tokens)
        self.wordpiece_vocab = wordpiece_vocab or {}
        self.max_wordpiece_length = 100
        
    def _tokenize(self, text: str) -> List[str]:
        words = text.lower().split()
        tokens = []
        for word in words:
            if word in self.wordpiece_vocab:
                tokens.append(word)
            else:
                # WordPiece tokenization
                pieces = []
                while word:
                    i = len(word)
                    while i > 0 and word[:i] not in self.wordpiece_vocab:
                        i -= 1
                    if i == 0:
                        pieces.append('[UNK]')
                        break
                    pieces.append(word[:i])
                    word = word[i:]
                    if word:
                        word = '##' + word
                tokens.extend(pieces)
        return tokens
        
    def fit(self, texts: List[str]) -> None:
        # Build WordPiece vocabulary
        words = []
        for text in texts:
            words.extend(text.lower().split())
            
        # Add common words and subwords to vocabulary
        word_counts = Counter(words)
        for word, count in word_counts.most_common(self.vocab_size - len(self.special_tokens)):
            self._add_to_vocab(word)
            
    def encode(self, text: str, max_length: Optional[int] = None) -> torch.Tensor:
        tokens = self._tokenize(text)
        if max_length is not None:
            tokens = tokens[:max_length-2]
            
        ids = [self.word2idx.get(token, self.word2idx['[UNK]']) for token in tokens]
        ids = [self.word2idx['[CLS]']] + ids + [self.word2idx['[SEP]']]
        
        if max_length is not None:
            padding_length = max_length - len(ids)
            if padding_length > 0:
                ids.extend([self.word2idx['[PAD]']] * padding_length)
                
        return torch.tensor(ids)
        
    def decode(self, ids: Union[List[int], torch.Tensor]) -> str:
        if isinstance(ids, torch.Tensor):
            ids = ids.tolist()
        tokens = [self.idx2word.get(idx, '[UNK]') for idx in ids]
        tokens = [t for t in tokens if t not in self.special_tokens]
        return ' '.join(tokens).replace(' ##', '')