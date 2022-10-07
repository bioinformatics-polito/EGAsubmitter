FROM debian:buster-20220328-slim
ENV DEBIAN_FRONTEND noninteractive

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

RUN apt-get update --fix-missing && apt-get install -y wget bzip2 ca-certificates \
    python3 snakemake perl gawk \
    python3-configargparse \
    python3-pandas \
    python3-yaml python3-ruamel.yaml \
    python3-jsonschema python3-simplejson \
    curl jq java-common default-jdk


# add R
#install packages advised by Gianluca Della Vedova <gianluca@dellavedova.org>
RUN apt-get install -y procps uuid-runtime

CMD ["/bin/bash"]
