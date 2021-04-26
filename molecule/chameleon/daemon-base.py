# This python file is the runtime for directly startup from `runc run` and call code in /code/index.py
import traceback
import json
import os
import time

import importlib.util
import sys
import base64

func = None

def start_faas_server():
    global func
    sys.path.append("/code")
    # load code
    if func is None:
        func = importlib.import_module('index')

    ####### hard code start ######
    # invoke the function
    print(func.invokeHandler())

def LoadTestImage():
    f = open("/code/test.jpg", 'rb')
    return str(base64.b64encode(f.read()), encoding='ascii')

def main():
    start_faas_server()

if __name__ == '__main__':
    main()

