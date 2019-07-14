#!/bin/bash
set -e

dn=$1
fn=$2

if [ "$dn" = "" -o "$fn" = "" ];
then
	echo "Usage: $0 <dirname> <floppyfile name>"
	exit 1
fi

tmpfile=$(mktemp)
tmpdir=$(mktemp -d)

dd if=/dev/zero of=$tmpfile bs=1440K count=1
mkfs.msdos -F 12 $tmpfile
sudo mount $tmpfile $tmpdir
sudo cp -r $dn/* $tmpdir/
sudo umount $tmpdir

cp $tmpfile $fn

rm -rf $tmpdir $tmpfile

exit 0
