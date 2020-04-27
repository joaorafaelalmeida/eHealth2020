class Orchestrator():
	def process(vocabularies, dataset):
		"""
		Manage the request to process the text using different methodologies. 
		At the end, it returns a divt with the results of each methodology defined in the system.
		Loads the vocabularies into an dictionary with the following format:
		:param vocabularies: Dict with the vocabularies. 
			Format: {"diagnosis":{"code":(spanish definition, english definion), ...}, ...}
		:param dataset: Dict with the clinical notes in both languages.
			Format: {"es":{"note id":"text", ...}, "en":{"note id":"text", ...}}
		:return: The dict results 
			Format: {"Method A": {"note id": [(observation type", "code", "term", "span"), ...], ...}, ...}
		"""
		results = {"rule-based": {}}
		results["rule-based"] = Orchestrator.ruledBased(vocabularies, dataset)
		#...
		return results

	def ruledBased(vocabularies, dataset):
		return {"note id": [("DIAGNOSTICO", "codeDD", "teste as", "12 15"), ("PROCEDIMIENTO", "codePP", "tasdadfeste as", "123 155")]}