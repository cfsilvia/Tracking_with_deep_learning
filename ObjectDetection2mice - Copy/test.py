import torch
print(torch.__version__)
print(torch.cuda.is_available())   # should be True
print(torch.version.cuda)     