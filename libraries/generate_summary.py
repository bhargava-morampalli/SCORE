# -------------------------------
# Title: generate_summary.py
# Author: Silver A. Wolf
# Last Modified: Thur, 15.08.2019
# Version: 0.0.6
# -------------------------------

# Imports
from Bio.Seq import Seq
import argparse
import csv

def break_gene(sequence):
	base_count = 0
	new_sequence_list = ""
	for base in sequence:
		if base_count == 59:
			new_sequence_list = new_sequence_list + base + "\n"
			base_count = 0
		else:
			new_sequence_list = new_sequence_list + base
			base_count += 1
	return(sequence)
				
def create_summary_file(ffn_file, genetic_code, metadata_file):
	conditions = []
	with open(metadata_file) as tsv:
		for line in csv.reader(tsv, delimiter = "\t"):
			if line[0][0] != "@":
				conditions.append(line[1])
	genes_downregulated = open("deg/genes_downregulated.fasta", "w")
	genes_neutral = open("deg/genes_neutral.tsv", "w")
	genes_upregulated = open("deg/genes_upregulated.tsv", "w")
	summary_file = open("deg/summary.tsv", "w")
	with open("deg/diffexpr_results_all.csv") as diffexpr_full_results:
		for diffexpr_line in csv.reader(diffexpr_full_results, delimiter = ","):
			id = diffexpr_line[0]
			if id == "":
				summary_file.write("ID\tgene name\tproduct\tlog2FC\tDE (SCORE) (-1: " + conditions[0] + " > " + conditions[4] + "; 1: " + conditions[4] + " >" + conditions[0] + ")\tcorrected p-value (baySeq)\tcorrected p-value (DESeq2)\tcorrected p-value (edgeR)\tcorrected p-value (limma)\tcorrected p-value (NOISeq)\tcorrected p-value (sleuth)\t" + conditions[0] + "\t" + conditions[4] + "\tnucleotide sequence\tAA sequence\n")
			else:
				deg = "0"
				nucleotide_sequence = ""
				p_value_bayseq = str(round(float(diffexpr_line[1]), 4))
				p_value_deseq2 = diffexpr_line[2]
				if p_value_deseq2 == "NA":
					p_value_deseq2 = "1"
				else:
					p_value_deseq2 = str(round(float(p_value_deseq2), 4))
				p_value_edger = str(round(float(diffexpr_line[3]), 4))
				p_value_limma = str(round(float(diffexpr_line[4]), 4))
				p_value_noiseq = diffexpr_line[5]
				if p_value_noiseq == "NA":
					p_value_noiseq = "1"
				else:
					p_value_noiseq = str(round((1 - float(p_value_noiseq)), 4))
				p_value_sleuth = diffexpr_line[6]
				if p_value_sleuth == "NA":
					p_value_sleuth = "1"
				else:
					p_value_sleuth = str(round(float(p_value_sleuth), 4))
				read_gene = False
				with open("deg/filtered_gene_counts_presence_absence_matrix.csv") as presence_absence_file:
					for presence_absence_line in csv.reader(presence_absence_file, delimiter = ","):
						if id == presence_absence_line[0]:
							gene_name = presence_absence_line[1]
							product = presence_absence_line[2]
							if int(presence_absence_line[3]) + int(presence_absence_line[4]) + int(presence_absence_line[5]) > 1:
								presence_absence_condition_1 = "1"
							else:
								presence_absence_condition_1 = "0"
							if int(presence_absence_line[6]) + int(presence_absence_line[7]) + int(presence_absence_line[8]) > 1:
								presence_absence_condition_2 = "1"
							else:
								presence_absence_condition_2 = "0"						
							break
				with open("deg/diffexpr_results_limma.csv") as limma_results:
					for limma_line in csv.reader(limma_results, delimiter = ","):
						if id == limma_line[0]:
							fold_change = str(round(float(limma_line[1]), 4))
							break
				with open("deg/consensus_diffexpr_results_extended.csv") as deg_file:
					for deg_line in csv.reader(deg_file, delimiter = ","):
						if id == deg_line[0]:
							if float(fold_change) > 0:
								deg = "1"
							elif float(fold_change) < 0:
								deg = "-1"
							else:
								deg = "0"
							break
				with open(ffn_file) as fasta_file:
					for line in fasta_file:
						if id in line:
							read_gene = True
						else:
							if read_gene == True:
								if line[0] == ">":
									break
								else:
									nucleotide_sequence = nucleotide_sequence + line.strip()
				nucleotide_sequence_biopython = Seq(nucleotide_sequence)
				aa_sequence = str(nucleotide_sequence_biopython.translate(table = genetic_code))
				summary_file.write(id + "\t" + gene_name + "\t" + product + "\t" + fold_change + "\t" + deg + "\t" + p_value_bayseq + "\t" + p_value_deseq2 + "\t" + p_value_edger + "\t" + p_value_limma + "\t" + p_value_noiseq + "\t" + p_value_sleuth + "\t" + presence_absence_condition_1 + "\t" + presence_absence_condition_2 + "\t" + nucleotide_sequence + "\t" + aa_sequence + "\n")
				
				gene_edit = break_gene(nucleotide_sequence)
				
				if deg == "-1":
					genes_downregulated.write("> " + id + "\n" + gene_edit + "\n")
				
				elif deg == "1":
					genes_upregulated.write("> " + id + "\n" + gene_edit + "\n")
					
				else:
					genes_neutral.write("> " + id + "\n" + gene_edit + "\n")

	genes_downregulated.close()
	genes_neutral.close()
	genes_upregulated.close()
	summary_file.close()
	
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description = "")
	parser.add_argument("-f", "--fasta_file", type = str, default = "references/REF.ffn", required = False, help = "FFN file in Fasta format")
	parser.add_argument("-g", "--genetic_code", type = str, default = "11", required = False, help = "NCBI Identifier for the Genetic Code (organism specific)")
	parser.add_argument("-m", "--metadata_table", type = str, default = "raw/Metadata.tsv", required = False, help = "The Metadata table used for the analysis")
	args = parser.parse_args()
	
	create_summary_file(args.fasta_file, args.genetic_code, args.metadata_table)