class RuleBased():
	def process(vocabularies, dataset, gs):
		"""
		Method based on rules learn from the train dataset.
		:param vocabularies: Dict with the vocabularies. 
			Format: {"diagnosis":{"code":(spanish definition, english definion), ...}, ...}
		:param dataset: Dict with the clinical notes in both languages.
			Format: {"es":{"note id":"text", ...}, "en":{"note id":"text", ...}}
		:param gs: Dict with the goldstandard (train or train and dev).
			Format: {"term":"id"}
		:return: The dict results 
			Format: {"note id": [("obsType", "code", "span"), ...], ...}
		"""

		results = {}
		for docId in dataset["es"]:
			results[docId] = []
			note =  dataset["es"][docId]
			note = note.replace(".", " ")
			for term in gs:
				spanStart = note.find(term)
				if spanStart >= 0:#muito incompleto
					span = "{} {}".format(spanStart, spanStart+len(term))
					results[docId] += [(gs[term][1], gs[term][0], span)]
		return results
