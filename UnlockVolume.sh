#!/bin/sh

while read line
do
    diskUtil coreStorage unlockVolume $1 -passphrase $line 2>&1 > /dev/null
    if [[ $? == 0 ]]; then
        echo "it was " $line
    fi
done < /dev/stdin
