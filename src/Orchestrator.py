from RuleBased import RuleBased
from FileManager import FileManager

class Orchestrator():
	def process(datasetType, vocabularies, dataset, settings):
		"""
		Manage the request to process the text using different methodologies. 
		At the end, it returns a divt with the results of each methodology defined in the system.
		Loads the vocabularies into an dictionary with the following format:
		:param datasetType: String indicating the dataset to be processed (Train, Dev or Test)
		:param vocabularies: Dict with the vocabularies. 
			Format: {"diagnosis":{"code":(spanish definition, english definion), ...}, ...}
		:param dataset: Dict with the clinical notes in both languages.
			Format: {"es":{"note id":"text", ...}, "en":{"note id":"text", ...}}
		:param settings: Global settings read from the file.
		:return: The dict results 
			Format: {"Method A": {"note id": [(observation type", "code", "term", "span"), ...], ...}, ...}
		"""
		results = {"rule-based": {}}
		results["rule-based"] = Orchestrator.ruledBased(datasetType, vocabularies, dataset, settings)
		#...
		return results

	def ruledBased(datasetType, vocabularies, dataset, settings):
		results = None
		if "dev" in datasetType:
			gsTrain = Orchestrator.mergeAngGetUniquesGS(FileManager.readGSX(settings["train"]["gs-t3"]))
			results = RuleBased.process(vocabularies, dataset, gsTrain)
		elif "test" in datasetType:
			gsTrain = FileManager.readGSX(settings["train"]["gs-t3"])
			gsDev = FileManager.readGSX(settings["dev"]["gs-t3"])
			bothGS = Orchestrator.mergeAngGetUniquesGS(gsTrain, gsDev)
			results = RuleBased.process(vocabularies, dataset, bothGS)
		else:
			print("RuledBased: Nothing implemented")
		return results
		#procce if diagnosito ou outro
		#return {"S0004-06142005000700014-1": [("DIAGNOSTICO", "n44.8", "teste as", "12 15"), ("PROCEDIMIENTO", "bw03zzz", "Rx tórax", "2163 2171")]}
	
	def mergeAngGetUniquesGS(gsTrain, gsDev=None):
		if gsDev:
			print("TODO")
		gs = gsTrain
		tmpGS = {}
		for term in gs:
			code = [k for k, v in sorted(gs[term].items(), key=lambda item: item[1])][-1]
			tmpGS[term] = code
		return tmpGS