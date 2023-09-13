FROM debian:buster-20220328-slim
ENV DEBIAN_FRONTEND noninteractive
ENV CONDA_ENV_NAME="EGAsubmitter"

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

RUN apt-get update --fix-missing && apt-get install -y wget bzip2 ca-certificates \
    libglib2.0-0 libxext6 libsm6 libxrender1 \
    vim \
    gmsl gawk perl python3 \
    cython python3-setuptools

#instal packages advised by Gianluca Della Vedova <gianluca@dellavedova.org>
RUN apt-get install -y procps uuid-runtime

WORKDIR /tmp
SHELL ["/bin/bash", "-c","-l"]

RUN wget -O miniconda.sh https://repo.anaconda.com/miniconda/Miniconda3-py39_23.1.0-1-Linux-x86_64.sh
RUN chmod ugo+x miniconda.sh

RUN ./miniconda.sh -b -p /opt/conda && \
    rm miniconda.sh && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> /etc/profile

COPY EGAsubmitter.yml EGAsubmitter.yml

RUN conda env create -f EGAsubmitter.yml

ENV PATH "/opt/conda/bin:/opt/conda/envs/${CONDA_ENV_NAME}/bin:${PATH}"
ENV CONDA_DEFAULT_ENV $CONDA_ENV_NAME
ENV CONDA_PREFIX /opt/conda/envs/$CONDA_ENV_NAME
ENV PYTHONPATH "/opt/conda/envs/EGAsubmitter/lib/python3.9/site-packages"
# for interactive occam-run which uses -l and has the user home mounted by default
RUN echo "export PATH=/opt/conda/bin:/opt/conda/envs/${CONDA_ENV_NAME}/bin:${PATH}" >> /etc/profile
RUN echo "export PYTHONPATH=/opt/conda/envs/EGAsubmitter/lib/python3.9/site-packages" >> /etc/profile

CMD ["/bin/bash"]
