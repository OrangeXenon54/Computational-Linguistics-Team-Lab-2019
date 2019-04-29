def readFile(path):
	source = open(path,"r")
	return source

def getSentenceCorpora(file):
	sentences = []
	sentence = []
	for line in file:
		token = line.split("\t")[0]
		#pos = line.split("\t")[1]
		if token != "\n":
			sentence.append(token)
		if token == "\n":
			sentences.append(sentence)
			sentence = []
	return sentences

def predictWriteToFile(filename,sent_corpora):
	f = open(filename,"w")
	for sent in sent_corpora:
		for token in sent:
			###                               ###
			### INSERT PREDICTION METHOD HERE ###
			###                               ###
			pos = "pos"
			f.write(token+"\t"+pos+"\n")
		f.write("\n")

if __name__ == "__main__":
	file = readFile("dev.col")
	corp = getSentenceCorpora(file)
	predictWriteToFile("dev_pred.col",corp)