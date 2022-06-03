import numpy as np

a = np.array([[0, 1]])
print(a.shape)
print(np.tile(a.transpose(), (1, 3)))
