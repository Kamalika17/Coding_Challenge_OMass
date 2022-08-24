#!/bin/sh
inputfile=$1
date -r $inputfile
var1="$(head -n 1 $inputfile)"
for v in $var1
    do 
       echo $v
    done

var2="$(awk '{print $--NF}' $inputfile)"
count=0
for v1 in $var2
    do
	if [[ $v1 == '"GPCR"' ]]
        then
           ((count=count+1))
	fi
    done
echo $count

records="$(grep "SLC15A4" $inputfile)"
echo $records | sed 's/NA/0/g' > gene_disease_opt_new.csv
