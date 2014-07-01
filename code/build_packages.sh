#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "${DIR}"

packages=("zato-common" "zato-server" "zato-client" "zato-agent" "zato-broker" "zato-cli" "zato-web-admin")

PC='\e[0;34m'       # Blue      - Package
EC='\e[0;31m'       # Red       - Error
WC='\e[1;33m'       # Yellow    - Warn
AC='\e[0;32m'       # Green     - Accept
NC='\e[0m'          # No color
# COL=$(tput cols)    # Number of columns


# Install build dependencies
echo -e "${NC}Installing Global Dependencies"
if output=(pip install hgdistver numpy -q); then
    echo -e "${AC}[OK]"
else
    echo -e "${NC}${output}"
    echo -e "${NC}Unable to install global dependencies${EC}[ERROR]"
fi

echo
echo

# Uninstall django_openid_auth
echo -e "${NC}Uninstalling django_openid_auth"
if pip uninstall django_openid_auth -y &>/dev/null; then
    echo -e "${AC}[OK]"
else
    echo -e "${NC}Package is not installed. Continuing anyways.${WC}[WARN]"
fi

echo
echo

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
            echo -e "${NC}Build broken. Kindly report to upstream. ${EC}[ERROR]"
            exit
        fi

        echo

        # Install distributable
        echo -e "${NC}Installing distributable"
        if output=$(pip install -q dist/*); then
            echo -e "${AC}[OK]"
        else
            echo ${output}
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

# Patch django_openid_auth
echo -e "${NC}Patching django_openid_auth"
if ! openid_path=$(python -c 'import django_openid_auth; print(django_openid_auth.__path__[0])'); then
    echo -e "${NC}Unable to find the path to django_openid_auth. Kindly report to upstream. ${EC}[ERROR]"
fi
if ! output=$(patch -N "${openid_path}/urls.py" < patches/django_openid_django_1_6.patch); then
    echo -e "${NC}Unable to patch django_openid_auth. Kindly report to upstream. ${EC}[ERROR]"
fi

echo
echo
echo

echo -e "${NC}All Done. ${AC}[OK]${NC}"
