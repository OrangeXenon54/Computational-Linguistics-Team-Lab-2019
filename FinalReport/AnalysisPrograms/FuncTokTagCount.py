import re

def TagCandP(TagNum) :
    tagN = []
    if TagNum == 1 :
        for keyT, valT in alltokens.items() :
            if len(valT) == 1 :
                tokenPOScount = [keyT, valT]
                tagN.append(tokenPOScount)
            else :
                continue
    else :
        for keyT, valT in alltokens.items() :
            if len(valT) == TagNum :
                for keyP, valP in alltokens[keyT].items() :
                    if TagNum == 8:
                        tokenPOScount = [keyT, keyP, valP]
                        print(tokenPOScount)
                    if keyT not in tagN:
                        tagN.append(keyT)
            else :
                continue
    if len(tagN) < 1 :
        print("No tokens with just ", TagNum, " POS tags \n")
    else :
        tagNpercent = len(tagN) / nc / tokentotal
        print("--", TagNum, " POS Tag Count: ", len(tagN))
        print(tagNpercent, " of all tokens\n")
        if TagNum >= 6:
            for item in tagN :
                print(item)

filename = input("Please type file name:")

devtext = open(filename)

alltokens = {}

print("Starting data reading: ")

for line in devtext :
    if line == "\n" :
        continue
    else :
        stripped = line.strip()
        word = re.findall('(^.+)\t', stripped)[0]
        postag = re.findall('\t(.+$)', stripped)[0]
        if word not in alltokens :
            alltokens[word] = {}
            alltokens[word][postag] = 1
        elif postag not in alltokens[word] :
            alltokens[word][postag] = 1
        elif postag in alltokens[word] :
            alltokens[word][postag] += 1

tokentotal = len(alltokens)

print("Data reading finished")
print("---------------")

print("Total Number of Unique Tokens: ", tokentotal, "\n")

nc = 1
while True :
    TagCandP(nc)
    nc += 1
    if nc == 49 :
        break
