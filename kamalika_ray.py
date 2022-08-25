import pandas as pd
import sys
import networkx as nx
import matplotlib.pyplot as plt

#e) Load the “gene_disease_opt.csv”
input_file = sys.argv[1]
df = pd.read_csv(input_file, sep='\t', index_col=False) 
associations = df[["score", "disease.name", 'gene_family']]

#f) Group the associations based on “gene_family” and use 0.4 as cut off on “score column to create a new logical variable called “selected”. Then find top 5 associated diseases that are above the cut off in each gene family and save it as a “selected_associations.csv” file in the /output folder. Plot a stacked bar plot of the associate per gene family using “selected” column.

selected = associations.loc[associations["score"] >= 0.4 ]
sorted_selected = selected.sort_values(['score'],ascending=False).groupby('gene_family')
selected_associations = sorted_selected[["score", "disease.name", 'gene_family']].head(5)
selected_associations.to_csv("output/selected_associations.csv", index=False)
new_table = pd.pivot_table(data=selected, index=['gene_family'], columns=['disease.name'], values='score')
ax1 = new_table.plot.bar(stacked=True, figsize=(30, 30))
ax1.set_title('Plot for selected column', fontsize=20)
ax1.legend(bbox_to_anchor=(1.0, 1.0))
fig1 = ax1.get_figure()
fig1.savefig('graphics/selected_stackedbar_plot.pdf')

#g) Find how many associations are based on studies published after 2020, then assess if there is any of the records carry missense variants (Hint. Use “publicationYear” and “variantFunctionalConsequence.label” columns).

no_of_studies_after2020 = df.loc[df["publicationYear"] > 2020 ]
print ("No. of associations that are based on studies published after 2020: ", len(no_of_studies_after2020))
missense_variant_studies = no_of_studies_after2020.loc[no_of_studies_after2020["variantFunctionalConsequence.label"] == "missense_variant"]
print ("No. of records carrying missense variants: ", len(missense_variant_studies))

#i) Write an R function (Python method) to take the data as input and returns the sorted list of variant ids and their corresponding score as a indexed matrix.
sorted_list = df.sort_values(['variantId'],ascending=True).reset_index()
sorted_list[['variantId', 'score']].to_csv("output/sorted_variantId.csv")

#h) Plot the distribution of the association scores and color them based on gene family and save it into /graphics/score_dst.pdf
ax2 = df.pivot(columns='gene_family', values='score').plot.hist(logy=True, alpha=0.4)
ax2.set_title('Distribution of scores per gene family', fontsize=20)
ax2.set_xlabel('Score')
fig2 = ax2.get_figure()
fig2.savefig('graphics/score_dst.pdf')

#j) Create a network plot of all gene disease associations and map the scores to the edges. Color the nodes based on if they are gene or disease. Save the Network plot in /graphics/gene_disease_ntw.pdf
plt.clf()
network_data = df[['target.approvedSymbol', 'disease.name', 'score']]
G = nx.from_pandas_edgelist(network_data, source = 'target.approvedSymbol', target = 'disease.name', edge_attr = 'score')
color_map = ['red' if node in df['target.approvedSymbol'].values else 'blue' for node in G]
pos = nx.spring_layout(G)
nx.draw(G, node_color=color_map, node_size = 5, font_size=3, pos = pos)
plt.title("Gene Disease Association Network")
plt.savefig("graphics/gene_disease_ntw.pdf")


