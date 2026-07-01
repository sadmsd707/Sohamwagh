# train_tokenizer.py
from tokenizers import Tokenizer, models, trainers, pre_tokenizers
import os

# Paths
corpus_path = "corpus.txt"
tokenizer_path = "tokenizer.json"
subset_size_mb = 200   # use 200 MB for training (adjust if you want)

# Read a subset of the corpus to train tokenizer quickly
print(f"Reading subset of {subset_size_mb} MB from corpus...")
with open(corpus_path, "r", encoding="utf-8", errors="ignore") as f:
    # Read only the first N bytes for speed; tokenizer doesn't need entire file
    subset = f.read(subset_size_mb * 1024 * 1024)

# Write subset to a temp file (tokenizer.train expects a file)
temp_file = "corpus_subset.txt"
with open(temp_file, "w", encoding="utf-8") as f:
    f.write(subset)

# Initialize BPE tokenizer
tokenizer = Tokenizer(models.BPE())
tokenizer.pre_tokenizer = pre_tokenizers.ByteLevel(add_prefix_space=False)

# Trainer settings
trainer = trainers.BpeTrainer(
    vocab_size=8192,          # small vocab = small model
    special_tokens=["<|endoftext|>", "<|pad|>"],
    min_frequency=2
)

# Train
print("Training tokenizer...")
tokenizer.train(files=[temp_file], trainer=trainer)

# Save
tokenizer.save(tokenizer_path)
print(f"Tokenizer saved to {tokenizer_path}")

# Clean up temp file
os.remove(temp_file)