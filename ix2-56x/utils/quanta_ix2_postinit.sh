#!/bin/bash
# Copyright (C) 2018 Quanta Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

EXEC_FUNC=${1}

# function
function _start {
while true; do
        if [ -e /run/docker-syncd/sswsyncd.socket ]; then
          echo 0 >/sys/class/gpio/gpio65/value
          sleep 1
          echo 1 >/sys/class/gpio/gpio65/value
          i2cset -y 0x13 0x38 0x0 0xff
          i2cset -y 0x13 0x38 0x2 0xff
          i2cset -y 0x13 0x38 0x3 0xff
          i2cset -y 0x13 0x38 0x4 0xff
          i2cset -y 0x13 0x38 0x5 0xff
          i2cset -y 0x13 0x38 0x6 0xff
          i2cset -y 0x13 0x38 0x7 0xff
          break
        fi
        sleep 10
    done
    echo "Post-Init finished !" 
}

function _stop {
    echo 1 >/sys/class/gpio/gpio65/value
    echo "Post-Init stop !"
}

function _main {
    tart_time_str=`date`
    start_time_sec=$(date +%s)

    if [ "${EXEC_FUNC}" == "start" ]; then
        _start
    elif [ "${EXEC_FUNC}" == "stop" ]; then
        _stop
    fi
}

_main

exit 0