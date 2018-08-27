#!/bin/sh
## vim:set ft=sh ts=4 sw=4 et:
set -e

#------------------------
# build the docker image and name it "ethminer-build-1604-img"
#------------------------
#docker build -t ethminer-build-1604-img -f Dockerfile .


#------------------------
#run the image interactive with zsh shell
#------------------------

# expect this script is in /.......ethminer/Docker
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

docker run -ti -v ${ethminer_dir}:/home/hosts/amd64-linux/build/ethminer.git:Z ethminer-build-1604-img zsh
