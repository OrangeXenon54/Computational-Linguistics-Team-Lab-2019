import re
#Returns a readable version of data, a list of lists with [0] being a list of tuples of the data and [1] being list of contained tags
#Argument is a text file that breaks down into a list of strings
def GoldData(datafile) :
    golddata = []
    data = []
    POS = []
    for line in datafile:
        if line == "\n" :
            ttup = ("\n", "NULL")
            data.append(ttup)
        else :
            stripped = line.strip()
            word = re.findall('(^.+)\t', stripped)[0]
            tag = re.findall('\t(.+$)', stripped)[0]
            ttup = (word, tag)
            data.append(ttup)
            if tag not in POS :
                POS.append(tag)
    golddata.append(data)
    POS.sort()
    golddata.append(POS)
    return golddata

#Returns: 1.) dictionary with key being POS tags and value being a list with [0] = TP [1] = FN [2] = FP
# 2.) dictionary of dictionaries where the first key is a POS tag, 2nd key is another POS tag, and the value is a list of tokens it got confused with
#Takes as an argument a tag list of all gold data tags and the gdata and predicted data
def tpfnfp(POS, gdata, pdata) :
    fdict = {}
    conf = {}
    #Creating dictionaries
    for i in POS :
        fdict[i] = [0, 0, 0]
        conf[i] = {}
        for x in POS :
            if x != i :
                conf[i][x] = []
    for gi in gdata :
        pi = pdata.pop(0)
        #Extracting the tags
        gt = gi[1]
        pt = pi[1]
        tok = gi[0]
        #Skipping newlines
        if tok == "\n":
            continue
        else:
            #Match aka true positive
            if gt == pt :
                fdict[gt][0] += 1
            #Mismatch, so update 1.) fdict with fn in gt's and fp in pt's 2.) the confusion matrix with conf[gt][pt] = tok
            else :
                fdict[gt][1] += 1
                fdict[pt][2] += 1
                conf[gt][pt].append(tok)
                conf[pt][gt].append(tok)
    dicts = [fdict, conf]
    return dicts

#Doesn't return anything. Calculates results, writes them to file, and prints it out
#Takes as an argument sorted tag list, dictionary of TPs, FNs, and FPs, and file name
def theResults(POS, dict, conf, fname):
    #TI = total instances of tag within gold data, TT = total tagged aka TP, TM = total missed aka FN
    hline = "Tag\tPrecision\tRecall\tF-Score\tConfT\tTI\tTP\tFN\tFP\n"
    print("Tag\tPrec\tRec\tF1\tConfT\tTI\tTP\tFN\tFP\n---\t---\t---\t---\t---\t---\t---\t---\t---")
    newname = "RESULTS" + fname
    newfile = open(newname, "w+")
    newfile.write(hline)
    tti = 0
    ttp = 0
    tfn = 0
    tfp = 0
    for i in POS :
        tp = float(dict[i][0])
        fn = float(dict[i][1])
        fp = float(dict[i][2])
        ti = dict[i][0] + dict[i][1]
        inttp = dict[i][0]
        intfn = dict[i][1]
        intfp = dict[i][2]
        tti += ti
        ttp += inttp
        tfn += intfn
        tfp += intfp
        precision = "NULL"
        recall = "NULL"
        f1score = "NULL"
        if (tp + fp) != 0:
            precision = tp / (tp + fp)
            precision = round(precision, 4)
        if (tp + fn) != 0:
            recall = tp / (tp + fn)
            recall = round(recall, 4)
        if  precision == "NULL" or recall == "NULL" or (precision + recall) == 0:
            f1score == "NULL"
        else:
            f1score = (2 * precision * recall) / (precision + recall)
            f1score = round(f1score, 4)
        clen = 0
        ctag = "NONE"
        for k,v in conf[i].items() :
            if len(v) > clen :
                clen = len(v)
                ctag = k
        line = i+"\t"+str(precision)+"\t"+str(recall)+"\t"+str(f1score)+"\t"+ctag+"\t"+str(ti)+"\t"+str(inttp)+"\t"+str(intfn)+str(intfp)+"\n"
        print(i,"\t",precision,"\t",recall,"\t",f1score,"\t",ctag,"\t",ti,"\t",inttp,"\t",intfn,"\t",intfp,"\t")
        newfile.write(line)
    tprec = ttp / (ttp + tfp)
    tprec = round(tprec, 4)
    trec = ttp / (ttp + tfn)
    trec = round(trec, 4)
    tf1 = (2 * tprec * trec) / (tprec + trec)
    tf1 = round(tf1, 4)
    lline = "M-AV\t"+str(tprec)+"\t"+str(trec)+"\t"+str(tf1)+"\t"+"N/A"+"\t"+str(tti)+"\t"+str(ttp)+"\t"+str(tfn)+"\t"+str(tfp)+"\n"
    print("---\t---\t---\t---\t---\t---\t---\t---\t---\nM-AV\t",tprec,"\t",trec,"\t",tf1,"\t","N/A","\t",tti,"\t",ttp,"\t",tfn,"\t",tfp)
    newfile.write(lline)
    newfile.close()

gname = "test.col"
gopen = open(gname)
gold = GoldData(gopen)
goldd = gold[0]
goldp = gold[1]
pname = "BLPerceptronpredicted-"+gname
popen = open(pname)
pred = GoldData(popen)
predd = pred[0]
predp = pred[1]
for i in predp :
    if i not in goldp :
        goldp.append(i)
        print(i," was not in the gold data tags")
goldp.sort()
res = tpfnfp(goldp, goldd, predd)
result = res[0]
confusion = res[1]
theResults(goldp, result, confusion, pname)
