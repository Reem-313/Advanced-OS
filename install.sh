#!/usr/bin/env bash

#
# disable unused services
#
systemctl disable --now bluetooth

apt install rsync sshpass
