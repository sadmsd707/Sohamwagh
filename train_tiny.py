
max_steps     = 20000
eval_interval = 100
val_iters     = 10
save_every    = 500
out_dir       = "."

# ---------- tokenizer loader ----------
def load_tokenizer(path="tokenizer.json"):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    if isinstance(data, list):
        itos = data
        stoi = {s: i for i, s in enumerate(itos)}
    elif isinstance(data, dict):
        if "model" in data and "vocab" in data["model"]:
            vocab_dict = data["model"]["vocab"]
        else:
            vocab_dict = data
        # if values are ints, treat as stoi directly
        if all(isinstance(v, int) for v in vocab_dict.values()):
            stoi = vocab_dict
            itos = {i: s for s, i in stoi.items()}
        else:
            stoi = vocab_dict
            itos = {i: s for s, i in stoi.items()}
        itos = [itos[i] for i in range(len(itos))]
    else:
        raise ValueError("Unsupported tokenizer.json format")

    class Tokenizer:
        def __init__(self, itos, stoi):
            self.itos = itos
            self.stoi = stoi
        def encode(self, text):
            # simple char-level fallback – replace with your real tokenizer
            return [self.stoi.get(c, 0) for c in text]
        def decode(self, ids):
            return ''.join(self.itos[i] if i < len(self.itos) else '<unk>' for i in ids)
    return Tokenizer(itos, stoi)

def get_batch(split, device="CL"):
    data = train_data if split == "train" else val_data
    ix = np.random.randint(0, len(data) - block_size, (batch_size,))
    x = Tensor.stack(*[Tensor(np.array(data[i:i+block_size], dtype=np.int32), device=device) for i in ix])
    y = Tensor.stack(*[Tensor(np.array(data[i+1:i+1+block_size], dtype=np.int32), device=device) for i in ix])
    return x.realize(), y.realize()

# ---------- main ----------
if __name__ == "__main__":
    device = os.environ.get("DEV", "CL")
    train_data = np.memmap("train.bin", dtype=np.uint16, mode='r')
    val_data   = np.memmap("val.bin",   dtype=np.uint16, mode='r')
    tokenizer  = load_tokenizer("tokenizer.json")
    vocab_size = len(tokenizer.itos) if hasattr(tokenizer, 'itos') else 50257

    config = GPTConfig(vocab_size=vocab_size, block_size=block_size,
                       n_layer=n_layer, n_head=n_head, n_embd=n_embd)
    model = GPT(config)
    model_params = nn.state.get_state_dict(model)
    params = list(model_params.values())
    optim = Adam(params, lr=learning_rate)

    # resume from checkpoint
    ckpt_path = os.path.join(out_dir, "checkpoint.safetensors")
    start_step = 0
    if os.path.exists(ckpt_path):
        print(f"Resuming from {ckpt_path}")
        loaded = safetensors.numpy.load_file(ckpt_path)
        for k, v in model_params.items():
            if k in loaded:
                v.assign(Tensor(loaded[k], device=device))
        if "step" in loaded:
            start_step = int(loaded["step"][0])
            print(f"Resumed from step {start_step}")

    # Define JIT step function
    @TinyJit
    def train_step(x, y) -> Tensor:
        optim.zero_grad()
        logits = model(x)
        loss = logits.reshape(-1, vocab_size).sparse_categorical_crossentropy(y.reshape(-1))
        loss.backward()
        optim.step()
        return loss.realize()

    Tensor.training = True
    start_time = time.time()
    for step in range(start_step, max_steps + 1):
        t0 = time.time()
        x, y = get_batch("train", device)

        # forward + backward + update (JIT-compiled)
        loss = train_step(x, y)

        t1 = time.time()

        if step > 0 and step % 10 == 0:
            elapsed = time.time() - start_time
            print(f"step={step} loss={loss.numpy().item():.4f} time={elapsed:.2f}s", flush=True)

        # logging & validation
        if step % eval_interval == 0 or step == max_steps:
            val_loss = 0.0
            Tensor.training = False
            for _ in range(val_iters):
                xv, yv = get_batch("val", device)
                logits_v = model(xv)
                loss_v = logits_v.reshape(-1, vocab_size).sparse_categorical_crossentropy(yv.reshape(-1))
                val_loss += loss_v.numpy().item()
            val_loss = val_loss / val_iters
            Tensor.training = True
            print(f"step {step:5d} | loss: {loss.numpy().item():.4f} | val_loss: {val_loss:.4f} | time: {(t1-t0)*1000:.1f}ms", flush=True)

        # checkpointing
        if step > 0 and step % save_every == 0:
            os.makedirs(out_dir, exist_ok=True)
            state_dict = {k: v.numpy() for k, v in model_params.items()}
            state_dict["step"] = np.array([step], dtype=np.int32)
            safetensors.numpy.save_file(state_dict, ckpt_path)
            print(f"Checkpoint saved at step {step}", flush=True)

    print("Training finished.")
