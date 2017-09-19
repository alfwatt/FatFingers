#!/bin/sh

while read line
do
    diskUtil coreStorage unlockVolume $1 -passphrase $line > /dev/null
    if [[ $? == 0 ]]; then
        echo "it was " $line
    fi
done < /dev/stdin
