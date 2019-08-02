import re
#Returns a readable version of the gold data, a list of lists with [0] being the token and [1] being the POS
#Argument is a text file that breaks down into a list of strings
def GoldData(datafile) :
    golddata = []
    for line in datafile:
        if line == "\n" :
            golddata.append(line)
        else :
            stripped = line.strip()
            word = re.findall('(^\S*?)\s', stripped)[0]
            tag = re.findall('\s(\S*?$)', stripped)[0]
            ttup = (word, tag)
            golddata.append(ttup)
    return golddata

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

#Creates a dictionary where the key is the POS tag the target word appears as and the value is a list of sentence strings
def ContextFinder(targ, sents) :
    tags = {}
    context = {}
    for s in sents:
        foundit = False
        ftag = str()
        for w in s:
            if targ == w[0] :
                ftag = w[1]
                foundit = True
                break
        if foundit == True :
            fs = "|"
            ind = 1
            max = len(s)
            for w in s :
                word = w[0]
                if ind == max :
                    fs += word+"|"
                else :
                    if word == targ :
                        word = "***"+word+"***"
                        fs += " "+word
                        ind += 1
                    else:
                        fs += " "+word
                        ind += 1
            if ftag not in tags:
                context[ftag] = [fs]
                tags[ftag] = 1
            else:
                context[ftag].append(fs)
                tags[ftag] += 1
    fullstory = (context, tags)
    return fullstory


fname = input("Please enter file name: ")
target = input("Please input the token you wish to find (case sensitive): ")
print("**********\nProcessing Data\n**********\n")
file = open(fname)
gd = GoldData(file)
sentences = SenList(gd)
fulls = ContextFinder(target, sentences)
if len(fulls[0]) < 1:
    print("Token not found")
else :
    con = fulls[0]
    tagd = fulls[1]
    taglist = []
    for k,v in tagd.items():
        taglist.append(k)
    taglist.sort()
    print("That token appears as the following tags :")
    for i in taglist:
        print(i,"\t",tagd[i])
    while True:
        smtag = input("Which tags sentences would you like to see? NOTE: Will only show a maximum of 10 sentences per tag - ")
        if smtag not in tagd :
            print("Good bye!")
            break
        else :
            if len(con[smtag]) <= 10 :
                for items in con[smtag]:
                    print(items)
            else :
                sens = con[smtag][:10]
                for items in sens :
                    print(items)
