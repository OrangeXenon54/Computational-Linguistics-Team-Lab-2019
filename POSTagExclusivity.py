import re

filename = input("Please type file name:")
devtext = open(filename)
alltags = {}
taglist = []
print("**********************\nStarting data reading:\n**********************")

for line in devtext :
    if line == "\n" :
        continue
    else :
        stripped = line.strip()
        token = re.findall('(^\S*)\s', stripped)[0]
        postag = re.findall('\s(\S*$)', stripped)[0]
        if postag not in taglist :
            alltags[postag] = set()
            alltags[postag].add(token)
            taglist.append(postag)
        elif token not in alltags[postag] :
            alltags[postag].add(token)
        elif token in alltags[postag] :
            continue

taglist = sorted(taglist)
puredict = alltags
puretags = []
impuretags = []

print("Data reading finished")
print("List of POS Tags in Document:")
for item in taglist :
    print(item)
print("---------------")

for focustag in taglist :
    taggedwords = puredict.pop(focustag)
    purecount = 0
    impurities = []
    for key, val in puredict.items() :
        for word in taggedwords :
            if word in val :
                impure = key, word
                impurities.append(impure)
                purecount += 1
            else :
                continue
    if purecount == 0 :
        puretags.append(focustag)
        #print(focustag, " is exclusive")
        #seelist = input("Do you want to see the exclusive words? Type y or n")
        #if seelist == "y" or "Y" or "yes" :
            #for word in taggedwords :
                #print(word)
            #print("\n")
        #else :
            #print("Skipping words \n")
    else :
        impnum = len(impurities)
        imptagcount = focustag, impnum
        impuretags.append(imptagcount)
        #print(focustag, " is NOT exclusive")
        #seelist = input("Do you want to see the list of shared words and their POS tag? Type y or n")
        #if seelist == "y" or "Y" or "yes" :
            #for tup in impurities :
                #print(tup)
            #print("\n")
        #else :
            #print("Skipping words \n")

print("Here are all exclusive tags\n")
puretags = sorted(puretags)
for item in puretags :
    print(item)
print("******************")
print("Here are tags and how many tokens cross over")
impuretags = sorted(impuretags)
for item in impuretags :
    print(item)
