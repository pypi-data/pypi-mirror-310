import logging
import os.path
import subprocess
from Bio import SeqIO
import regex


def run_external(cmd, keep_stdout=False, keep_stderr=True):
	logger = logging.getLogger("main")
	logger.debug("Running: %s", " ".join(cmd))
	stderr_dest = subprocess.PIPE if keep_stderr else subprocess.DEVNULL
	stdout_dest = subprocess.PIPE if keep_stdout else subprocess.DEVNULL

	try:
		r = subprocess.run(cmd, stderr=stderr_dest, stdout=stdout_dest,
			check=True, encoding="utf-8")
		return r
	except subprocess.CalledProcessError as e:
		logger.error("Error during run of \"%s\"", e.cmd)
		logger.error("stderr message:")
		logger.error(e.stderr)
		raise e


def check_files(file_list):
	for x in file_list:
		if not os.path.isfile(x):
			logging.error("Input file not found: %s", x)
			raise FileNotFoundError(x)


def write_records_to_fasta(records, path, glue=False):
	'''Return path to FASTA or None'''
	logger = logging.getLogger()
	with open(path, "w") as f:
		if not glue:
			for record in records:
				SeqIO.write(record, f, 'fasta')
		else:
			pattern = regex.compile(r'^(.+)_frag_(\d+)$')
			prev_rec = next(records)
			m0 = pattern.match(prev_rec.id)
			if m0:
				prev_cont = m0.group(1)
				prev_n = int(m0.group(2))
			else:
				prev_cont = prev_rec.id
				prev_n = -127
			for record in records:
				m = pattern.match(record.id)
				if m:
					contig = m.group(1)
					n = int(m.group(2))
					if contig != prev_cont:
						prev_rec.id = f"{prev_cont}_{prev_n}"
						prev_rec.description = ''
						SeqIO.write(prev_rec, f, 'fasta')
						prev_cont = contig
						prev_rec = record
					else:
						if n == prev_n + 1:
							prev_rec += record
						else:
							prev_rec.id = f"{prev_cont}_{prev_n}"
							prev_rec.description = ''
							SeqIO.write(prev_rec, f, 'fasta')
							prev_cont = contig
							prev_rec = record
					prev_n = n
				else:
					prev_rec.id = prev_cont
					prev_rec.description = ''
					SeqIO.write(prev_rec, f, 'fasta')
					prev_cont = record.id
					prev_rec = record
			SeqIO.write(prev_rec, f, 'fasta')

		logger.debug("Sequences had been written to: %s", path)
		return path
	return None
