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
        if re.search('\S+ied', token) :
            features.append(1.)
        else :
            features.append(0.)
        #eS
        if re.search('\S+s$', token) :
            features.append(1.)
        else :
            features.append(0.)
        #eES
        if re.search('\S+es$', token) :
            features.append(1.)
        else :
            features.append(0.)
        #eIES
        if re.search('\S+ies$', token) :
            features.append(1.)
        else :
            features.append(0.)
        #eLY
        if re.search('\S+ly$', token) :
            features.append(1.)
        else :
            features.append(0.)
        #eING
        if re.search('\S+ing$', token) :
            features.append(1.)
        else :
            features.append(0.)
        #eINGS
        if re.search('\S+ings$', token):
            features.append(1.)
        else :
            features.append(0.)
        #bUN
        if re.search('^[Uu]n\S+', token) :
            features.append(1.)
        else :
            features.append(0.)
        #bNON
        if re.search('(^[Nn]on)\S+', token) :
            features.append(1.)
        else :
            features.append(0.)
        #eFUL
        if re.search('\S+ful$', token) :
            features.append(1.)
        else :
            features.append(0.)
        #eER
        if re.search('\S+er$', token) :
            features.append(1.)
        else :
            features.append(0.)
        #eIER
        if re.search('\S+ier$', token) :
            features.append(1.)
        else :
            features.append(0.)
        #eEST
        if re.search('\S+est$', token) :
            features.append(1.)
        else :
            features.append(0.)
        #eIEST
        if re.search('\S+iest$', token) :
            features.append(1.)
        else :
            features.append(0.)
        #bCAP
        if re.search('^[A-Z]\S+', token) :
            features.append(1.)
        else :
            features.append(0.)
        #iNUM
        if re.search('^[0-9]+', token) :
            features.append(1.)
        else :
            features.append(0.)
        #bAPOS
        if re.search('^\'\S+', token) :
            features.append(1.)
        else :
            features.append(0.)
        #iG7
        if len(token) > 7 :
            features.append(1.)
        else :
            features.append(0.)
        #eION
        if re.search('\S+ion$', token) :
            features.append(1.)
        else :
            features.append(0.)
        #eIONS
        if re.search('\S+ions$', token) :
            features.append(1.)
        else :
            features.append(0.)
        #eTION
        if re.search('\S+tion$', token) :
            features.append(1.)
        else :
            features.append(0.)
        #eTIONS
        if re.search('\S+tions$', token) :
            features.append(1.)
        else :
            features.append(0.)
        #eNESS
        if re.search('\S+ness$', token) :
            features.append(1.)
        else :
            features.append(0.)
        #eNESSES
        if re.search('\S+nesses$', token) :
            features.append(1.)
        else :
            features.append(0.)
        #eSHIP
        if re.search('\S+ship$', token) :
            features.append(1.)
        else :
            features.append(0.)
        #eSHIPS
        if re.search('\S+ships$', token) :
            features.append(1.)
        else :
            features.append(0.)
        #eSION
        if re.search('\S+sion$', token) :
            features.append(1.)
        else :
            features.append(0.)
        #eSIONS
        if re.search('\S+sions$', token) :
            features.append(1.)
        else :
            features.append(0.)
        #eMENT
        if re.search('\S+ment$', token) :
            features.append(1.)
        else :
            features.append(0.)
        #eMENTS
        if re.search('\S+ments$', token) :
            features.append(1.)
        else :
            features.append(0.)
        #iOF
        if token is "of" or "OF" or "Of" :
            features.append(1.)
        else :
            features.append(0.)
        #iIN
        if token is "in" or "IN" or "In" :
            features.append(1.)
        else :
            features.append(0.)
        #iTO
        if token is "to" or "TO" or "To" :
            features.append(1.)
        else :
            features.append(0.)
        #iFOR
        if token is "FOR" or "for" or "For" :
            features.append(1.)
        else :
            features.append(0.)
        #iWITH
        if token is "WITH" or "with" or "With" :
            features.append(1.)
        else :
            features.append(0.)
        #iON
        if token is "ON" or "on" or "On" :
            features.append(1.)
        else :
            features.append(0.)
        #iAT
        if token is "at" or "AT" or "At" :
            features.append(1.)
        else :
            features.append(0.)
        #iFROM
        if token is "from" or "FROM" or "From" :
            features.append(1.)
        else :
            features.append(0.)
        #iBY
        if token is "BY" or "by" or "By" :
            features.append(1.)
        else :
            features.append(0.)
        #iABOUT
        if token is "ABOUT" or "about" or "About" :
            features.append(1.)
        else :
            features.append(0.)
        #iAS
        if token is "as" or "AS" or "As" :
            features.append(1.)
        else :
            features.append(0.)
        #iINTO
        if token is "INTO" or "into" or "Into" :
            features.append(1.)
        else :
            features.append(0.)
        #iLIKE
        if token is "like" or "LIKE" or "Like" :
            features.append(1.)
        else :
            features.append(0.)
        #iTHROUGH
        if token is "through" or "THROUGH" or "Through" :
            features.append(1.)
        else :
            features.append(0.)
        #iAFTER
        if token is "AFTER" or "after" or "After" :
            features.append(1.)
        else :
            features.append(0.)
        #iOVER
        if token is "OVER" or "Over" or "over" :
            features.append(1.)
        else :
            features.append(0.)
        #iBETWEEN
        if token is "BETWEEN" or "between" or "Between" :
            features.append(1.)
        else :
            features.append(0.)
        #iOUT
        if token is "OUT" or "out" or "Out" :
            features.append(1.)
        else :
            features.append(0.)
        #iAGAINST
        if token is "AGAINST" or "against" or "Against" :
            features.append(1.)
        else :
            features.append(0.)
        #iDURING
        if token is "DURING" or "during" or "During" :
            features.append(1.)
        else :
            features.append(0.)
        #iWITHOUT
        if token is "WITHOUT" or "without" or "Without" :
            features.append(1.)
        else :
            features.append(0.)
        #iBEFORE
        if token is "BEFORE" or "Before" or "before" :
            features.append(1.)
        else :
            features.append(0.)
        #iUNDER
        if token is "UNDER" or "under" or "Under" :
            features.append(1.)
        else :
            features.append(0.)
        #iAROUND
        if token is "AROUND" or "around" or "Around" :
            features.append(1.)
        else :
            features.append(0.)
        #iAMONG
        if token is "AMONG" or "among" or "Among" :
            features.append(1.)
        else :
            features.append(0.)
        #iTHE
        if token is "the" or "THE" or "The" :
            features.append(1.)
        else :
            features.append(0.)
        #iA
        if token is "a" or "A" :
            features.append(1.)
        else :
            features.append(0.)
        #iAN
        if token is "an" or "AN" or "An" :
            features.append(1.)
        else :
            features.append(0.)
        #iI
        if token is "I" :
            features.append(1.)
        else :
            features.append(0.)
        #iYOU
        if toekn is "YOU" or "you" or "You" :
            features.append(1.)
        else :
            features.append(0.)
        #iTHEY
        if token is "THEY" or "they" or "They" :
            features.append(1.)
        else :
            features.append(0.)
        #iHE
        if token is "he" or "HE" or "He" :
            features.append(1.)
        else :
            features.append(0.)
        #iSHE
        if token is "she" or "SHE" or "She" :
            features.append(1.)
        else :
            features.append(0.)
        #iIT
        if token is "it" or "IT" or "It" :
            features.append(1.)
        else :
            features.append(0.)
        #iIS
        if token is "is" or "IS" or "Is" :
            features.append(1.)
        else :
            features.append(0.)
        #iWAS
        if token is "was" or "WAS" or "Was" :
            features.append(1.)
        else :
            features.append(0.)
        #iARE
        if token is "are" or "ARE" or "Are" :
            features.append(1.)
        else :
            features.append(0.)
        #iAM
        if token is "am" or "AM" or "Am" :
            features.append(1.)
        else :
            features.append(0.)
        #iWERE
        if token is "WERE" or "Were" or "were" :
            features.append(1.)
        else :
            features.append(0.)
        #iWHO
        if token is "WHO" or "who" or "Who" :
            features.append(1.)
        else :
            features.append(0.)
        #iWHAT
        if token is "WHAT" or "What" or "what" :
            features.append(1.)
        else :
            features.append(0.)
        #iWHEN
        if token is "WHEN" or "When" or "when" :
            features.append(1.)
        else :
            features.append(0.)
        #iTHEN
        if token is "then" or "THEN" or "Then" :
            features.append(1.)
        else :
            features.append(0.)
        #iWHERE
        if token is "where" or "WHERE" or "Where" :
            features.append(1.)
        else :
            features.append(0.)
        #iTHERE
        if token is "THERE" or "There" or "there" :
            features.append(1.)
        else :
            features.append(0.)
        #iWHY
        if token is "WHY" or "why" or "Why" :
            features.append(1.)
        else :
            features.append(0.)
        #iHOW
        if token is "HOW" or "How" or "how" :
            features.append(1.)
        else :
            features.append(0.)
        #iPERIOD
        if token is "." :
            features.append(1.)
        else :
            features.append(0.)
        #iQUESTION
        if token is "?" :
            features.append(1.)
        else :
            features.append(0.)
        #iCOMMA
        if token is "," :
            features.append(1.)
        else :
            features.append(0.)
        #iCOLON
        if token is ":" :
            features.append(1.)
        else :
            features.append(0.)
        #iSEMICOLON
        if token is ";" :
            features.append(1.)
        else :
            features.append(0.)
        #iLRB
        if token is "(" or "{" :
            features.append(1.)
        else :
            features.append(0.)
        #iRRB
        if token is ")" or "}" :
            features.append(1.)
        else :
            features.append(0.)
        #iLQUOTE
        if token is "``" :
            features.append(1.)
        else :
            features.append(0.)
        #iRQUOTE
        if token is "''" :
            features.append(1.)
        else :
            features.append(0.)
        #iDOLLAR
        if token is "$" :
            features.append(1.)
        else :
            features.append(0.)
        #iHYPH
        if token is "-" :
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
20.) iG7: is greater than 7 letters
21.) eION: ends in "ion"
22.) eIONS: ends in "ions"
23.) eTION: ends in "tion"
24.) eTIONS: ends in "tions"
25.) eNESS: ends in "ness"
26.) eNESSES: ends in "nesses"
27.) eSHIP: ends in "ship"
28.) eSHIPS: ends in "ships"
30.) eSION: ends in "sion"
31.) eSIONS: ends in "sions"
32.) eMENT: ends in "ment"
33.) eMENTS: ends in "ments"
+ more specific word checking features for common words
e = ends with
b = begins with
i = is
"""
