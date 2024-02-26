#!/bin/bash

# Args
vagrant_rpm_url=$1
vagrant_http_proxy=$2

# Vars
tmp_dir="/tmp"
download_rpm_prefix="https://releases.hashicorp.com/vagrant/2.3.6/vagrant-2.3.6-1.x86_64.rpm"

# Use HTTP proxy to download RPM file
if [[ -n "$vagrant_http_proxy" ]] ; then
    export http_proxy="$vagrant_http_proxy"
    export https_proxy="$vagrant_http_proxy"
fi

# Cleanup
trap "rm -f ${tmp_dir}/vagrant*.rpm" SIGINT SIGTERM ERR EXIT

# Download RPM file from Hashicorp website
cd $tmp_dir
wget $vagrant_rpm_url

### Install RPM package
dnf -y install ./vagrant*.rpm
