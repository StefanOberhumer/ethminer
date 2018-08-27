FROM ubuntu:xenial-20180726
MAINTAINER noname <stefan@obssys.com>


# Generate a docker container for building ethminer under linux ubuntu-16.04 (including CUDA and dbus)


RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get -y install vim zsh wget git cmake

RUN apt-get -y install software-properties-common
RUN add-apt-repository -y ppa:ubuntu-toolchain-r/test
RUN apt-get -y update

# set timezone to Europe/Vienna
#RUN apt-get install -qy tzdata && rm /etc/localtime && cd /etc && ln -s /usr/share/zoneinfo/Europe/Vienna localtime && echo "Europe/Vienna" > timezone

# if we search a missing file we can use 'apt-file search <filename>'
#RUN apt-get -y install apt-file && apt-file update

# install gcc-6 and gcc-4.8
# refer to https://gist.github.com/application2000/73fd6f4bf1be6600a2cf9f56315a2d91
RUN apt-get install gcc-6 g++-6 -y && \
    update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-6 60 --slave /usr/bin/g++ g++ /usr/bin/g++-6 && \
    apt-get install gcc-4.8 g++-4.8 -y && \
    update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-4.8 60 --slave /usr/bin/g++ g++ /usr/bin/g++-4.8;

# sudo update-alternatives --config gcc
#RUN apt-get -y install 'g++'
#RUN apt-get -qy install g++-7


# Install OpenCL includes
RUN apt-get -y install mesa-common-dev

# Install DBUS support
RUN apt-get -y install libdbus-1-dev


# Install CUDA versions
RUN apt-key adv --fetch-keys http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/7fa2af80.pub && \
    cd /root && mkdir CUDA && cd CUDA && \
    wget "http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/cuda-repo-ubuntu1604_8.0.61-1_amd64.deb" && \
    wget "http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/cuda-repo-ubuntu1604_9.0.176-1_amd64.deb" && \
    wget "http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/cuda-repo-ubuntu1604_9.1.85-1_amd64.deb" && \
    wget "http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/cuda-repo-ubuntu1604_9.2.88-1_amd64.deb" && \
    wget "http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/cuda-repo-ubuntu1604_9.2.148-1_amd64.deb" && \
    dpkg -i cuda-repo-ubuntu1604_8.0.61-1_amd64.deb && \
    dpkg -i cuda-repo-ubuntu1604_9.0.176-1_amd64.deb && \
    dpkg -i cuda-repo-ubuntu1604_9.1.85-1_amd64.deb && \
    dpkg -i cuda-repo-ubuntu1604_9.2.88-1_amd64.deb && \
    dpkg -i cuda-repo-ubuntu1604_9.2.148-1_amd64.deb
RUN apt-get -qy update && \
	apt-get -qy install \
		cuda-core-8-0 cuda-cudart-dev-8-0 \
		cuda-core-9-0 cuda-cudart-dev-9-0 \
		cuda-nvcc-9-1 cuda-cudart-dev-9-1 \
		cuda-nvcc-9-2 cuda-cudart-dev-9-2


# prepare out build directory which get mapped via 'docker -v $MY_LOCAL_DIRECTORY:/home/hosts/amd64-linux/build/ethminer.git:Z' option
RUN mkdir -p /home/hosts/amd64-linux/build/ethminer.git


# 1st build - implies building boost library - so boost is not built every time
RUN cd /tmp && \
    git clone https://github.com/ethereum-mining/ethminer.git && \
    cd ethminer && git submodule update --init --recursive && \
    mkdir build && cd build && \
    cmake -DCMAKE_CXX_COMPILER=/usr/bin/g++-6 -DCMAKE_C_COMPILER=/usr/bin/gcc-6 \
          -DHUNTER_JOBS_NUMBER=4 -DHUNTER_STATUS_DEBUG=OFF \
          -DCOMPUTE=61 -DETHDBUS=ON \
          -DCUDA_TOOLKIT_ROOT_DIR=/usr/local/cuda-9.0 .. && \
    VERBOSE=1 CXX=/usr/bin/g++-6 cmake --build . --config release -- -j 4 && \
 \
    cd / && rm -rf /tmp/ethminer
#
