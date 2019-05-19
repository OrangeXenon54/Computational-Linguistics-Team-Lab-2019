import re

#Returns a dictionary where the key is the line number and the value is a list of all tokens in the line
#Argument is a text file
def SentDict(textfile) :
    sents = {}
    for line in textfile:
        senttok = line.split()
        linenum = int(senttok.pop(0))
        sents[linenum] = senttok
    return sents

#Returns a list of lists, with the lists being word pairs such that each token is represented with both the word in front of it and after it
#Argument is a list such as the value from the SentDict()
def WordPairs(sentence) :
    wordpairs = []
    lastposition = len(sentence) - 1
    noback = []
    nofront = []
    indnum = 0
    for item in sentence :
        if indnum == 0 :
            noback.append(item)
            indnum += 1
        elif indnum < lastposition :
            noback.append(item)
            nofront.append(item)
            indnum += 1
        else :
            nofront.append(item)
    indnum = 0
    while indnum < lastposition :
        word1 = noback[indnum]
        word2 = nofront[indnum]
        pair = []
        pair.append(word1)
        pair.append(word2)
        wordpairs.append(pair)
        indnum += 1
    return wordpairs

#Returns a list of lists with the 1st item being the line number and the 2nd being the name
def AnswerKey(textfile) :
    answers = []
    for line in textfile :
        if line == "\n" :
            continue
        else :
            tokens = line.split()
            if len(tokens) < 3 :
                continue
            else :
                linenum = int(tokens.pop(0))
                useless = tokens.pop(0)
                if len(tokens) == 1 :
                    pair = [linenum, tokens[0]]
                else :
                    words = []
                    lastindex = len(tokens) - 1
                    itnum = 0
                    fullname = " "
                    for tok in tokens :
                        if itnum == lastindex :
                            fullname = fullname + tok
                        else :
                            fullname = fullname + tok + " "
                    fullname = fullname.strip()
                    pair = [linenum, fullname]
                answers.append(pair)
    return answers

filename = input("Please type file name:")
devtext = open(filename)
print("Creating dictionary of sentences.\nPlease wait......")
sentences = SentDict(devtext)
print("***Dictionary Successfully Created***")
print("-------------------------------")
ankey = input("Please input answer key file name: ")
keyfile = open(ankey)
answers = AnswerKey(keyfile)
print("----------------")
print("Here are the correct names: ")
for answer in answers :
    print(answer)
print("\n\n")
print("Checking for names\nPlease wait.......\n")
NERList = []
for key, val in sentences.items() :
    if len(val) < 3 :
        continue
    else :
        pairs = WordPairs(val)
        for pair in pairs :
            #If 1st word has a capital letter followed by a period and 2nd word starts with a capital
            if re.search('^[A-Z]\.$', pair[0]) and re.search('^[A-Z]+\S+$', pair[1]) :
                pair[0] = pair[0] + " "
                namedE = pair[0] + pair[1]
                lineNE = [key, namedE]
                NERList.append(lineNE)
            #If both words start with capital letters
            elif re.search('^[A-Z][a-z]+$', pair[0]) and re.search('^[A-Z][a-z]+$', pair[1]) :
                pair[0] = pair[0] + " "
                namedE = pair[0] + pair[1]
                lineNE = [key, namedE]
                NERList.append(lineNE)
            #If first word starts with capital lower capital
            elif re.search('^[A-Z][a-z][A-Z]\S+$', pair[0]) :
                lineNE = [key, pair[0]]
                NERList.append(lineNE)
            #If first word starts with capital apostrophe captial
            elif re.search('^[A-Z]\'[A-Z][a-z]+$', pair[0]) :
                lineNE = [key, pair[0]]
                NERList.append(lineNE)
            #If first word ends in tti
            elif re.search('^[A-Z]+[A-Za-z]*[Tt][Tt][Ii]$', pair[0]) :
                lineNE = [key, pair[0]]
                NERList.append(lineNE)
            #If first word ends in ova
            elif re.search('^[A-Z]+[A-Za-z]*[Oo][Vv][Aa]$', pair[0]) :
                lineNE = [key, pair[0]]
                NERList.append(lineNE)
            #If first word ends in ola
            elif re.search('^[A-Z]+[A-Za-z]*[Oo][Ll][Aa]$', pair[0]) :
                lineNE = [key, pair[0]]
                NERList.append(lineNE)
            #If first word ends in son
            elif re.search('^[A-Z]+[A-Za-z]+[Ss][Oo][Nn]$', pair[0]) :
                lineNE = [key, pair[0]]
                NERList.append(lineNE)
            #If first word begins with Fitz
            elif re.search('^[Ff][Ii][Tt][Zz]\S+', pair[0]) :
                lineNE = [key, pair[0]]
                NERList.append(lineNE)
            #If word begins with a capital letter and is longer than 8 letters
            elif re.search('^[A-Z]+\S+', pair[0]) and len(pair[0]) > 8 :
                lineNE = [key, pair[0]]
                NERList.append(lineNE)
            #If these words/pairs don't meet any of these rules, skip them
            else :
                continue

if len(NERList) < 1 :
    print("No names found.")
elif len(NERList) >= 1 :
    print("Total number of names found: ", len(NERList), "\n")
    print("Here are the names:")
    for item in NERList :
        print(item)
else :
    quit()

tp = 0
fp = 0

for item in answers :
    if item in NERList :
        tp += 1

fp = len(NERList) - tp
print("Number of Correctly Tagged Names :", tp)
fp = float(fp)
tp = float(tp)
fn = len(answers) - tp
fn = float(fn)
per = tp / (fp + tp)
rec = tp / (tp + fn)
fscore = (2 * per * rec) / (per + rec)
print("Number of Wrongly Tagged Names: ", fp)
print("Number of Missed Names: ", fn, "\n")
print("Precision: ", per)
print("Recall: ", rec)
print("F-Score: ", fscore)
