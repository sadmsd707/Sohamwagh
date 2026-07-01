# api.py
import os, sys
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from tinygrad import Tensor, nn
import safetensors.numpy
from tokenizers import Tokenizer
from tiny_model import GPT, GPTConfig

app = FastAPI()

# Enable CORS so our web page can connect to the api
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Force UTF-8 encoding for stdout on Windows
if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8")

# Load Tokenizer
tokenizer_path = "tokenizer.json"
tokenizer = Tokenizer.from_file(tokenizer_path)
vocab_size = tokenizer.get_vocab_size()

# Load Model
config = GPTConfig(
    vocab_size=vocab_size,
    block_size=256,
    n_layer=6,
    n_head=6,
    n_embd=384
)
model = GPT(config)

# Load checkpoint
device = os.environ.get("DEV", "CL")
ckpt_path = "checkpoint.safetensors"
if os.path.exists(ckpt_path):
    print(f"Loading checkpoint weights from {ckpt_path}...")
    ckpt = safetensors.numpy.load_file(ckpt_path)
    state = nn.state.get_state_dict(model)
    for k, v in state.items():
        if k in ckpt:
            v.assign(Tensor(ckpt[k], device=device))

class GenerationRequest(BaseModel):
    prompt: str
    max_tokens: int = 100
    temperature: float = 0.8

@app.post("/generate")
def generate_text(req: GenerationRequest):
    try:
        # Encode prompt
        prompt_ids = tokenizer.encode(req.prompt).ids
        context = Tensor([prompt_ids], device=device)
        
        # Generate new tokens
        output = model.generate(context, max_new_tokens=req.max_tokens, temperature=req.temperature, top_k=50)
        
        # Decode output
        out_ids = output.numpy().flatten().tolist()
        generated_text = tokenizer.decode(out_ids)
        
        # Clean BPE control characters
        clean_text = generated_text.replace("Ġ", " ").replace("Ċ", "\n").replace("ĉ", "\n")
        
        return {"prompt": req.prompt, "output": clean_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
