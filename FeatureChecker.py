import re

#Returns a list of strings from the data with only the tokens and new lines so that tokens can be analyzed and POS tags added later
#Argument is a text file that breaks down into a list of strings
def NoPOSList(datafile) :
    tokensNoPOS = []
    for line in datafile:
        if line == "\n" :
            tokensNoPos.append(line)
        else :
            stripped = line.strip()
            word = re.findall('(^\S*)\s', stripped)[0]
            tokensNoPOS.append(word)
    return tokensNoPOS

#Returns a list of strings that are the extracted POS tags from the data plus new lines
#Argument is a text file that breaks down into a list of strings
def TargetTags(datafile) :
    TargetTagList = []
    for line in datafile:
        if line == "\n" :
            TargetTagList.append(line)
        else :
            stripped = line.strip()
            postag = re.findall('\s(\S*$)', stripped)[0]
            TargetTagList.append(line)
    return TargetTagList

#Returns a list of lists with each list representing a whole sentence
#Argument is a list of strings
def SenList(tokenlist) :
    allsentences = []
    sentence = []
    for word in tokenlist :
        if word == "\n" :
            allsentences.append(sentence)
            allsentences.append(word)
            sentence = []
        else :
            sentence.append(word)
    return allsentences

#Returns a list of lists with the list consisting of the token -a string -and its features -a set
#For now, only assigns features on single token basis not in context
#Argument is a list of strings
def FeatureChecker(tokenlist) :
    tokANDfeat = []
    for word in tokenlist:
        if word == "\n" :
            tokANDfeat.append(word)
        else :
            feats = set()
            if re.search('\S+ed$', word) :
                if re.search('\S+ied', word) :
                    feats.add("featIED")
                else :
                    feats.add("featED")
            if re.search('\S+er$', word) :
                if re.search('\S+ier$', word) :
                    feats.add("featIER")
                else :
                    feats.add("featER")
            if re.search('\S+s$', word) :
                if re.search('\S+ies$', word) :
                    feats.add("featIES")
                elif re.search('\S+es$', word) :
                    feats.add("featES")
                else :
                    feats.add("featS")
            if re.search('^[0-9]+', word) :
                feats.add("featNUM")
            if re.search('\S+ing$', word) or re.search('\S+ings$', word) :
                feats.add("featING")
            if re.search('\S+ly$', word) :
                feats.add("featLY")
            if re.search('\S+ful$', word) :
                feats.add("featFUL")
            if re.search('^[Uu]n\S+', word) or re.search('(^[Nn]on)\S+', word) :
                feats.add("featNEGP")
            if re.search('^[A-Z]\S+', word) :
                feats.add("featCAP")
            if re.search('\S+est$', word) :
                if re.search('\S+iest$', word) :
                    feats.add("featIEST")
                else :
                    feats.add("featEST")
            if re.search('^\'\S+', word) :
                feats.add("featAPOS")
            if len(feats) <= 0 :
                tokfeats = [word]
            else :
                tokfeats = [word, feats]
            tokANDfeat.append(tokfeats)
    return tokANDfeat

filename = input("Please type file name:")
devtext = open(filename)

print("Creating list of all tokens...")
justtokens = NoPOSList(devtext)
print("***All tokens list created***\n")
print("Adding features to all tokens...")
tokenfeatures = FeatureChecker(justtokens)
print("***All features added to tokens***\n")

"""
A.)	featED
1.)	the word ends in “ed”
B.)	featIED
1.)	the word ends in “ied”
C.)	featS
1.)	the word ends in “s”
D.)	featES
1.)	the word ends in “es”
E.)	featIES
1.)	the word ends in “ies”
F.)	featLY
1.)	the word ends in “ly”
G.)	featING
1.)	the word ends in “ing”
H.)	featNEGP
1.)	the word begins with “un” or “non”
I.)	featFUL
1.)	the word ends in “ful”
J.)	featER
1.)	the word ends in “er”
K.)	featIER
1.)	the word ends in “ier”
L.)	featEST
1.)	the word ends in “est”
M.)	featIEST
1.)	the word ends in “iest”
N.)	featCAP
1.)	the word begins with a capital letter and is not the first word in the sentence
O.)	featNUM
1.)	The word contains a numeric character
P.) featAPOS
1.) The word starts with an apostrophe
"""
