import torch
import time
torch.set_num_threads(10)
a = torch.randn(2000, 2000)
b = torch.randn(2000, 2000)
t0 = time.time()
for _ in range(10):
    c = a @ b
print(f"10 matmuls: {time.time()-t0:.3f}s")