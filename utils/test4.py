import pickle
import numpy as np

fr = open('../emulator/MIMII/saxs10.pkl', 'rb')
lst = pickle.load(fr)
dim1 = len(lst)
dim2 = len(lst[0])
dim3 = len(lst[0][0])

# 打印三维列表的形状
print(f"({dim1}, {dim2}, {dim3})")