import numpy as np
from time import time


def matmul(n):
    A = np.random.rand(n, n)
    B = np.random.rand(n, n)

    start = time()
    C = np.matmul(A, B)
    latency = time() - start
    return latency


def handler(event):
    n = int(event['n'])
    result = matmul(n)
    print(result)
    return result

def invokeHandler():
    startTime = int(round(time() * 1000))
    ret = handler({'n': 100})
    retTime = int(round(time() * 1000))

    output = {'results': ret,
        'startTime': startTime,
        'retTime' : retTime,
        'invokeTime': startTime
        }
    logf = open("log.txt", "w")
    logf.write(str(output))

    print(output)

if __name__ == "__main__":
    invokeHandler()
