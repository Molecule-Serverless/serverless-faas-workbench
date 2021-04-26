#import boto3
import uuid
from time import time
import cv2
import os

#s3_client = boto3.client('s3')

tmp = "/data/"
FILE_NAME_INDEX = 0
FILE_PATH_INDEX = 2


def video_processing(object_key, video_path):
    #file_name = object_key.split(".")[FILE_NAME_INDEX]
    file_name = 'test'
    result_file_path = tmp+file_name+'-output.avi'

    if os.path.exists(result_file_path):
        os.remove(result_file_path)

    video = cv2.VideoCapture(video_path)

    width = int(video.get(3))
    height = int(video.get(4))

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(result_file_path, fourcc, 20.0, (width, height))

    start = time()
    while video.isOpened():
        ret, frame = video.read()

        if ret:
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            tmp_file_path = tmp+'tmp.jpg'
            cv2.imwrite(tmp_file_path, gray_frame)
            gray_frame = cv2.imread(tmp_file_path)
            out.write(gray_frame)
        else:
            break

    latency = time() - start

    video.release()
    out.release()
    return latency, result_file_path


def handler(event):
    #input_bucket = event['input_bucket']
    object_key = event['object_key']
    #output_bucket = event['output_bucket']

    #download_path = tmp+'{}{}'.format(uuid.uuid4(), object_key)
    download_path = event['video_path']

    #s3_client.download_file(input_bucket, object_key, download_path)


    latency, upload_path = video_processing(object_key, download_path)

    #s3_client.upload_file(upload_path, output_bucket, upload_path.split("/")[FILE_PATH_INDEX])

    return latency

def invokeHandler():
    startTime = int(round(time() * 1000))
    ret = handler({'object_key':'same_video.test.mp4',
                   'video_path':'/data/SampleVideo_1280x720_10mb.mp4'})
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
