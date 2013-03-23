#!/bin/bash
cd /home/minibay/tpb_archive/data
for i in `find -maxdepth 2 -iname "*.7z"`
do
    echo 'Extracting '$i'...'
    7zr x -y $i >/dev/null
    TARGET=`echo $i|awk -F/ '{print $3}'|awk -F. '{print $1}'`
    echo 'Importing '$TARGET' to MySQL...'
    python /home/minibay/minibay-django/manage.py importtpb $TARGET
    echo 'Cleaning up '$TARGET'...'
    rm -Rf $TARGET
done
