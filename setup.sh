#!/bin/bash

if [ -x /usr/bin/python3.6 ] || [ -x /usr/bin/python36 ]; then
   pip3 install --editable .
   echo -e "\e[92m quicksystem tool has been installed successfully! \e[0m\n"

else
    echo -e "\e[91m Python3.6 is not installed on system! \e[0m"
fi
