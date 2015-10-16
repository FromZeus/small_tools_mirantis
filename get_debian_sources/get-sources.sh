#!/bin/bash

#set -x

clone()
{
  git clone "ssh://dtrishkin@review.fuel-infra.org:29418/packages/trusty/$packet"
  pushd $dist
  if [ ! -d buffer ]; then
    mkdir -p buffer
  fi
  git co "origin/7.0"
  cp -rf * buffer
  git co "origin/8.0"
  cp -rf buffer/* .
  rm -rf buffer
  popd
}

while [ $# -gt 0 ]; do
  case "$1" in
    -p)
      shift
      packet="$1"
      ;;
    -d)
      shift
      dist="$1"
      ;;
    -c)
      shift
      clone_if=true
      ;;
    *)
      shift
      ;;
  esac
done

if [[ $packet == "" || $dist == "" ]]; then
  echo "Specify -p and -d"
  exit 0
fi

len=1

if [ ${packet:0:3} = "lib" ]; then
    len=4
fi

experimental=false
echo "Trying to get experimental version..."
url="https://packages.debian.org/source/experimental/$packet"
wget $url -O "$packet.pack"

info=$(cat "$packet.pack" | grep dsc)
if [ "$info" ]; then
  experimental=true
  echo "Success! We got it!"
  sources_url=${info##*href=\"}
  sources_url=${sources_url%\">*}
else
  echo "Fail! No experimental here!"
  url="https://packages.qa.debian.org/${packet:0:${len}}/${packet}.html"
  wget $url

  info=$(cat "$packet.html" | grep dsc)
  sources_url=${info##*href=\"}
  sources_url=${sources_url%\" title*}
  rm -rf "$packet.html"
fi
rm -rf "$packet.pack"

if [[ $clone_if == true ]]; then
  clone
fi

if [ "$(ls $dist)" ]; then
  dist="$dist/building"
fi
if [ ! -d $dist ]; then
  mkdir -p $dist
fi
pushd $dist
dget $sources_url
targz=$(find . -name "*tar.gz" -o -name "*tar.xz")
for el in $targz; do
  tar -xvf $el
  rm -f $el
done
rm -f $(find . -name "*dsc")
popd

rm -f "$packet.html"

echo -e "\n"
pushd $dist > /dev/null
echo $(git br)
popd > /dev/null
if [[ $experimental == true ]]; then
  echo "Experimantal brunch used"
else
  echo "Testing brunch used"
fi
echo -e "\nSources are from\n  $sources_url"
echo $(date -R)