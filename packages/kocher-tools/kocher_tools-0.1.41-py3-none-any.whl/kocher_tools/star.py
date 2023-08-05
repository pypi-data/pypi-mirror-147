#!/usr/bin/env python
import os
import sys
import yaml
import copy
import logging
import subprocess
import multiprocessing

from kocher_tools.misc import confirmExecutable
from genome import Genome

class STAR ():
	def __init__ (self, **kwargs):

		# Confirm the STAR executable is installed
		self._executable_path = confirmExecutable('STAR')
		if not self._executable_path: raise IOError('STAR not found. Please confirm the executable is installed')
		self.version = self.call(['--version'], return_stdout = True)

	def call (self, star_call_args, return_stdout = False):

		# STAR subprocess call
		star_call = subprocess.Popen([self._executable_path] + star_call_args, stderr = subprocess.PIPE, stdout = subprocess.PIPE)

		# Get stdout and stderr from subprocess
		star_stdout, star_stderr = star_call.communicate()

		# Convert bytes to string, if needed
		if sys.version_info[0] == 3:
			star_stdout = star_stdout.decode()
			star_stderr = star_stderr.decode()

		# Check the stderr for errors
		self._checkForErrors(star_stderr)

		if return_stdout: return star_stdout.strip()

	@staticmethod
	def _checkForErrors (star_stderr):

		# Check if the stderr is empty
		if not star_stderr: return

		print(star_stderr)

		'''
		# Report the error
		raise Exception(star_stderr)
		'''

def genomeGenerate (genome_fasta_list, genome_dir = '', out_path_prefix = '', path_hierarchy = ['basic'], ram_limit = None, threads = None, **kwargs):

	# Initialize STAR
	star_method = STAR()

	# Check if the genome directory is defined
	if genome_dir: path_hierarchy = ['defined']

	# Check that the path hierarchy won't result in errors
	if len(genome_fasta_list) > 1 and not set(path_hierarchy) & set(['method', 'species', 'joined']):
		raise Exception (f'Defined path hierarch incompatible with more than one genome: {path_hierarchy}')

	# Create the argument list and assign the run mode to genomeGenerate
	genomes_generate_call_args = ['--runMode', 'genomeGenerate']

	# Assign the basic arguments for genomeGenerate
	if ram_limit: genomes_generate_call_args.extend(['--limitGenomeGenerateRAM', str(ram_limit)])
	if threads: genomes_generate_call_args.extend(['--runThreadN', str(threads)])

	'''
	Assign the genomeGenerate-specific arguments
	1) The input genome
	2) The output directory
	3) The index length
	'''
	for genome_fasta in genome_fasta_list:

		# Create a copy of the call args for the current genome
		genome_generate_call_args = genomes_generate_call_args.copy()	

		# Read in the genome
		genome = Genome.readFASTA(genome_fasta)

		# Read in FASTA if not compressed. If compressed, assign/Create a decompressed FASTA
		if not genome.is_compressed: genome_generate_call_args.extend(['--genomeFastaFiles', genome_fasta])
		else: genome_generate_call_args.extend(['--genomeFastaFiles', genome.getDecompressedFile()])
		
		# Build the output path hierarchy by type
		out_path_list = [out_path_prefix]
		for path_type in path_hierarchy:
			if path_type == 'method': out_path_list.append(f'STAR_{star_method.version}_Index')
			elif path_type == 'species': out_path_list.append(genome.speciesCode())
			elif path_type == 'joined': out_path_list.append(f'{genome.speciesCode()}_STAR_{star_method.version}_Index')
			elif path_type == 'basic': out_path_list.append('STAR_Index')
			elif path_type == 'defined': out_path_list.extend(genome_dir.split(os.sep))
			else: raise Exception(f'Unknown type in path hierarchy: {path_type}')

		# Define the output path
		out_path = os.path.join(*out_path_list)

		# Assign the output directory
		genome_generate_call_args.extend(['--genomeDir', out_path])

		# Assign the index length
		genome_generate_call_args.extend(['--genomeSAindexNbases', str(genome.calcGenomeSAindexNbases())])

		# Generate the STAR index
		#star_method.call(genome_generate_call_args)

		# Create the genome info yaml
		genome_info_dict = {'FASTA': os.path.abspath(genome_fasta), 'Species_Code': genome.speciesCode(), 'STAR_Version': star_method.version}		
		with open(os.path.join(out_path, f'genome_info.yaml'), 'w') as genome_info_yaml:
			yaml.dump(genome_info_dict, genome_info_yaml)

		# Close the genome
		genome.close()


def alignReads (fastq_list, genome_dir, out_file_prefix = '', out_path_prefix = '', path_hierarchy = ['basic'], threads = None, sorted = True, **kwargs):

	# Initialize STAR
	star_method = STAR()

	# Confirm the fasta file(s) exists 
	for fastq in fastq_list:
		if not os.path.isfile(fastq): raise IOError(f'{fastq} does not exist')

	# Check if the file(s) are compressed
	gzip_compressed = [_fq.endswith('.gz') for _fq in fastq_list]
	if len(set(gzip_compressed)) == 1: gzip_compressed = gzip_compressed[0]
	else: raise Exception(f'FASTQ Compression inconsistent: {fastq_list}')

	# Create the argument list and assign the run mode to alignReads
	align_reads_call_args = ['--runMode', 'alignReads']

	# If compressed, add the argument to the list
	if gzip_compressed: align_reads_call_args.extend(['--readFilesCommand', 'zcat'])

genomeGenerate([sys.argv[1]], path_hierarchy = ['species', 'method'], ram_limit = '24000000000', threads = 20)
#alignReads([sys.argv[1]], '', path_hierarchy = ['species', 'method'], ram_limit = '24000000000', threads = 20)


'''
--runThreadN 10 --runMode genomeGenerate --genomeDir STAR/LCAL_Index --genomeFastaFiles STAR/LCAL_Index/LCAL_genome
_v2.1.1.fasta --limitGenomeGenerateRAM 38000000000 --genomeSAindexNbases 13

--runThreadN 8 --runMode alignReads --genomeDir /Genomics/kocherlab/lab/STAR_Genomes/official_release_v2.1.1/AAUR_I
ndex/ --outSAMtype BAM Unsorted --outFileNamePrefix AAUR_STAR/AA_12_brain. --readFilesCommand zcat --readFilesIn AAUR_Fi
ltered/AA_12_brain_R1.filtered.fq.gz AAUR_Filtered/AA_12_brain_R2.filtered.fq.gz
'''