# tiny_model.py -- Tinygrad GPT model
import math
from tinygrad import Tensor, nn
from tinygrad.nn import Linear, LayerNorm, Embedding

class GPTConfig:
    def __init__(self, vocab_size, block_size, n_layer, n_head, n_embd, dropout=0.0, bias=False):
        self.vocab_size = vocab_size
        self.block_size = block_size
        self.n_layer = n_layer
        self.n_head = n_head
        self.n_embd = n_embd
        self.dropout = dropout
        self.bias = bias

class CausalSelfAttention:
    def __init__(self, config: GPTConfig):
        assert config.n_embd % config.n_head == 0
        self.n_head = config.n_head
        self.n_embd = config.n_embd
        self.head_dim = config.n_embd // config.n_head
        self.c_attn = Linear(config.n_embd, 3 * config.n_embd, bias=config.bias)
        self.c_proj = Linear(config.n_embd, config.n_embd, bias=config.bias)
        # causal mask (upper triangular = -inf)
        mask = Tensor.ones(config.block_size, config.block_size).triu(1) * -1e9
        self.mask = mask.reshape(1, 1, config.block_size, config.block_size)

    def __call__(self, x: Tensor) -> Tensor:
        B, T, C = x.shape
        qkv = self.c_attn(x)                     # (B, T, 3*C)
        q, k, v = qkv.split(self.n_embd, dim=2)
        # reshape to (B, nh, T, hs)
        q = q.reshape(B, T, self.n_head, self.head_dim).transpose(1, 2)
        k = k.reshape(B, T, self.n_head, self.head_dim).transpose(1, 2)
        v = v.reshape(B, T, self.n_head, self.head_dim).transpose(1, 2)
        # scaled attention
        att = (q @ k.transpose(-2, -1)) * (1.0 / math.sqrt(self.head_dim))
        att = att + self.mask[:, :, :T, :T]
        att = att.softmax(-1)
        y = att @ v                               # (B, nh, T, hs)
        y = y.transpose(1, 2).reshape(B, T, C)
        return self.c_proj(y)

class MLP:
    def __init__(self, config: GPTConfig):
        self.c_fc   = Linear(config.n_embd, 4 * config.n_embd, bias=config.bias)
        self.c_proj = Linear(4 * config.n_embd, config.n_embd, bias=config.bias)

    def __call__(self, x: Tensor) -> Tensor:
        return self.c_proj(self.c_fc(x).gelu())   # apply gelu directly on tensor

class Block:
    def __init__(self, config: GPTConfig):
        self.ln_1 = LayerNorm(config.n_embd)
        self.attn = CausalSelfAttention(config)
        self.ln_2 = LayerNorm(config.n_embd)
        self.mlp  = MLP(config)

    def __call__(self, x: Tensor) -> Tensor:
        x = x + self.attn(self.ln_1(x))
        x = x + self.mlp(self.ln_2(x))
        return x

class GPT:
    def __init__(self, config: GPTConfig):
        self.config = config
        self.wte = Embedding(config.vocab_size, config.n_embd)
        self.wpe = Embedding(config.block_size, config.n_embd)
        self.blocks = [Block(config) for _ in range(config.n_layer)]
        self.ln_f = LayerNorm(config.n_embd)
        self.lm_head = Linear(config.n_embd, config.vocab_size, bias=False)
        # weight tying
        self.lm_head.weight = self.wte.weight

    def __call__(self, idx: Tensor) -> Tensor:
        B, T = idx.shape
        assert T <= self.config.block_size, f"Cannot forward sequence of length {T}, block size is only {self.config.block_size}"
        tok_emb = self.wte(idx)                   # (B, T, n_embd)
        pos = Tensor.arange(0, T).reshape(1, T).expand(B, T)
        pos_emb = self.wpe(pos)                   # (B, T, n_embd)
        x = tok_emb + pos_emb
        for block in self.blocks:
            x = block(x)
        x = self.ln_f(x)
        return self.lm_head(x)                    # (B, T, vocab_size)

    def generate(self, idx: Tensor, max_new_tokens: int, temperature=1.0, top_k=None) -> Tensor:
        for _ in range(max_new_tokens):
            idx_cond = idx[:, -self.config.block_size:]   # crop to block size
            logits = self(idx_cond)                       # (B, T, vocab_size)
            logits = logits[:, -1, :] / temperature       # only last token
            if top_k is not None:
                v, _ = logits.topk(top_k)
                logits = logits.where(logits >= v[:, -1:], -float('inf'))
            probs = logits.softmax(-1)
            idx_next = probs.multinomial(1)               # sample one token per batch
            idx = idx.cat(idx_next, dim=1).realize()
        return idx
