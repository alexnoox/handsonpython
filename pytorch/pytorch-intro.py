#%%
from __future__ import print_function
import torch

x = torch.empty(5, 3)
print(x)


#%%
x = torch.rand(5, 3)
print(x)


#%%
x = torch.zeros(5, 3, dtype=torch.long)
print(x)


#%%
x = torch.tensor([5.5, 3])
print(x)

x = x.new_ones(5, 3, dtype=torch.double)      # new_* methods take in sizes
print(x)

x = torch.randn_like(x, dtype=torch.float)    # override dtype!
print(x)                                      # result has the same size

print(x.size())


#%%
y = torch.rand(5, 3)
print(x + y)
print(torch.add(x, y))
result = torch.empty(5, 3)
torch.add(x, y, out=result)
print(result)


#%%
x = torch.randn(4, 4)
y = x.view(16)
z = x.view(-1, 8)  # the size -1 is inferred from other dimensions
print(x.size(), y.size(), z.size())


#%%
a = torch.ones(5)
print(a)
b = a.numpy()
print(b)


#%%
a.add_(1)
print(a)
print(b)


#%%
import numpy as np
a = np.ones(5)
b = torch.from_numpy(a)
np.add(a, 1, out=a)
print(a)
print(b)
