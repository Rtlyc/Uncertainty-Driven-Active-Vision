import numpy as np

file1 = "luomo_blender/1/P_1.npy"
file2 = "luomo/1/P_1.npy"

data1 = np.load(file1, allow_pickle=True)
data2 = np.load(file2, allow_pickle=True)

print(f"Data1: {data1}")
print(f"Data2: {data2}")