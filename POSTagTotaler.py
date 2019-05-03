filename = input("Please type file name:")

devtext = open(filename)

allpos = []
seen = set()
TagEx = []

#Iterate through the text, making a list of every POS tag in it
#Also find the first example of each POS instance and count the POS as seen
for line in devtext :
    if line == "\n" :
        continue
    else :
        stripped = line.strip()
        postag = stripped.split()[1]
        allpos.append(postag)
        if postag not in seen :
            seen.add(postag)
            POSex = stripped.split()[0]
            TagEx.append([postag, POSex])
        else :
            continue

#Sort the lists of all tags and examples and total number of POS seen
allpos = sorted(allpos)
TagEx = sorted(TagEx)
seencount = len(seen)

#Convert seen, an unordered set, to a sorted list
sortseen = []
for item in seen :
    sortseen.append(item)
sortseen = sorted(sortseen)

#Count the total instances of a POS and make a list of lists
totals = []
countword = None
for pos in allpos :
    if countword is None :
        countword = pos
        postotal = [countword, 1]
    elif countword == pos :
            postotal[1] = postotal[1] + 1
    else :
        totals.append(postotal)
        countword = pos
        postotal = [countword, 1]


#Print total number of tags and all tags found
print("Total types of POS tags in data: ", seencount, "\n")
print("List of all tags: \n")
for item in sortseen :
    print(item)

print("----------------------------")
print("POS tag total counts: \n")
for total in totals:
    print(total)
print("----------------------------")
print("POS tag examples: \n")
for item in TagEx:
    print(item[0], ": ", item[1])
