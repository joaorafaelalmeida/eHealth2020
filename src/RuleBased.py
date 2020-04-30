class RuleBased():
	def process(vocabularies, dataset):
		"""
		Method based on rules and stop word filtering using english dataset mixed with similarity search over spanish dataset 
		At the end, it returns a dict with the codes, location, and the clinical note id
		:param vocabularies: Dict with the vocabularies. 
			Format: {"diagnosis":{"code":(spanish definition, english definion), ...}, ...}
		:param dataset: Dict with the clinical notes in both languages.
			Format: {"es":{"note id":"text", ...}, "en":{"note id":"text", ...}}
		:return: The dict results 
			Format: {"note id": [("code", "span", "term"), ...], ...}
		"""
		results = {}
		newVoc = RuleBased.cleanEnglishVoc(vocabularies)
		# a ideia é ver o numero da frase, depois ir ao texto em espanhol 
		#e tentar fazer match das palavras pel referencia standard do voc em espanhol
		for docId in dataset["en"]:
			results[docId] = []
			note =  dataset["en"][docId]
			phraseID = 0
			for phrase in note.split("."):
				filteredPhrase = RuleBased.cleanStopWods(phrase)
				for voc in newVoc:
					if newVoc[voc][1] in filteredPhrase:
						span = RuleBased.getSpanishSpan(phraseID, dataset["es"][docId], voc, vocabularies, newVoc[voc][0].lower())
						results[docId] += [(newVoc[voc][0], voc, span)]
				phraseID += 1
		return results
		#return {"S0004-06142005000700014-1": [("DIAGNOSTICO", "n44.8", "teste as", "12 15"), ("PROCEDIMIENTO", "bw03zzz", "Rx tórax", "2163 2171")]}

	def cleanStopWods(text):
		newText = ""
		for word in text.split(" "):
			if word not in STOPWORDS:
				newText += word + " "
		return newText.lower()

	def cleanEnglishVoc(vocabularies):
		newVoc = {}
		for voc in vocabularies:
			for concept in vocabularies[voc]:
				newText = ""
				tempPhrase = vocabularies[voc][concept][1].split(" ")
				for word in tempPhrase:
					if word not in STOPWORDS:
						newText += word + " "
				newVoc[concept] = (voc.upper(), newText.lower())
		return newVoc

	def getSpanishSpan(phraseID, note, conceptID, vocabularies, obsType):
		"""
		Method to retrieve the span from the concept found.
		:param phraseID: The setence number
		:param note: The note in spanish
		:param conceptID: The concept ID found (diagnosis or procedure)
		:param vocabularies: Dict with the vocabularies. 
			Format: {"diagnosis":{"code":(spanish definition, english definion), ...}, ...}
		:return: The span values in string format. Ex: "10 15;18 24"
		"""
		phrases = note.split(".")
		if phraseID >= len(phrases):
			return None
		before = 0
		count = 0
		for p in phrases:
			if count < phraseID:
				before += len(p) + 1
			else: 
				break
		phrase = phrases[phraseID]
		conceptDefES = vocabularies[obsType][conceptID][0]
		for x in conceptDefES.split(" "):
			span = RuleBased.findStr(phrase, x)
			if span != -1:
				return "{} {}".format(before+span, before+span+len(x)-1)
		return None

	def findStr(s, char):
		index = 0		   
		if char in s:
			char = char[0]
			for ch in s:
				if ch in s:
					index += 1
				if ch == char:
					return index
		else:
			return -1

STOPWORDS = set(["future",
	"'ll", "'ve", '0o', '0s', '3a', '3b', '3d', '6b', '6o', 'A', 'B', 'C', 'D', 'E', 
	'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
	'Y', 'Z', 'a', "a's", 'a1', 'a2', 'a3', 'a4', 'ab', 'able', 'about', 'above', 'abst', 'ac',
	'accept', 'accepted', 'accordance', 'according', 'accordingly', 'across', 'act', 'actually',
	'ad', 'add', 'added', 'adj', 'advised', 'ae', 'af', 'affected', 'affecting', 'affects', 
	'after', 'afternoon', 'afterwards', 'ag', 'again', 'against', 'age', 'ages', 'agree', 'arise',
	'agreed', 'ah', 'ain', "ain't", 'aj', 'al', 'all', 'allow', 'allowed', 'allows', 'almost',
	'alone', 'along', 'already', 'also', 'although', 'always', 'am', 'among', 'amongst', 'argued',
	'amoungst', 'amount', 'an', 'ancestry.', 'and', 'announce', 'another', 'any', 'anybody', 
	'anyhow', 'anymore', 'anyone', 'anything', 'anyway', 'anyways', 'anywhere', 'ao', 'ap', 
	'apart', 'apparently', 'appear', 'appeared', 'appears', 'appreciate', 'appropriate', 'around',
	'approximately', 'apr', 'april', 'ar', 'are', 'aren', "aren't", 'arent', 'argue', 'arrange', 
	'arranged', 'arrive', 'arrived', 'as', 'aside', 'ask', 'asked', 'asking', 'associated', 'at', 
	'ate', 'attempts', 'au', 'aug', 'august', 'auth', 'av', 'available', 'aw', 'away', 'awfully', 
	'ax', 'ay', 'az', 'b', 'b1', 'b2', 'b3', 'ba', 'back', 'base', 'based', 'bc', 'bd', 'be', 
	'bear', 'beat', 'beaten', 'became', 'because', 'become', 'becomes', 'becoming', 'been', 
	'before', 'beforehand', 'began', 'begin', 'beginning', 'beginnings', 'begins', 'begun', 
	'behind', 'being', 'believe', 'believed', 'believes', 'below', 'bend', 'bent', 'beside', 
	'besides', 'best', 'better', 'between', 'beyond', 'bi', 'bill', 'biol', 'bj', 'bk', 'bl', 
	'blew', 'blow', 'blown', 'bn', 'bore', 'born', 'borne', 'both', 'bottom', 'bought', 'bp', 'br', 
	'break', 'brief', 'briefly', 'bring', 'brought', 'bs', 'bt', 'bu', 'build', 'built', 'but', 
	'buy', 'bx', 'by', 'c', "c'mon", "c's", 'c1', 'c2', 'c3', 'ca', 'call', 'called', 'came', 
	'can', "can't", 'cannot', 'cant', 'carried', 'carries', 'carry', 'cast', 'catch', 'caucChile', 
	'caucIndia', 'caught', 'cause', 'caused', 'causes', 'cc', 'cd', 'ce', 'certain', 'certainly', 
	'cf', 'cg', 'ch', 'change', 'changed', 'changes', 'choose', 'chose', 'chosen', 'ci', 'cit', 
	'cj', 'cl', 'clearly', 'close', 'closed', 'cm', 'cn', 'co', 'com', 'come', 'comes', 'con', 
	'concerning', 'consequently', 'consider', 'considered', 'considering', 'contain', 'containing', 
	'contains', 'continue', 'continued', 'corresponding', 'cost', 'could', 'couldn', "couldn't", 
	'couldnt', 'course', 'cover', 'covered', 'cp', 'cq', 'cr', 'create', 'created', 'cry', 'cs', 
	'ct', 'cu', 'currently', 'cut', 'cv', 'cx', 'cy', 'cystdermoid', 'cz', 'd', 'd2', 'da', 'date', 
	'dc', 'dd', 'de', 'deal', 'dealt', 'dec', 'december', 'decide', 'decided', 'declined', 
	'defects,', 'deficiency', 'definitely', 'denied', 'denies', 'descent', 'descent.', 'describe', 
	'described', 'describes', 'despite', 'detail', 'details', 'determine', 'determined', 'develop', 
	'developed', 'df', 'di', 'diagnosed', 'diagnoses', 'dictated', 'did', 'didn', "didn't", 'die', 
	'different', 'dig', 'discussed', 'dissolved', 'dj', 'dk', 'dl', 'do', 'does', 
	'doesn', "doesn't", 'doing', 'don', "don't", 'done', 'down', 'downwards', 'dp', 'dr', 'drank', 
	'draw', 'drawn', 'drew', 'drink', 'drive', 'driven', 'drop', 'dropped', 'drove', 'drunk', 'ds', 
	'dt', 'du', 'due', 'dug', 'duodenal', 'during', 'dx', 'dy', 'e', 'e2', 'e3', 'ea', 'each', 
	'eat', 'eaten', 'ec', 'ed', 'edu', 'ee', 'ef', 'eg', 'ei', 'eight', 'eighty', 'either', 'ej', 
	'el', 'eleven', 'else', 'elsewhere', 'em', 'empty', 'en', 'encouraged', 'end', 'ended', 
	'ending', 'enough', 'enter', 'entered', 'entirely', 'eo', 'ep', 'eq', 'er', 'es', 'especially', 
	'est', 'et', 'etc', 'eu', 'ev', 'even', 'ever', 'every', 'everybody', 'everyone', 'everything', 
	'everywhere', 'ex', 'exactly', 'example', 'except', 'expect', 'expected', 'explain', 
	'explained', 'extended', 'ey', 'f', 'f2', 'fa', 'face', 'faced', 'fail', 'failed', 'fall', 
	'fallen', 'family', 'far', 'fc', 'feb', 'february', 'fed', 'feed', 'feel', 'fell', 'felt', 
	'few', 'ff', 'fi', 'fifteen', 'fifth', 'fify', 'fight', 'fill', 'filled', 'find', 'fire', 
	'first', 'five', 'fix', 'fj', 'fl', 'flew', 'flown', 'fly', 'fn', 'fo', 'focus', 'focused', 
	'follow', 'followed', 'following', 'follows', 'for', 'forget', 'forgot', 'forgotten', 'former', 
	'formerly', 'forth', 'forty', 'fought', 'found', 'four', 'fr', 'from', 'front', 'fs', 'ft', 
	'fu', 'full', 'further', 'furthermore', 'fy', 'g', 'ga', 'gave', 'ge', 'get', 'gets', 'getting', 
	'gi', 'give', 'given', 'gives', 'giving', 'gj', 'gl', 'go', 'goes', 'going', 'gone', 'got', 
	'gotten', 'gr', 'graves', 'greetings', 'gs', 'gy', 'h', 'h2', 'h3', 'had', 'hadn', "hadn't", 
	'hang', 'hanged', 'happen', 'happened', 'happens', 'hardly', 'has', 'has.', 'hasn', "hasn't", 
	'hasnt', 'have', 'haven', "haven't", 'having', 'hear', 'heard', 'hed', 'held', 'hello', 'help', 
	'helped', 'hence', 'here', "here's", 'hereafter', 'hereby', 'herein', 'heres', 'hereupon', 
	'heritage', 'hh', 'hi', 'hid', 'hidden', 'hide', 'history', 'history.', 'hit', 'hither', 'hj', 
	'ho', 'hold', 'home', 'hope', 'hoped', 'hopefully', 'how', "how's", 'howbeit', 'however', 'hr', 
	'hs', 'http', 'hu', 'hundred', 'hung', 'hurt', 'hy', 'i', "i'd", "i'll", "i'm", "i've", 'i2', 
	'i3', 'i4', 'i6', 'i7', 'i8', 'ia', 'ib', 'ibid', 'ic', 'id', 'identified', 'identify', 'ie', 
	'if', 'ig', 'ignored', 'ih', 'ii', 'ij', 'il', 'im', 'immediate', 'immediately', 'importance', 
	'important', 'in', 'inasmuch', 'inc', 'include', 'included', 'includes', 'increase', 'increased', 
	'indeed', 'index', 'indicate', 'indicated', 'indicates', 'information', 'inner', 'insofar', 
	'instead', 'interest', 'into', 'invention', 'involve', 'involved', 'inward', 'io', 'ip', 'iq', 
	'ir', 'is', 'islands', 'isn', "isn't", 'it', "it'd", "it'll", "it's", 'itd', 'its', 'itself', 
	'iv', 'ix', 'iy', 'iz', 'j', 'jan', 'january', 'jj', 'join', 'joined', 'jr', 'js', 'jt', 'ju', 
	'jul', 'july', 'jun', 'june', 'just', 'k', 'ke', 'keep', 'keeps', 'kept', 'kg', 'kj', 'km', 
	'knew', 'know', 'known', 'knows', 'ko', 'l', 'l2', 'la', 'laid', 'lain', 'largely', 'last', 
	'lately', 'later', 'latter', 'latterly', 'lay', 'lb', 'lc', 'le', 'lead', 'lean', 'leaned', 
	'leant', 'learn', 'learned', 'learnt', 'least', 'leave', 'led', 'left', 'les', 'less', 'lest', 
	'let', "let's", 'lets', 'lf', 'lie', 'lied', 'light', 'like', 'liked', 'likely', 'line', 'listen', 
	'listened', 'lit', 'little', 'lived', 'lj', 'll', 'ln', 'lo', 'look', 'looked', 'looking', 'looks', 
	'los', 'lose', 'lost', 'love', 'loved', 'lr', 'ls', 'lt', 'ltd', 'm', 'm2', 'ma', 'made', 'mainly', 
	'make', 'makes', 'managed', 'many', 'mar', 'march', 'may', 'maybe', 'me', 'mean', 'means', 'meant', 
	'meantime', 'meanwhile', 'meet', 'merely', 'met', 'metastasized', 'metastatic.', 'mg', 'might', 
	'mightn', "mightn't", 'mill', 'million', 'mine', 'ml', 'mn', 'mo', 'more', 'moreover', 
	'morning', 'most', 'mostly', 'move', 'moved', 'mt', 'mu', 'much', 'must', 
	'mustn', "mustn't", 'my', 'myself', 'n', 'n2', 'na', 'name', 'namely', 'nay', 'nc', 'nd', 'ne', 
	'near', 'nearly', 'necessarily', 'necessary', 'need', 'needed', 'needn', "needn't", 'needs', 
	'neither', 'never', 'nevertheless', 'new', 'next', 'ng', 'ni', 'nine', 'ninety', 'nj', 'nl', 
	'nn', 'no', 'nobody', 'non', 'none', 'nonetheless', 'noone', 'nor', 'normally', 'nos', 'not', 
	'note', 'noted', 'nothing', 'nov', 'novel', 'november', 'now', 'nowhere', 'nr', 'ns', 'nt', 'ny', 
	'o', 'oa', 'ob', 'obtain', 'obtained', 'obviously', 'oc', 'occur', 'occurred', 'oct', 'october', 
	'od', 'of', 'off', 'offer', 'offered', 'often', 'og', 'oh', 'oi', 'oj', 'ok', 'okay', 'ol', 'old', 
	'om', 'omitted', 'on', 'once', 'one', 'ones', 'only', 'onto', 'oo', 'op', 'open', 'opened', 'oq', 
	'or', 'ord', 'os', 'ot', 'other', 'others', 'otherwise', 'ou', 'ought', 'our', 'ours', 'ourselves', 
	'out', 'outside', 'over', 'overall', 'overall,', 'ow', 'owing', 'own', 'ox', 'oz', 'p', 'p1', 'p2', 
	'p3', 'page', 'pagecount', 'pages', 'paid', 'par', 'part', 'particular', 'particularly', 'partner', 
	'pas', 'pass', 'passed', 'past', 'pay', 'pc', 'pd', 'pe', 'pedigree', 'per', 'perhaps', 'pf', 'ph', 
	'pi', 'pick', 'picked', 'pj', 'pk', 'pl', 'place', 'placed', 'plan', 'planned', 'play', 'played', 
	'please', 'plus', 'pm', 'pn', 'po', 'point', 'pointed', 'poorly', 'possible', 'possibly', 
	'potentially', 'pp', 'pq', 'pr', 'predominantly', 'prepare', 'prepared', 'present', 'pressure', 
	'presumably', 'presumed', 'previously', 'primarily', 'probably', 'problems', 'produce', 'produced', 
	'promptly', 'protect', 'protected', 'proud', 'prove', 'proved', 'proven', 'provide', 'provided', 
	'provides', 'ps', 'pt', 'pu', 'pull', 'pulled', 'push', 'pushed', 'put', 'py', 'q', 'qj', 'qu', 
	'que', 'quickly', 'quite', 'qv', 'r', 'r2', 'ra', 'ran', 'rang', 'rather', 'rc', 'rd', 're', 
	'reach', 'reached', 'read', 'readily', 'realize', 'realized', 'really', 'reasonably', 'recalls', 
	'receive', 'received', 'recent', 'recently', 'recognize', 'recognized', 'recurred', 'reduce', 
	'reduced', 'ref', 'refs', 'regarding', 'regardless', 'regards', 'related', 'relatively', 'remain', 
	'remained', 'remember', 'remembered', 'remembers', 'removed', 'report', 'reported', 'reports', 
	'represent', 'represented', 'require', 'required', 'research', 'research-articl', 'resolved', 
	'respectively', 'resulted', 'resulting', 'results', 'return', 'returned', 'reviewed', 'rf', 'rh', 
	'ri', 'ridden', 'ride', 'right', 'ring', 'rise', 'risen', 'rj', 'rl', 'rm', 'rn', 'ro', 'rode', 
	'rose', 'rq', 'rr', 'rs', 'rt', 'ru', 'run', 'rung', 'rv', 'ry', 's', 's2', 'sa', 'said', 'same', 
	'sang', 'sat', 'save', 'saved', 'saw', 'say', 'saying', 'says', 'sc', 'screened', 'sd', 'se', 
	'sec', 'second', 'secondly', 'section', 'see', 'seeing', 'seek', 'seem', 'seemed', 'seeming', 
	'seems', 'seen', 'self', 'sell', 'selves', 'send', 'sensible', 'sent', 'sep', 'september', 
	'serious', 'seriously', 'serve', 'served', 'set', 'seven', 'several', 'sf', 'shake', 'shaken', 
	'shall', 'shan', "shan't", 'share', 'shared', 'shook', 'shoot', 'shot', 'should', "should've", 
	'shouldn', "shouldn't", 'show', 'showed', 'shown', 'showns', 'shows', 'shut', 'si', 'sick', 'side', 
	'significant', 'significantly', 'similar', 'similarly', 'since', 'sincere', 'sing', 'sit', 'six', 
	'sixty', 'sj', 'sl', 'sleep', 'slept', 'slid', 'slidden', 'slide', 'slightly', 'sm', 'smell', 
	'smelled', 'smelt', 'sn', 'so', 'sold', 'some', 'somebody', 'somehow', 'someone', 'somethan', 
	'something', 'sometime', 'sometimes', 'somewhat', 'somewhere', 'soon', 'sorry', 'sought', 'sounds', 
	'sp', 'speak', 'specifically', 'specified', 'specify', 'specifying', 'spend', 'spent', 'spoke', 
	'spoken', 'spread', 'sq', 'sr', 'ss', 'st', 'stand', 'start', 'started', 'stated', 'states', 'stay', 
	'stayed', 'steal', 'stenosis.', 'stick', 'still', 'stole', 'stolen', 'stood', 'stop', 'stopped', 
	'strike', 'strongly', 'struck', 'stuck', 'sub', 'substantially', 'successfully', 'such', 'suffered', 
	'suffers', 'sufficiently', 'suggest', 'suggested', 'sung', 'sup', 'support', 'supported', 'sure', 
	'suspected', 'suspects', 'swing', 'swung', 'sy', 'system', 'sz', 't', "t's", 't1', 't2', 't3', 
	'take', 'taken', 'taking', 'talk', 'talked', 'taught', 'tb', 'tc', 'td', 'te', 'teach', 'tear', 
	'tell', 'ten', 'tends', 'tested', 'tf', 'th', 'than', 'thank', 'thanked', 'thanks', 'thanx', 
	'that', "that'll", "that's", "that've", 'thats', 'the', 'then', 'thence', 'there', "there'll", 
	"there's", "there've", 'thereafter', 'thereby', 'thered', 'therefore', 'therein', 'thereof', 
	'therere', 'theres', 'thereto', 'thereupon', 'these', 'thickv', 'thin', 'think', 'third', 'this', 
	'thorough', 'thoroughly', 'those', 'thou', 'though', 'thoughh', 'thought', 'thousand', 'three', 
	'threw', 'throug', 'through', 'throughout', 'throw', 'thrown', 'thru', 'thus', 'ti', 'til', 'tip', 
	'tj', 'tl', 'tm', 'tn', 'to', 'today', 'today.', 'together', 'told', 'tomorrow', 'too', 'took', 
	'top', 'tore', 'torn', 'toward', 'towards', 'tp', 'tq', 'tr', 'tried', 'tries', 'truly', 'try', 
	'trying', 'ts', 'tt', 'turn', 'turned', 'tv', 'twelve', 'twenty', 'twice', 'two', 'tx', 'u', 'u201d', 
	'ue', 'ui', 'uj', 'uk', 'um', 'un', 'under', 'understand', 'understood', 'underwent', 
	'unfortunately', 'unless', 'unlike', 'unlikely', 'until', 'unto', 'uo', 'up', 'upon', 'ups', 'ur', 
	'us', 'use', 'used', 'useful', 'usefully', 'usefulness', 'uses', 'using', 'usually', 'ut', 'v', 
	'va', 'value', 'various', 'vd', 've', 'very', 'via', 'visit', 'viz', 'vj', 'vo', 'vol', 'vols', 
	'volumtype', 'vq', 'vs', 'vt', 'vu', 'w', 'wa', 'wait', 'waited', 'wake', 'waked', 'walk', 'walked', 
	'want', 'wanted', 'wants', 'was', 'wasn', "wasn't", 'wasnt', 'watch', 'watched', 'way', 'we', 
	"we'd", "we'll", "we're", "we've", 'wear', 'wears', 'wed', 'welcome', 'well', 'well-b', 'went', 
	'were', 'weren', "weren't", 'werent', 'what', "what'll", "what's", 'whatever', 'whats', 'when', 
	"when's", 'whence', 'whenever', 'where', "where's", 'whereafter', 'whereas', 'whereby', 'wherein', 
	'wheres', 'whereupon', 'wherever', 'whether', 'which', 'while', 'whim', 'whither', 'who', "who'll", 
	"who's", 'whod', 'whoever', 'whole', 'whom', 'whomever', 'whos', 'whose', 'why', "why's", 'wi', 
	'widely', 'will', 'willing', 'win', 'wish', 'with', 'within', 'without', 'wo', 'woke', 'woken', 
	'won', "won't", 'wonder', 'wondered', 'wont', 'words', 'wore', 'work', 'worked', 'works', 'world', 
	'worn', 'would', 'wouldn', "wouldn't", 'wouldnt', 'wrap', 'wrapped', 'wrapt', 'write', 'written', 
	'wrote', 'www', 'x', 'x1', 'x2', 'x3', 'xf', 'xi', 'xj', 'xk', 'xl', 'xn', 'xo', 'xs', 'xt', 'xv', 
	'xx', 'y', 'y2', 'yes', 'yet', 'yj', 'yl', 'you', "you'd", "you'll", "you're", "you've", 'youd', 
	'your', 'youre', 'yours', 'yourself', 'yourselves', 'yr', 'ys', 'yt', 'z', 'zero', 'zi', 'zz'])