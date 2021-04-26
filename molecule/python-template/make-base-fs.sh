TMP_CONTAINER=$(docker create python-base-image)
docker export ${TMP_CONTAINER} | tar -C .base/fs/rootfs -xf -
docker rm -f ${TMP_CONTAINER}
