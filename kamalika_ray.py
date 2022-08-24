# Answers for (e),(f),(g)

filename = open("gene_disease_opt.csv")
dict_gf = {}
dict_score = {}
count = 0
pubsafter2020 = 0
fr = open('records_of_missense_variants_published_after_2020.csv','w')
for line in filename:
	count += 1
	if count == 1:
		continue
	cols = line.strip().split("\t")
	genefamily = cols[-2]
	score = float(cols[0])
	disease = cols[-4]
	pubyear = int(cols[3])
	variant = cols[-3]
	# Find how many associations are based on studies published after 2020, then assess if there is any of the records carry missense variants
	if pubyear > 2020:
		pubsafter2020 += 1
		if variant == '"missense_variant"':
			fr.write(line.strip()+"\n")	 
        #grouping by gene_family and using score cutoff of 0.4
	if not float(cols[0]) >= 0.4:
		continue
	if genefamily not in dict_gf:
		dict_gf[genefamily] = []
	if score not in dict_score:
		dict_score[score] = []
	dict_gf[genefamily].append(score)
	dict_score[score].append(disease)

for key,value in dict_gf.items():
	dict_gf[key].sort(reverse=True)
fw = open('selected_associations.csv', 'w')
for key in dict_gf.keys():
	c = 0
	for s in dict_gf[key]:
		c += 1
		fw.write(key.strip()+","+dict_score[s][0].strip()+","+str(s)+"\n")
		if c > 5:
			break
fw.close()
fr.close()
filename.close()
print("Number of associations after 2020: "+str(pubsafter2020))
