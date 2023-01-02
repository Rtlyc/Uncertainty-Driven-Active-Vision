import numpy as np

file1 = "luomo_blender/3/P_3.npy"
file2 = "luomo/3/P_3.npy"

data1 = np.load(file1, allow_pickle=True)
data2 = np.load(file2, allow_pickle=True)

print(f"Data1: {data1}")
print(f"Data2: {data2}")