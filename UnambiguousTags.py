import re

filename = input("Please type file name:")

devtext = open(filename)

alltokens = {}
tagcount = {}

print("Starting data reading: ")

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

print("Data reading finished")
print("---------------")
print("***Tokens with 1 POS Tag*** \n")
tag1 = []
for keyT, valT in alltokens.items() :
    if len(keyT) == 1 :
        tokenPOScount = [keyT, valT]
        tag1.append(tokenPOScount)
    else :
        continue
if len(tag1) < 1 :
    print("No tokens with only 1 POS tag \n")
else :
    tag1 = sorted(tag1)
    for item in tag1 :
        print(item)
        del alltokens[item[0]]

print("\n***Tokens with 2 POS Tags*** \n")
tag2 = []
for keyT, valT in alltokens.items() :
    if len(valT) == 2 :
        for keyP, valP in alltokens[keyT].items() :
            tokenPOScount = [keyT, keyP, valP]
            tag2.append(tokenPOScount)
    else :
        continue
if len(tag2) < 1 :
    print("No tokens with only 2 POS tags \n")
else :
    tag2 = sorted(tag2)
    for item in tag2 :
        print(item)
        if item[0] in alltokens :
            del alltokens[item[0]]

print("\n***Tokens with 3 POS Tags*** \n")
tag3 = []
for keyT, valT in alltokens.items() :
    if len(valT) == 3 :
        for keyP, valP in alltokens[keyT].items() :
            tokenPOScount = [keyT, keyP, valP]
            tag3.append(tokenPOScount)
    else :
        continue
if len(tag3) < 1 :
    print("No tokens with only 3 POS tags \n")
else :
    tag3 = sorted(tag3)
    for item in tag3 :
        print(item)
        if item[0] in alltokens :
            del alltokens[item[0]]
