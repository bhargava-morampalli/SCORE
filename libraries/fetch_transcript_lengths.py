# -------------------------------
# Title: fetch_transcript_lengths
# Author: Silver A. Wolf
# Last Modified: Thur, 25.07.2019
# Version: 0.0.7
# -------------------------------

# Imports
import argparse
import csv

def fetch_lengths(gff, id):
	id = id + "="
	output_lengths = open("deg/transcript_lengths.csv", "w")
	output_lengths.write("Transcript ID,Length\n")
	with open(gff) as full_gff_file:
		for line in csv.reader(full_gff_file, delimiter = "\t"):
			if len(line) > 0:
				if line[0][0] != "#" and id in line[8]:
					transcript_length = abs(int(line[3]) - int(line[4]))
					transcript_id = line[8].split(id)[1].split(";")[0]
					output_lengths.write(transcript_id + "," + str(transcript_length) + "\n")
	output_lengths.close()
	
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "")
    parser.add_argument("-f", "--annotation_file", type = str, default = "references/human_transduced/PROKKA_07132018.gff", required = False, help = "Annotation GFF file")
    parser.add_argument("-i", "--annotation_identifier", type = str, default = "locus_tag", required = False, help = "Identifier used in the GFF file")
    args = parser.parse_args()

    fetch_lengths(args.annotation_file, args.annotation_identifier)