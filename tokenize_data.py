# tokenize_data.py
from tokenizers import Tokenizer
import numpy as np
import os

tokenizer_path = "tokenizer.json"
corpus_path = "corpus.txt"
block_size = 1024
output_train = "train.bin"
output_val = "val.bin"
val_split = 0.1   # 10% validation

tokenizer = Tokenizer.from_file(tokenizer_path)
pad_id = tokenizer.token_to_id("<|pad|>")

print("Tokenizing corpus (streaming)...")
# We'll read the corpus in chunks, encode, and write to a temporary binary file
temp_bin = "tokens_temp.bin"
with open(corpus_path, "r", encoding="utf-8", errors="ignore") as f_in, \
     open(temp_bin, "wb") as f_out:
    chunk_size = 1024 * 1024  # 1 MB text chunks
    while True:
        text_chunk = f_in.read(chunk_size)
        if not text_chunk:
            break
        ids = tokenizer.encode(text_chunk).ids
        if ids:
            f_out.write(np.array(ids, dtype=np.uint16).tobytes())

print("Encoding complete. Now splitting into blocks...")
# Load the entire token array (might be 50-100 million tokens, ~100-200 MB RAM)
ids = np.fromfile(temp_bin, dtype=np.uint16)
total_tokens = len(ids)
print(f"Total tokens: {total_tokens}")

# Truncate to multiple of block_size
n_blocks = total_tokens // block_size
ids = ids[:n_blocks * block_size]
data = ids.reshape(-1, block_size)

# Shuffle and split
np.random.seed(42)
indices = np.random.permutation(len(data))
split = int(len(data) * (1 - val_split))
train_indices = indices[:split]
val_indices = indices[split:]

train_data = data[train_indices]
val_data = data[val_indices]

print(f"Train blocks: {len(train_data)}, Val blocks: {len(val_data)}")
train_data.tofile(output_train)
val_data.tofile(output_val)
os.remove(temp_bin)
print(f"Saved {output_train} and {output_val}")