#!/bin/bash
## vim:set ft=sh ts=4 sw=4 et:
set -e
#set -x

self=$0
selfdir=$(dirname -- "${self}")

# search ethminer or ethminer.git directory
up=""
ethminer_dir=$(readlink -en -- "${selfdir}")
bn=$(basename -- ${ethminer_dir})
while [ ${ethminer_dir} != "/" ] && [ $bn != "ethminer" ] && [ $bn != "ethminer.git" ]; do
    up="${up}/.."
    ethminer_dir=$(readlink -en -- "${selfdir}${up}")
    bn=$(basename -- ${ethminer_dir})
done
if [ ${ethminer_dir} == "/" ]; then
    echo "ERROR: Could not find ethminer/ethminer.git directory!"
    exit 1
fi


# Build via docker - assuming this script is in /.........ethminer/build/docker :
docker run -t -v ${ethminer_dir}:/home/hosts/amd64-linux/build/ethminer.git:Z ethminer-build-1604-img \
       sh -c 'cd /home/hosts/amd64-linux/build/ethminer.git/build && VERBOSE=1 CXX=/usr/bin/g++-6 cmake --build . --config release -- -j 4 && cp -a ethminer/ethminer ethminer.out'
