#!/bin/bash

if command -v python3.12 >/dev/null 2>&1 || command -v python3 >/dev/null 2>&1; then
   pip3 install --editable .
   echo -e "\e[92m quicksystem tool has been installed successfully! \e[0m\n"

else
    echo -e "\e[91m Python 3.12 or later is not installed on system! \e[0m"
fi
