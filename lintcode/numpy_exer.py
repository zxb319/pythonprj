
import numpy as np

arr1=np.array([
    1,2,3,4,5
])

print(arr1)

arr2=np.array({
    'name':'zxb',
    'age':32
})

print(arr2)
print(arr2.ndim)

arr3=np.arange(20,0,-2)

print(arr3)

arr=np.zeros((3,4),dtype=np.int64)
print(arr)

arr=np.ones(10)

print(arr)

arr=np.eye(3)

print(arr)

arr=np.random.random((3,4))
print(arr)

arr=np.random.randint(0,10,(10,10))
print(arr)

arr=np.random.uniform(0,1,(5,5))
print(arr)

arr=np.linspace(0,10,10)
print(arr)

arr=np.arange(0,10,1)
np.random.shuffle(arr)
print(arr)


print(arr.reshape((2,5)))


arr=np.arange(0,10).reshape(2,5)

print(arr.transpose())

arr=np.random.randint(0,10,(2,5))
print(arr)
print(arr.flatten('F'))


arr1=np.random.randint(0,10,(3,3))
arr2=np.random.randint(100,200,(3,3))
arr=np.hstack((arr1,arr2))
print(arr)

arr=np.vstack((arr1,arr2))
print(arr)

arr=np.random.randint(0,10,(3,3))

print(arr[:,:2])