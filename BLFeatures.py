import re

#Returns a list of strings from the data with only the tokens and new lines so that tokens can be analyzed and POS tags added later
#Argument is a text file that breaks down into a list of strings
def NoPOSList(datafile) :
    tokensNoPOS = []
    for line in datafile:
        if line == "\n" :
            tokensNoPOS.append(line)
        else :
            stripped = line.strip()
            word = re.findall('(^\S*?)\s', stripped)[0]
            tokensNoPOS.append(word)
    return tokensNoPOS

featurenameorder = ["BIAS", "eED", "eIED", "eS", "eES", "eIES", "eLY", "eING", "eINGS", "bUN", "bNON", "eFUL", "eER", "eIER", "eEST", "eIEST", "bCAP", "iNUM", "bAPOS"]

#Returns a list of lists with the list consisting of the token -a string -and its features -a set
#For now, only assigns features on single token basis not in context
#Argument is a list of strings
def FeatureChecker(token) :
    features = []
    if token == "\n" :
        features.append("NULL")
        #features = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    else :
        #BIAS
        features.append(1.)
        #eED
        if re.search('\S+ed$', token) :
            features.append(1.)
        else:
            features.append(0.)
        #eIED
        if re.search('\S+ied', word) :
            features.append(1.)
        else :
            features.append(0.)
        #eS
        if re.search('\S+s$', word) :
            features.append(1.)
        else :
            features.append(0.)
        #eES
        if re.search('\S+es$', word) :
            features.append(1.)
        else :
            features.append(0.)
        #eIES
        if re.search('\S+ies$', word) :
            features.append(1.)
        else :
            features.append(0.)
        #eLY
        if re.search('\S+ly$', word) :
            features.append(1.)
        else :
            features.append(0.)
        #eING
        if re.search('\S+ing$', word) :
            features.append(1.)
        else :
            features.append(0.)
        #eINGS
        if re.search('\S+ings$', word):
            features.append(1.)
        else :
            features.append(0.)
        #bUN
        if re.search('^[Uu]n\S+', word) :
            features.append(1.)
        else :
            features.append(0.)
        #bNON
        if re.search('(^[Nn]on)\S+', word) :
            features.append(1.)
        else :
            features.append(0.)
        #eFUL
        if re.search('\S+ful$', word) :
            features.append(1.)
        else :
            features.append(0.)
        #eER
        if re.search('\S+er$', word) :
            features.append(1.)
        else :
            features.append(0.)
        #eIER
        if re.search('\S+ier$', word) :
            features.append(1.)
        else :
            features.append(0.)
        #eEST
        if re.search('\S+est$', word) :
            features.append(1.)
        else :
            features.append(0.)
        #eIEST
        if re.search('\S+iest$', word) :
            features.append(1.)
        else :
            features.append(0.)
        #bCAP
        if re.search('^[A-Z]\S+', word) :
            features.append(1.)
        else :
            features.append(0.)
        #iNUM
        if re.search('^[0-9]+', word) :
            features.append(1.)
        else :
            features.append(0.)
        #bAPOS
        if re.search('^\'\S+', word) :
            features.append(1.)
        else :
            features.append(0.)
    return features

filename = input("Please type file name:")
devtext = open(filename)

justtokens = NoPOSList(devtext)
toksANDfeats = []

for tok in justtokens :
    feats = FeatureChecker(tok)
    tf = [tok, feats]
    toksANDfeats.append(tf)

for item in toksANDfeats :
    print(item)

"""
1.)	BIAS: just something you add to the feature vector
2.)	eED: the word ends in “ed”
3.)	eIED: the word ends in “ied”
4.)	eS: the word ends in “s”
5.)	eES: the word ends in “es”
6.)	eIES: the word ends in “ies”
7.)	eLY: the word ends in “ly”
8.)	eING: the word ends in “ing”
9.)	eINGS: the word ends in "ings"
10.) bUN: the word begins with "un"
11.) bNON: the word begins with "non"
12.) eFUL: the word ends in “ful”
13.) eER: the word ends in “er”
14.) eIER: the word ends in “ier”
15.) eEST: the word ends in “est”
16.) eIEST: the word ends in “iest”
17.) bCAP: the word begins with a capital letter and is not the first word in the sentence
18.) iNUM: The word contains a numeric character
19.) bAPOS: The word starts with an apostrophe
e = ends with
b = begins with
i = is
"""
