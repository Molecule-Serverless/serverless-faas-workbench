from time import time
import gzip
import os


def handler(event):
    file_size = event['file_size']
    file_write_path = '/tmp/file'
    #file_write_path = event['source_file']

    start = time()
    with open(file_write_path, 'wb') as f:
        f.write(os.urandom(file_size * 1024 * 1024))
    disk_latency = time() - start

    with open(file_write_path, 'rb') as f:
        start = time()
        with gzip.open('/tmp/result.gz', 'wb') as gz:
            gz.writelines(f)
        compress_latency = time() - start

    print(compress_latency)

    return {'disk_write': disk_latency, "compress": compress_latency}

def invokeHandler():
    startTime = int(round(time() * 1000))
    ret = handler({'file_size': 4, 'source_file':'./animal-dog.jpg'}) #4M file
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
