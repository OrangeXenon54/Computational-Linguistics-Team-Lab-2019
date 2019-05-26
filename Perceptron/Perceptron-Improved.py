import operator
import re

#Built based on: https://towardsdatascience.com/6-steps-to-write-any-machine-learning-algorithm-from-scratch-perceptron-case-study-335f638a70f3
def Perceptron(feature,result,activation=0.0,learning_rate=0.1,epochs=23):
    #weight dict consisting of feature:weight pairs
    w = {}
    
    for e in range(0,epochs):
        for n in range(0,len(feature)):
            #f = calculated dot product of weights and features(input)

            f = 0.
            for k,v in feature[n].items():
                if k not in w:
                    w[k] = 0.
                f += w[k]*v

            #triggers activation function if f > activation
            if f > activation:
                yhat = 1.
            else:
                yhat = 0.

            #adapt weights only for current active features
            for k in feature[n]:
                w[k] = w[k] + learning_rate*(result[n] - yhat)*feature[n][k]

    return w

#Returns a list of lists with the list consisting of the token -a string -and its features -a set
#Argument is a list of strings

# BIAS
# Current token
# Current token suffix(3 chars)
# Current token is_number
# Previous token

# To add, ideas:
# Length previous word - next word
# Sentence position?
# suffix, next word?
# is capitalized?

def FeatureChecker(prev,token):
    d = {}

    #BIAS
    d["b_bias"] = 1.
    #Current token
    d["cw_"+token] = 1.
    #Current token suffix(3 chars)
    if len(token) >= 5:
        d["cw-suf_"+token[-3:]] = 1.
    #Current token contains numerical character
    if re.search('[0-9]+', token):
        d["n_num"] = 1.
    #previous token
    d["pw_"+prev] = 1.

    return d

# train perceptron
# output = trained weights for each pos
def train(file):
    #get all pos of train dataset
    unique_pos = set()
    with open(file) as f:
        for l in f:
            if l != "\n":
                pos = l.split("\t")[1].strip()
                unique_pos.add(pos)

    result = {}
    for p in unique_pos:
        result[p] = [[],[]]

    progress_count = 1
    #read train file
    prev = "."
    with open(file) as f:
        for l in f:
            if l != "\n":
                token = l.split("\t")[0].strip()
                pos = l.split("\t")[1].strip()

                print("learning @line: "+str(progress_count))
                progress_count += 1
                #add features and results
                for k,v in result.items():
                    featcheck = FeatureChecker(prev,token)
                    if k == pos:
                        result.get(k)[0].append(featcheck)
                        result.get(k)[1].append(1.)
                    else:
                        result.get(k)[0].append(featcheck)
                        result.get(k)[1].append(0.)
                prev = token

    progress_count = 1
    #calculate perceptron weights
    for k,v in result.items():
        print("calculating perceptron "+str(progress_count)+"/"+str(len(result)))
        progress_count += 1
        result[k] = Perceptron(result.get(k)[0],result.get(k)[1])
        
    return result

def predict(file,pos_weights):
    progress_count = 1
    predict_dataset = open(file,"r")
    out = open("ImprovedP-Predicted-"+file,"w")
    
    sentences = []
    sent_tmp = []

    #read file to be predicted
    for line in predict_dataset:
        token = line.split("\t")[0]
        if token != "\n":
            sent_tmp.append(token)
        if token == "\n":
            sentences.append(sent_tmp)
            sent_tmp = []

    progress_count = 0
    for i in range(0,len(sentences)):
        for j in range(0,len(sentences[i])):
            print("predicting @line: "+str(progress_count))
            progress_count += 1
            #we store the results of the dot product (weight + cur features)
            #in multi_class and the corresponding pos tag in multi_class_pos
            multi_class = []
            multi_class_pos = []
            for pos,weight in pos_weights.items():
                dot = 0.
                if j >= 1:
                    current_feat = FeatureChecker(sentences[i][j-1],sentences[i][j])
                else:
                    current_feat = FeatureChecker(".",sentences[i][j])

                #compute the dot product
                for k,v in current_feat.items():
                    if k in weight:
                        dot += v*weight[k]
                        
                multi_class.append(dot)
                multi_class_pos.append(pos)
            #get the highest result (strongest weights) --> pos
            index,value = max(enumerate(multi_class),key=operator.itemgetter(1))
            out.write(sentences[i][j]+"\t"+multi_class_pos[index]+"\n")
        out.write("\n")
    out.close()

if __name__ == "__main__":
    pos_weight = train("train.col")
    predict("dev.col",pos_weight)