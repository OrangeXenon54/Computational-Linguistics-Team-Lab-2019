import re

filename = input("Please type file name:")

devtext = open(filename)

allpos = []
seen = set()
print(len(seen))
examples = []

for line in devtext :
    if line == "\n" :
        continue
    else :
        stripped = line.strip()
        # WTF am I thinking? postag = re.search('\s(.*)$', stripped)
        postag = stripped.split()[1]
        allpos.append(postag)
        if postag not in seen :
            seen.add(postag)
            examples.append(stripped)
        else :
            continue

sortpos = sorted(allpos)
totals = []
countword = None

for pos in sortpos :
    if countword is None :
        countword = pos
        postotal = [countword, 1]
    elif countword == pos :
            postotal[1] = postotal[1] + 1
    else :
        totals.append(postotal)
        countword = pos
        postotal = [countword, 1]

seencount = len(seen) - 1
print("Total types of POS tags in data: ", seencount, "\n")
print("POS tag total counts: \n")
for total in totals:
    print(total, "\n")
print("POS tag examples: 'n")
for item in examples:
    print(item, "\n")
