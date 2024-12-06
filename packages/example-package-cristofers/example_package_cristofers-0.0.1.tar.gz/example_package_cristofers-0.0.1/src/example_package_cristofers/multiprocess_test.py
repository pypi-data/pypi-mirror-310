# from multiprocessing import Process
# import os

# def info(title):
#     print(title)
#     print('module name:', __name__)
#     print('parent process:', os.getppid())
#     print('process id:', os.getpid())

# def f(name):
#     info('function f')
#     print('hello', name)

# if __name__ == '__main__':
#     info('main line')
#     p = Process(target=f, args=('bob',))
#     p.start()
#     p.join()

import numpy as np

d3_array = np.array([
    [[1,2],[3,4],[5,6],[7,8]],
    [[9,10],[11,12],[13,14],[15,16]],
    [[17,18],[19,20],[21,22],[23,24]]
    
    ])

print(d3_array.shape)

L,D,N = d3_array.shape
values = []
reshaped_X = []

for d in range(D):
    for l in range(L):
        values.append(d3_array[l][d][:N])
    reshaped_X.append(np.concatenate((values), axis=None))
    values.clear()

X = np.array(reshaped_X)

