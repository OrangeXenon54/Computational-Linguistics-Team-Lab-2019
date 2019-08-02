pathy = "corpora/test.txt"
filename = "test.col"
out = open(pathy,"w")

with open(filename) as f:
    for l in f:
        if l != "\n":
            token = l.split("\t")[0].strip()
            pos = l.split("\t")[1].strip()
            out.write(token+"/"+pos)
            out.write(" ")
        else:
            out.write("\n")

out.close()
