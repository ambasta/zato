#!/bin/bash

echo "Zato requires the following global packages: [haproxy]. Please ensure that they are installed before you start the server."

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "${DIR}"

HOMEDIR="$(getent passwd $USER | awk -F ':' '{print $6}')"
BUILD_DIR="${HOMEDIR}/.zato-builder"

if [ ! -d "config" ]; then
    mkdir "${BUILD_DIR}"
fi

packages=("zato-common" "zato-server" "zato-client" "zato-agent" "zato-broker" "zato-cli" "zato-web-admin")

PC='\e[0;34m'       # Blue      - Package
EC='\e[0;31m'       # Red       - Error
WC='\e[1;33m'       # Yellow    - Warn
AC='\e[0;32m'       # Green     - Accept
NC='\e[0m'          # No color
# COL=$(tput cols)    # Number of columns

CACHE_DIR="${BUILD_DIR}/pip_cache"
LOGFILE="${BUILD_DIR}/build.log"

function usage
{
    echo "usage: build_packages [[-l file] | [-c cache_dir ] | [-h]]"
}

while [ "$1" != "" ]; do
    case $1 in
        -l | --logfile )    shift
                            LOGFILE=$1
                            ;;
        -c | --cache-dir )  shift
                            CACHE_DIR=$1
                            ;;
        -h | --help )       usage
                            exit
                            ;;
        * )                 usage
                            exit 1
    esac
    shift
done

PIP_INSTALL_PARAMS="--download-cache=${CACHE_DIR}"

# Install build dependencies
echo -e "${NC}Installing Global Dependencies"

if pip install "${PIP_INSTALL_PARAMS}" hgdistver numpy 1>>"${LOGFILE}" 2>&1; then
    echo -e "${AC}[OK]"
else
    echo -e "${NC}Unable to install global dependencies${EC}[ERROR]"
    echo -e "${NC}Kindly refer ${LOGFILE} or report to upstream with the same attached."
fi

echo
echo

echo -e "${NC}Patching hgdistver"
if ! hgdistver_path=$(python -c 'import hgdistver; print(hgdistver.__file__[:-1])'); then
    echo -e "${NC}Unable to find the path to django_openid_auth. Kindly report to upstream. ${EC}[ERROR]"
fi
if ! patch -N ${hgdistver_path} < patches/hgdistver_git_fixes.patch 1>>"${LOGFILE}" 2>&1; then
    echo -e "${NC}Unable to patch hgdistver. Kindly report to upstream. ${EC}[ERROR]"
fi
echo -e "${AC}[OK]"

echo
echo

# Uninstall django_openid_auth
echo -e "${NC}Uninstalling django_openid_auth"
if ! pip uninstall django_openid_auth -y 1>>"${LOGFILE}" 2>&1; then
    echo -e "${NC}Package is not installed. Continuing anyways.${AC}[OK]"
fi
echo -e "${AC}[OK]"

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
        if pip uninstall "${package}" -y 1>>"${LOGFILE}" 2>&1; then
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
        if python setup.py sdist 1>>"${LOGFILE}" 2>&1; then
            echo -e "${AC}[OK]"
        else
            echo -e "${NC}Build broken. Kindly report to upstream with ${LOGFILE}. ${EC}[ERROR]"
            exit
        fi

        echo

        # Install distributable
        echo -e "${NC}Installing distributable"
        if pip install "${PIP_INSTALL_PARAMS}" dist/* 1>>"${LOGFILE}" 2>&1; then
            echo -e "${AC}[OK]"
        else
            echo -e "${NC}Install broken. Kindly report to upstream with ${LOGFILE}. ${EC}[ERROR]"
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
if ! patch -N ${openid_path}/urls.py < patches/django_openid_django_1_6.patch 1>>"${LOGFILE}" 2>&1; then
    echo -e "${NC}Unable to patch django_openid_auth. Kindly report to upstream. ${EC}[ERROR]"
fi

echo
echo
echo

echo -e "${NC}All Done. ${AC}[OK]${NC}"
