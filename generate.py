# generate.py
import os, sys
import numpy as np
from tinygrad import Tensor, nn
import safetensors.numpy
from tokenizers import Tokenizer
from tiny_model import GPT, GPTConfig

if __name__ == "__main__":
    # Force UTF-8 encoding for stdout on Windows to prevent UnicodeEncodeError
    if sys.platform.startswith("win"):
        sys.stdout.reconfigure(encoding="utf-8")
        
    device = os.environ.get("DEV", "CL")
    
    # 1. Load the real BPE tokenizer
    tokenizer_path = "tokenizer.json"
    if not os.path.exists(tokenizer_path):
        raise FileNotFoundError(f"Could not find {tokenizer_path}")
    tokenizer = Tokenizer.from_file(tokenizer_path)
    vocab_size = tokenizer.get_vocab_size()
    print(f"Loaded BPE Tokenizer with vocab size: {vocab_size}")

    # 2. Setup configuration matching the trained model hyperparameters
    config = GPTConfig(
        vocab_size=vocab_size,
        block_size=256,
        n_layer=6,
        n_head=6,
        n_embd=384
    )
    model = GPT(config)
    
    # 3. Load checkpoint weights
    ckpt_path = "checkpoint.safetensors"
    if not os.path.exists(ckpt_path):
        raise FileNotFoundError(f"Could not find {ckpt_path}. Please train the model first.")
        
    print(f"Loading weights from {ckpt_path}...")
    ckpt = safetensors.numpy.load_file(ckpt_path)
    state = nn.state.get_state_dict(model)
    for k, v in state.items():
        if k in ckpt:
            v.assign(Tensor(ckpt[k], device=device))
            
    # 4. Generate text from a prompt
    prompt = "Once upon a time"
    print(f"\nPrompt: '{prompt}'")
    
    # Encode prompt to tokens
    prompt_ids = tokenizer.encode(prompt).ids
    context = Tensor([prompt_ids], device=device)
    
    # Generate tokens
    print("Generating...")
    # Generate 100 new tokens
    output = model.generate(context, max_new_tokens=100, temperature=0.8, top_k=50)
    
    # Decode and print output
    out_ids = output.numpy().flatten().tolist()
    generated_text = tokenizer.decode(out_ids)
    
    # Clean up BPE control characters for human-readable output
    clean_text = generated_text.replace("Ġ", " ").replace("Ċ", "\n").replace("ĉ", "\n")
    
    print("\nGenerated Output:")
    print("-" * 50)
    print(clean_text)
    print("-" * 50)
