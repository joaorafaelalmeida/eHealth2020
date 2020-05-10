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
		results["rule-based"] = Orchestrator.ruledBased(datasetType, vocabularies, dataset, settings, "BOTH")
		results["rule-basedD"] = Orchestrator.ruledBased(datasetType, vocabularies, dataset, settings, "DEV")
		results["rule-basedT"] = Orchestrator.ruledBased(datasetType, vocabularies, dataset, settings, "TRAIN")
		results["rule-basedTLim4"] = Orchestrator.ruledBased(datasetType, vocabularies, dataset, settings, "TRAIN", 4)
		results["rule-basedLim4"] = Orchestrator.ruledBased(datasetType, vocabularies, dataset, settings, "BOTH", 4)

		#...
		return results

	def ruledBased(datasetType, vocabularies, dataset, settings, gs, lim=0):
		results = None
		if "dev" in datasetType:
			gsTrain = Orchestrator.mergeAngGetUniquesGS(lim, FileManager.readGSX(settings["train"]["gs-t3"]))
			results = RuleBased.process(vocabularies, dataset, gsTrain)
		elif "test" in datasetType:
			gsTrain = FileManager.readGSX(settings["train"]["gs-t3"])
			gsDev = FileManager.readGSX(settings["dev"]["gs-t3"])
			if gs == "DEV":
				gsTrain = dict(gsDev)
				gsDev = None
			elif gs == "TRAIN":
				gsDev = None
			bothGS = Orchestrator.mergeAngGetUniquesGS(lim, gsTrain, gsDev)
			results = RuleBased.process(vocabularies, dataset, bothGS)
		else:
			print("RuledBased: Nothing implemented")
		return results
		#procce if diagnosito ou outro
		#return {"S0004-06142005000700014-1": [("DIAGNOSTICO", "n44.8", "teste as", "12 15"), ("PROCEDIMIENTO", "bw03zzz", "Rx tórax", "2163 2171")]}
	
	def mergeAngGetUniquesGS(lim, gsTrain, gsDev=None):
		gs = dict(gsTrain)
		if gsDev != None:
			for term in gsDev:
				if term not in gs:
					gs[term] = gsDev[term]
				else:
					for concept in gsDev[term]:
						if concept not in gs[term]:
							gs[term][concept] = gsDev[term][concept]
						else:
							gs[term][concept] += gsDev[term][concept]
		if lim != 0:
			allTmpGS = dict(gs)
			gs = {}
			for term in allTmpGS:
				for concept in allTmpGS[term]:
					if allTmpGS[term][concept] > lim:
						if term not in gs:
							gs[term] = {}
						gs[term][concept] = allTmpGS[term][concept] 
		print(len(gs))

		tmpGS = {}
		for term in gs:
			code = [k for k, v in sorted(gs[term].items(), key=lambda item: item[1])][-1]
			tmpGS[term] = code
		return tmpGS