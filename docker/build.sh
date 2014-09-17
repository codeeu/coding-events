#!/bin/bash

set_latest=false

function error() {
    >&2 echo "${1}"
    exit 1
}

function usage() {
    echo "usage: [sudo] build.sh [latest]"
    exit 0
}

[[ $# -lt 2 ]] || usage
if [[ $# -eq 1 ]]; then
    if [[ "${1}" == "latest" ]]; then
        set_latest=true
    else
        usage
    fi
fi

# figure out the app name (the dirname above this one)
app_name=$(basename $(dirname $(pwd)))

[[ -f "Dockerfile" ]] || error "Dockerfile not found in this directory"
maintainer=$(cat Dockerfile | grep MAINTAINER | \
    sed 's/^MAINTAINER[[:space:]]*\([^[[:space:]]*\)[[:space:]]*$/\1/')

# the Docker repository to use for the generated image
docker_repo="${maintainer}/${app_name}"

function output_result() {
    if [[ "${1}" -eq 0 ]]; then
        echo -e "\e[32mOK\e[0m"
    else
        echo -e "\e[31mFailed!\e[0m"
    fi
    return "${1}"
}

function cleanup() {
    echo -n "Cleaning up... "
    rm -f "tmp_install.sh"
    output_result "${?}"
}

[[ "$(id -u)" -eq "0" ]] || error "Script must be run as root"

docker=$(which docker) || error "Docker is needed"
git=$(which git) || error "Git is needed"

temp_dir=$(mktemp -d)
trap 'cleanup' EXIT

echo -n "Looking for last tag... "
last_tag=$(git describe --abbrev=0 --tags 2> /dev/null)
if [[ "${?}" -eq 0 ]]; then
    echo -e "\e[32m${last_tag}\e[0m"
else
    echo -e "\e[31mFailed!\e[0m"
    error "Git repository must have at least one tag"
fi

echo -n "Creating temporary install script... "
sed "s/{{check-tag}}/${last_tag}/" _install.sh > tmp_install.sh
output_result "${?}" || exit

echo "Running docker build:"
docker build -t="${docker_repo}:${last_tag}" .
if [[ "${?}" -ne 0 ]]; then
    echo -e "\n\n\e[31m***\e[0m Docker execution Failed!\n"
fi

if [[ "${set_latest}" == "true" ]]; then
    echo -n "Retrieving image ID... "
    image_id=$(docker images | grep "${docker_repo}" | grep "${last_tag}" | sed 's/[[:space:]]\+/ /g' | cut -d' ' -f 3)
    if [[ "${?}" -eq 0 ]]; then
        echo -e "\e[32m${image_id}\e[0m"
        echo -n "Setting latest tag... "
        docker tag "${image_id}" "${docker_repo}:latest"
        output_result "${?}"
    else
        echo -e "\e[31mFailed!\e[0m"
        error "Git repository must have at least one tag"
    fi
else
    echo "Skip tagging image as latest"
fi

# cleanup does this, but still, let's be nice
echo -n "Deleting temporary install script... "
rm -f tmp_install.sh
output_result "${?}" || exit
