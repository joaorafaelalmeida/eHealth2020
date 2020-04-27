import codecs
import glob
import os

class FileManager():
	def loadVocabularies(vocabulariesPaths):
		"""
		Loads the vocabularies into an dictionary
		:param vocabulariesPaths: location of all files composing the vocabularies
		:return: The dict tmpVoc.
			Format: {"diagnosis":{"code":(spanish definition, english definion), ...}, ...}
		"""
		tmpVoc = {}
		for voc in vocabulariesPaths:
			if voc not in tmpVoc:
				tmpVoc[voc] = {}
			with codecs.open(vocabulariesPaths[voc], 'r', encoding='utf8') as fp:
				for line in fp:
					line = line.strip().split("\t")
					if len(line) == 3:
						tmpVoc[voc][line[0]] = (line[1],line[2])
		return tmpVoc

	def readDataset(datasetDir):
		"""
		Loads the clinical notes into an dictionary
		:param datasetDir: location of all files related with the dataset (text_files and text_files_en directories)
		:return: The dict dataset.
			Format: {"es":{"note id":"text", ...}, "en":{"note id":"text", ...}}
		"""
		dataset = {"es":{}, "en":{}}
		for directory in datasetDir:
			allFiles = glob.glob('{}*.{}'.format(datasetDir[directory], "txt"))
			for file in allFiles:
				noteId = file.split("/")[-1].split(".")[0]
				with codecs.open(file, 'r', encoding='utf8') as fp:
					note = FileManager.cleanFile(fp.read())
				if "/text_files/" in datasetDir[directory]: #Spanish notes
					dataset["es"][noteId] = note
				if "/text_files_en/" in datasetDir[directory]: #English notes
					dataset["en"][noteId] = note
		return dataset

	def cleanFile(file):
		"""
		Cleans the clinical notes text
		:param file: the readed text
		:return file: the clean text
		"""
		file = file.replace("\n", " ").replace("’", "\'")
		for ch in ['\\','\"','*','_','{','}','[',']','(',')','>','#','+',',','!','$',':',';']:
				if ch in file:
					file = file.replace(ch,"")
		#file = file.lower()
		return file

	def writeResults(directory, results):
		"""
		Writes the results for the 3 sub-tasks
		:param directory: Location to write the results. It aggregates by sub-tasks.
		:param results: Dict with the annotation from all the methods developed. 
			Format: {"Method A": {"note id": [(observation type", "code", "term", "span"), ...], ...}, ...}
		"""
		if not os.path.exists(directory["t1"]):
			os.makedirs(directory["t1"])
		if not os.path.exists(directory["t2"]):
			os.makedirs(directory["t2"])
		if not os.path.exists(directory["t3"]):
			os.makedirs(directory["t3"])
		for method in results:
			outD = open("{}{}_testD.tsv".format(directory["t1"], method), "w")
			outP = open("{}{}_testP.tsv".format(directory["t2"], method), "w")
			outX = open("{}{}_testX.tsv".format(directory["t3"], method), "w")
			for noteID in results[method]:
				for obsType, code, term, span in results[method][noteID]:
					if "DIAGNOSTICO" in obsType:
						outD.write("{}\t{}\n".format(noteID, code))
					elif "PROCEDIMIENTO" in obsType:
						outP.write("{}\t{}\n".format(noteID, code))
					else:
						print("BUG!")
					outX.write("{}\t{}\t{}\t{}\n".format(noteID, span, obsType, code))
			outD.close()
			outP.close()
			outX.close()
		