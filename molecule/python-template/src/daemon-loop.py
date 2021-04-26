import traceback
import json
import os
import time
import ol
import uuid
import socket
import array

# pkgs to cache apps's usage
import importlib.util
import sys
import base64
import cv2


import tornado
import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.netutil

file_sock_path = 'fork.sock'
file_sock = None

# global variables:
func = None
funcName = None
def start_app_server():
    # print("daemon.py: start app server on fd: %d" % file_sock.fileno())

    class SockFileHandler(tornado.web.RequestHandler):
        def post(self):
            try:
                data = self.request.body
                try :
                    event = json.loads(data)
                except:
                    self.set_status(400)
                    self.write('bad POST data: "%s"'%str(data))
                    return
                self.write(event)
                tornado.ioloop.IOLoop.instance().stop() # Stop the server immediately after receiving the first request
            except Exception:
                self.set_status(500) # internal error
                self.write(traceback.format_exc())

    tornado_app = tornado.web.Application([
        (".*", SockFileHandler),
    ])
    server = tornado.httpserver.HTTPServer(tornado_app)
    server.add_socket(file_sock)
    tornado.ioloop.IOLoop.instance().start()
    server.start()

def start_faas_server():
    global func
    sys.path.append("/code")
    # load code
    if func is None:
        func = importlib.import_module('index')

    ####### hard code start ######
    # invoke the function
    # print("image_resize output: ")
    f = open("/code/test.jpg", 'rb')
    output = func.handler({'img': LoadTestImage(), 'height': 200, 'width': 200})
    # print(output)
    ####### hard code end #######
    while True:
        time.sleep(1)
        #print("I am not dead")

    return

def LoadTestImage():
    f = open("/code/test.jpg", 'rb')
    return str(base64.b64encode(f.read()), encoding='ascii')

def Invoke():
    return

# copied from https://docs.python.org/3/library/socket.html#socket.socket.recvmsg
def recv_fds(sock, msglen, maxfds):
    fds = array.array("i")   # Array of ints
    msg, ancdata, flags, addr = sock.recvmsg(msglen, socket.CMSG_LEN(maxfds * fds.itemsize))
    for cmsg_level, cmsg_type, cmsg_data in ancdata:
        if (cmsg_level == socket.SOL_SOCKET and cmsg_type == socket.SCM_RIGHTS):
            # Append data, ignoring any truncated integers at the end.
            fds.frombytes(cmsg_data[:len(cmsg_data) - (len(cmsg_data) % fds.itemsize)])
    return msg, list(fds)


def start_fork_server():
    global file_sock
    global file_sock_path
    # print("daemon.py: start fork server on fd: %d" % file_sock.fileno())
    file_sock.setblocking(True)

    while True:
        client, info = file_sock.accept()
        _, fds = recv_fds(client, 20, 5)
        pid = os.fork()
        target_fd = fds[0]
        uts_namespace_fd = fds[1]
        pid_namespace_fd = fds[2]
        ipc_namespace_fd = fds[3]
        mnt_namespace_fd = fds[4]

        if pid:
            # the grand-parent process
            # ret, exitcode = os.waitpid(pid, 0)
            # end = time.perf_counter_ns()
            # print('waitpid returns %d %d' % (ret, exitcode))
            # client.sendall(bytes(str(pid), 'utf8'))
            client.close()
            os.close(target_fd)
            os.close(uts_namespace_fd)
            os.close(pid_namespace_fd)
            os.close(ipc_namespace_fd)
            os.close(mnt_namespace_fd)
        else:
            # the parent process
            os.fchdir(target_fd)
            os.chroot(".")
            os.close(target_fd)
            # rv = ol.unshare()
            # assert rv == 0
            rv = ol.setns(uts_namespace_fd)
            assert rv == 0
            rv = ol.setns(pid_namespace_fd)
            assert rv == 0
            rv = ol.setns(ipc_namespace_fd)
            assert rv == 0
            rv = ol.setns(mnt_namespace_fd)
            assert rv == 0
            os.close(uts_namespace_fd)
            os.close(pid_namespace_fd)
            os.close(ipc_namespace_fd)
            os.close(mnt_namespace_fd)
            pid = os.fork()
            if pid:
                # the parent process
                client.sendall(bytes(str(pid), 'utf8'))
                client.close()
                os._exit(0)
            else:
                # the child process
                file_sock.close()
                file_sock = None

                # file_sock_path = 'fork.sock' + '.' + str(os.getpid()) # + '.' + str(uuid.uuid4())
                # file_sock = tornado.netutil.bind_unix_socket(file_sock_path)
                client.close()
                start_faas_server()
                exit()


def main():
    global file_sock
    # print("daemon.py: main")
    file_sock = tornado.netutil.bind_unix_socket(file_sock_path)
    start_fork_server()

if __name__ == '__main__':
    main()
