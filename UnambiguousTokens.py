import re

#Returns a dictionary of dictionaries where the first key is the token, the second key is the tag, and the value is the total count of that token as that tag
#Argument is a text file that can be read line by line
def TPCDict(datafile) :
    alltokens = {}
    for line in devtext :
        if line == "\n" :
            continue
        else :
            stripped = line.strip()
            word = re.findall('(^\S*)\s', stripped)[0]
            postag = re.findall('\s(\S*$)', stripped)[0]
            if word not in alltokens :
                alltokens[word] = {}
                alltokens[word][postag] = 1
            elif postag not in alltokens[word] :
                alltokens[word][postag] = 1
            elif postag in alltokens[word] :
                alltokens[word][postag] += 1
    return alltokens

#Returns a dictionary where the key is a token and its value is a POS tag
#The tag is considered "unambiguous" for the token if 90% of the time, the token is that tag
#Argument is a dictionary of dictionaries produced by TPCDict
def UAToks(tpcdict) :
    uatokens = {}
    for keyT, valT in tpcdict.items() :
        totaltags = 0
        for keyC, valC in valT.items() :
            totaltags += valC
        for keyC, valC in valT.items() :
            tagpercent = valC / totaltags
            if tagpercent >= 0.90000 :
                uatokens[keyT] = keyC
    return uatokens

filename = input("Please type file name:")
devtext = open(filename)

print("Creating token, tag, and count dictionary....")
tpcd = TPCDict(devtext)
print("***Dictionary created***\n")

print("Determining unambiguous tokens...")
uatoks = UAToks(tpcd)
print("***Tokens Determined***\n")

print("--Here are all unambiguous tokens and their tags--")
for key, val in uatoks.items() :
    print(key, " ", val)
