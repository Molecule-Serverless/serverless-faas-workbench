#include <Python.h>
#include <arpa/inet.h>
#include <stdlib.h>
#include <stdio.h>
#include <sched.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <sys/types.h>
#include <sys/wait.h>

static PyObject *ol_unshare(PyObject *module) {
    int res = unshare(CLONE_NEWUTS|CLONE_NEWPID|CLONE_NEWIPC);
    return Py_BuildValue("i", res);
}

static PyObject *ol_fork(PyObject *module) {
    int res = fork();
    return Py_BuildValue("i", res);
}

static PyObject *ol_setns(PyObject *module, PyObject *args) {
    int fd, res;

    if (!PyArg_ParseTuple(args, "i", &fd))
        return Py_BuildValue("i", -1);

    res = setns(fd, 0);
    return Py_BuildValue("i", res);
}

static PyMethodDef OlMethods[] = {
    {"unshare", (PyCFunction)ol_unshare, METH_NOARGS, "unshare"},
    {"fork", (PyCFunction)ol_fork, METH_NOARGS, "fork"},
    {"setns", (PyCFunction)ol_setns, METH_VARARGS, "setns"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef olMod = {
    PyModuleDef_HEAD_INIT,
    "ol",
    NULL,
    -1,
    OlMethods
};

PyMODINIT_FUNC
PyInit_ol(void)
{
    return PyModule_Create(&olMod);
}
