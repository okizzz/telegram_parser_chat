#!/usr/bin/env bash

#-------------config-------------#
Day=01 #last day online
Month=02 #last Month online
Year=2019 #last Year online
#-------------config-------------#

Act_Day=$(date +%d)
Act_Month=$(date +%m)

function search_users(){
    echo "Last online status:" ${Day}-${Month}-${Year}
    while [ ${Day} -le ${Act_Day} ]
    do
    cat *_users.txt | grep -v 'None' | awk '{print $1}' >> dump_users.txt
    Day=$[Day+1]
    done
}
function sort_users(){
    uniq dump_users.txt > sort_users.txt
    quantity=$(cat sort_users.txt | wc -l)
    rm dump_users.txt
    echo "Work done! Quantity users:" ${quantity}
}
search_users
sort_users
