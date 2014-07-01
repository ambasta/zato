#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "${DIR}"

packages=( */ )

PC='\e[0;34m'       # Blue      - Package
EC='\e[0;31m'       # Red       - Error
WC='\e[1;33m'       # Yellow    - Warn
AC='\e[0;32m'       # Green     - Accept
NC='\e[0m'          # No color
# COL=$(tput cols)    # Number of columns

echo -e "${NC}Building packages:"
echo -e "${PC}${packages[*]}"

for package in "${packages[@]}"
    do
        echo
        echo
        echo

        # Move to package directory
        echo -e "${NC}Changing directory to ${PC}${package}"
        if ! cd "${package}"; then
            echo -e "${NC}Ensure that you're in the code directory in repo${EC}[ERROR]"
            exit
        else
            echo -e "${AC}[OK]"
        fi

        echo

        # Uninstall older package
        echo -e "${NC}Uninstalling ${PC}${package}"
        if pip uninstall $package -y &>/dev/null; then
            echo -e "${AC}[OK]"
        else
            echo -e "${NC}Package is not installed. Continuing anyways.${WC}[WARN]"
        fi

        echo

        # Delete existing distributions
        echo -e "${NC}Deleting dist folder"
        if rm -fR dist; then
            echo -e "${AC}[OK]"
        else
            echo -e "${NC}No dist directory found. Continuing anyways.${WC}[WARN]"
        fi

        echo

        # Build distributable
        echo -e "${NC}Building distributable"
        if python setup.py sdist -q &>/dev/null; then
            echo -e "${AC}[OK]"
        else
            echo $output
            echo -e "${NC}Build broken. Kindly report to upstream. ${EC}[ERROR]"
            exit
        fi

        echo

        # Install distributable
        echo -e "${NC}Installing distributable"
        if pip install -q dist/* &>/dev/null; then
            echo -e "${AC}[OK]"
        else
            echo -e "${NC}Install broken. Kindly report to upstream. ${EC}[ERROR]"
            exit
        fi

        echo

        # Move to parent directory
        echo -e "${NC}Returning to parent directory"
        cd ..

        echo
        echo
        echo
    done
