# train.py — CPU‑optimised for Snapdragon X Plus (ARM64, Windows)
import os
os.environ["OMP_NUM_THREADS"] = "10"
os.environ["MKL_NUM_THREADS"] = "10"
os.environ["NUMEXPR_NUM_THREADS"] = "10"
os.environ["OMP_DYNAMIC"] = "FALSE"

import torch
torch.set_num_threads(10)

import torch.nn.functional as F
import numpy as np
from model import GPT
from tokenizers import Tokenizer
import time

# ----------------------------
# Config
# ----------------------------
vocab_size          = 8192
block_size          = 1024
n_embd              = 512
n_head              = 8
n_layer             = 8
batch_size          = 2              # saturates 10 cores, fits in 16 GB RAM
learning_rate       = 3e-4
epochs              = 10
checkpoint_path     = "checkpoint.pt"
train_bin           = "train.bin"
val_bin             = "val.bin"
tokenizer_path      = "tokenizer.json"
print_interval      = 10              # print loss every 10 steps
checkpoint_interval = 500             # less disk I/O (was 10)

device = torch.device('cpu')
print(f"Using CPU, Threads: {torch.get_num_threads()}", flush=True)

# ----------------------------
# Tokenizer & data (RAM loaded)
# ----------------------------
tokenizer = Tokenizer.from_file(tokenizer_path)
pad_id    = tokenizer.token_to_id("<|pad|>")

print("Loading data into RAM...", flush=True)
train_data = np.array(np.memmap(train_bin, dtype=np.uint16, mode='r').reshape(-1, block_size))
val_data   = np.array(np.memmap(val_bin,   dtype=np.uint16, mode='r').reshape(-1, block_size))
print(f"Train blocks: {len(train_data)}, Val blocks: {len(val_data)}", flush=True)

def get_batch(split):
    data = train_data if split == 'train' else val_data
    ix   = torch.randint(len(data), (batch_size,))
    x    = torch.from_numpy(data[ix].astype(np.int64)).to(device)
    return x

# ----------------------------
# Model, optimiser, scheduler
# ----------------------------
model     = GPT(vocab_size, n_embd, n_head, n_layer, block_size).to(device)
optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)
scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
    optimizer,
    T_max=epochs * (len(train_data) // batch_size),
    eta_min=1e-5,
)

# ----------------------------
# Resume from checkpoint
# ----------------------------
start_epoch = 0
start_step  = 0
if os.path.exists(checkpoint_path):
    print("Loading checkpoint...", flush=True)
    ckpt = torch.load(checkpoint_path, map_location=device)
    model.load_state_dict(ckpt['model_state_dict'])
    optimizer.load_state_dict(ckpt['optimizer_state_dict'])
    scheduler.load_state_dict(ckpt['scheduler_state_dict'])
    start_epoch = ckpt['epoch']
    start_step  = ckpt['step']
    print(f"Resumed from epoch {start_epoch}, step {start_step}", flush=True)

# ----------------------------
# Training loop
# ----------------------------
model.train()
step = start_step
t0   = time.perf_counter()
print(f"Training started (print every {print_interval} steps, "
      f"checkpoint every {checkpoint_interval})", flush=True)

for epoch in range(start_epoch, epochs):
    steps_per_epoch = len(train_data) // batch_size
    for batch_idx in range(steps_per_epoch):
        x = get_batch('train')

        # Forward (full precision on CPU)
        logits = model(x[:, :-1])
        loss = F.cross_entropy(
            logits.reshape(-1, vocab_size),
            x[:, 1:].reshape(-1),
            ignore_index=pad_id,
        )

        # Backward
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)  # stability
        optimizer.step()
        scheduler.step()

        step += 1

        # Confirm device on first step
        if step == 1:
            print(f"DEBUG x.device={x.device} | "
                  f"model param device={next(model.parameters()).device}", flush=True)

        # Logging (with ms/step timing)
        if step % print_interval == 0:
            t1          = time.perf_counter()
            ms_per_step = (t1 - t0) * 1000 / print_interval
            print(f"Epoch {epoch} | step {step} | loss {loss.item():.4f} | "
                  f"{ms_per_step:.1f} ms/step", flush=True)
            t0 = t1

        # Checkpoint (every 500 steps, not 10)
        if step % checkpoint_interval == 0:
            torch.save({
                'epoch':                epoch,
                'step':                 step,
                'model_state_dict':     model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'scheduler_state_dict': scheduler.state_dict(),
                'loss':                 loss.item(),
            }, checkpoint_path)
            print(f"Checkpoint saved at step {step}", flush=True)

    # Validation
    model.eval()
    val_losses = []
    with torch.no_grad():
        for _ in range(20):
            x_val = get_batch('val')
            logits_val = model(x_val[:, :-1])
            loss_val = F.cross_entropy(
                logits_val.reshape(-1, vocab_size),
                x_val[:, 1:].reshape(-1),
                ignore_index=pad_id,
            )
            val_losses.append(loss_val.item())
    print(f"=== Epoch {epoch} val loss: {np.mean(val_losses):.4f} ===", flush=True)
    model.train()

    torch.save(model.state_dict(), f"gpt_epoch{epoch}.pth")
    print(f"Saved gpt_epoch{epoch}.pth", flush=True)

print("Training complete.")