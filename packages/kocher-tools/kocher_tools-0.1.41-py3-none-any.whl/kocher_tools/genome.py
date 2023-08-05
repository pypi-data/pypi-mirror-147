import os
import sys
import gzip
import math
import yaml
import shutil

from Bio import SeqIO
from collections import defaultdict

class Genome ():
	def __init__ (self, genome_filename = '', genome_format = '', yaml_filename = '', **kwargs):

		# Check the files exists
		if not os.path.isfile(genome_filename): raise IOError(f'{genome_filename} does not exist')
		if yaml_filename and not os.path.isfile(yaml_filename): raise IOError(f'{yaml_filename} does not exist')

		if genome_filename.endswith('.gz'): yaml_filename = f'{os.path.basename(genome_filename)[:-3]}.yml'
		else: yaml_filename = f'{os.path.basename(genome_filename)}.yml'

		# Check the file format is defined
		if not genome_format: raise Exception(f'File format not defined')

		# Genome-based variables
		self._genome_filename = genome_filename
		self._genome_format = genome_format
		self.is_compressed = genome_filename.endswith('.gz')
		self._genome_decompress_filename = None

		# Genome statistics variables
		self._contig_lens = []
		self._attributes_updated = False
		self._attributes = {'contig_sum': 0,
							   'n_count': 0,
						       'n_stats': {'N10': '',
										   'N20': '',
										   'N30': '',
										   'N40': '',
										   'N50': '',
										   'N60': '',
										   'N70': '',
										   'N80': '',
										   'N90': ''}}

		# Assign the YAML filename, and read if it exists
		if yaml_filename: self._yaml_filename = yaml_filename
		else: self.assignYAMLFilename()
		self.readYAML()

	def sequenceParser (self, record_lens = False, record_sum = False, record_Ns = False):

		# Confirm if the parse is required
		if not any((record_lens, record_sum, record_Ns)): return

		# Read in the genome file
		if self._genome_filename.endswith('.gz'): genome_file = gzip.open(self._genome_filename, 'rt')
		else: genome_file = open(self._genome_filename, 'r')
		
		'''
		Multiple options that can be recorded:
		1) Record the length for each sequence - i.e. chromosome, contig
		2) Record the sum the sequences - i.e. chromosome, contig
		3) Count the number of N's
		4) Count the number of gaps elements (-)
		'''
		for seq_record in SeqIO.parse(genome_file, self._genome_format):
			seq_len = len(seq_record)
			if record_lens: self._contig_lens.append(seq_len)
			if record_sum: self._attributes['contig_sum'] += seq_len
			if record_Ns: self._attributes['n_count'] += seq_record.seq.count('N')
		
		# Once the file has been read, sort the contigs (if being recorded)
		if record_lens: self._contig_lens = sorted(self._contig_lens, reverse = True)

		# Report the attributes have been updated
		self._attributes_updated = True

	def nStatistics (self):

		# Assign the N statistic list
		n_statistics = [_ni for _ni in range(10, 100, 10) if self._attributes['n_stats'][f'N{_ni}'] == '']
		
		# Check if the N statistics have been calculated
		if not n_statistics: return

		# Collect the necessary sequence statistics
		self.sequenceParser(record_lens = not self._contig_lens, record_sum = not self._attributes['contig_sum'])

		# Assign the N statistic cutoffs
		n_cutoff_dict = {(self._attributes['contig_sum'] * (1 - (_ni / 100))):f'N{_ni}' for _ni in n_statistics}
		n_min_cutoff = min(list(n_cutoff_dict))
		
		# Create variables to store the sequence sum and counts
		n_sum = 0
		n_count = 0

		# Calc the N statistics
		for len_int in self._contig_lens:
			n_sum += len_int
			n_count += 1
			if n_sum >= n_min_cutoff:
				self._attributes['n_stats'][n_cutoff_dict[n_min_cutoff]] = [len_int, n_count]
				del n_cutoff_dict[n_min_cutoff]
				if not n_cutoff_dict: break
				else: n_min_cutoff = min(list(n_cutoff_dict))

		# Empty the contig lens
		self._contig_lens = []

		# Report the attributes have been updated
		self._attributes_updated = True

	def calcGenomeSAindexNbases (self):

		# Collect the necessary sequence sum
		self.sequenceParser(record_sum = not self._attributes['contig_sum'])

		# Return the value
		return min(14, int(math.log2(self._attributes['contig_sum'])/2 - 1))

	def speciesCode (self):

		'''
		Return the species code
		Current: Return the first four letters of the genome
		To Do: Update to use the database
		'''
		return os.path.basename(self._genome_filename)[:4]

	def getDecompressedFile (self):

		# Return the decompressed filename if already decompressed
		if self._genome_decompress_filename: return self._genome_decompress_filename

		# Decompress the file if not already decompressed
		self.decompressGenome()

		# Return the decompress filename
		return self._genome_decompress_filename

	def delDecompressedFile (self):

		# Delete the decompressed genome
		if self._genome_decompress_filename: 
			os.remove(self._genome_decompress_filename)
			self._genome_decompress_filename = None

	def decompressGenome (self):

		try:

			# Assign the decompressed filename
			self._genome_decompress_filename = self._genome_filename[:-3]

			# Check if the decompressed file already exists
			if os.path.isfile(self._genome_decompress_filename): return

			# Decompress the genome
			with gzip.open(self._genome_filename, 'rb') as compressed_genome:
				with open(self._genome_decompress_filename, 'wb') as decompressed_genome:
					shutil.copyfileobj(compressed_genome, decompressed_genome)
		
		except:
			raise Exception(f'Unable to decompress genome file: {self._genome_filename}')

	def assignYAMLFilename (self):

		# Define the YAML output dir using the genome filename
		yaml_dirname = os.path.dirname(self._genome_filename)

		# Define the YAML basename using the genome filename
		if self._genome_filename.endswith('.gz'): yaml_basename = f'{os.path.basename(self._genome_filename)[:-3]}.yml'
		else: yaml_basename = f'{os.path.basename(self._genome_filename)}.yml'
		
		# Assign the YAML filename
		self._yaml_filename = os.path.join(yaml_dirname, yaml_basename)

		# FOR TESTING, REMOVE WHEN DONE
		self._yaml_filename = yaml_basename

	def readYAML (self):

		# Assign the file, if needed 
		if not self._yaml_filename or not os.path.isfile(self._yaml_filename): return

		# Read the YAML file and load the attributes
		with open(self._yaml_filename, 'r') as file:
			self._attributes = yaml.full_load(file)

	def writeYAML (self):

		with open(self._yaml_filename, 'w') as yaml_file:
			yaml.dump(self._attributes, yaml_file)

	def close (self):

		# Check if the attributes have been updated
		if self._attributes_updated: self.writeYAML()

		# Check if a decompressed file was created
		if self._genome_decompress_filename: self.delDecompressedFile()

		# Clear the attributes
		self._contig_lens = []
		self._attributes = {'contig_sum': 0,
							   'n_count': 0,
						       'n_stats': {'N10': '',
										   'N20': '',
										   'N30': '',
										   'N40': '',
										   'N50': '',
										   'N60': '',
										   'N70': '',
										   'N80': '',
										   'N90': ''}}

	@classmethod
	def readFASTA (cls, genome_filename, **kwargs):
		return cls(genome_filename = genome_filename, genome_format = 'fasta', **kwargs)


#test = Genome.readFASTA(sys.argv[1])
#test.sequenceParser(record_sum = True, record_Ns = True)
#test.writeYAML()
