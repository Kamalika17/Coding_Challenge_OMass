#!/bin/sh
inputfile=$1 # Requires input as command-line argument

#a) Prints the date and the column names of the file (Hint- use new line for printing the column names).
date -r $inputfile
head -n 1 $inputfile | tr '\t' '\n'

#b) Prints the following line “Number of the GPCRs:” with number of the records in the file that belong to the GPCR family (Hint: use the “gene_family” column information)
awk '{print $--NF}' $inputfile | grep "GPCR" | wc -l

#c) Finds all the records for the gene “SLC15A4” and replaces all the NA with 0 and saves it to the new file named “gene_disease_opt_new.csv” in the “/output/” and prints the number of the records to the terminal.
grep "SLC15A4" $inputfile | sed 's/NA/0/g' | tee 'output/gene_disease_opt_new.csv' | wc -l
