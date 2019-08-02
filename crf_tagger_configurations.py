from nltk.corpus.reader import TaggedCorpusReader
from sklearn.cross_validation import train_test_split
import numpy as np
import re
from itertools import combinations
from collections import Counter

#based on: https://medium.com/analytics-vidhya/pos-tagging-using-conditional-random-fields-92077e5eaa31

def features(conf,sentence,index):
    ### sentence is of the form [w1,w2,w3,..], index is the position of the word in the sentence
    d = {'cur_word':sentence[index],
        'word_index':index,
        'is_first_capital':int(sentence[index][0].isupper()),
        'is_first_word': int(index==0),
        'is_last_word':int(index==len(sentence)-1),
        'is_complete_capital': int(sentence[index].upper()==sentence[index]),
        'prev_word':'' if index==0 else sentence[index-1],
        'prev_word2':'' if index<=1 else sentence[index-2],
        'next_word':'' if index==len(sentence)-1 else sentence[index+1],
        'next_word2':'' if index>=len(sentence)-2 else sentence[index+2],
        'is_numeric':int(sentence[index].isdigit()),
        'is_alphanumeric': int(bool((re.match('^(?=.*[0-9]$)(?=.*[a-zA-Z])',sentence[index])))),
        'prev_word_prefix_4':'' if index==0 else sentence[index-1][:4],
        'prev_word_suffix_4':'' if index==0 else sentence[index-1][-4:],
        'next_word_prefix_4':'' if index==len(sentence)-1 else sentence[index+1][:4],
        'next_word_suffix_4':'' if index==len(sentence)-1 else sentence[index+1][-4:],
        'prefix_1':sentence[index][0],
        'prefix_2':sentence[index][:2],
        'prefix_3':sentence[index][:3],
        'prefix_4':sentence[index][:4],
        'suffix_1':sentence[index][-1],
        'suffix_2':sentence[index][-2:],
        'suffix_3':sentence[index][-3:],
        'suffix_4':sentence[index][-4:],
        'word_has_hyphen': 1 if '-' in sentence[index] else 0}
    d_ = {k: v for k, v in d.items() if k in conf}

    return d_

"""
def features(sentence,index):
    ### sentence is of the form [w1,w2,w3,..], index is the position of the word in the sentence
    return {
        'cur_word':sentence[index],
        'is_numeric':int(bool(re.search('[0-9]+', sentence[index]))),
        'suffix_3':sentence[index][-3:],
        'prev_word':'' if index==0 else sentence[index-1],
         }
"""

def untag(sentence):
    return [word for word,tag in sentence]

def prepareData(conf,tagged_sentences):
    X,y=[],[]
    for sentences in tagged_sentences:
        X.append([features(conf, untag(sentences), index) for index in range(len(sentences))])
        y.append([tag for word,tag in sentences])
    return X,y

def helper(conf):
    X_train,y_train=prepareData(conf,train_set)
    X_test,y_test=prepareData(conf,test_set)

    from sklearn_crfsuite import CRF
    crf = CRF(
        algorithm='lbfgs',
        c1=0.01,
        c2=0.1,
        max_iterations=100,
        all_possible_transitions=True
    )
    crf.fit(X_train, y_train)

    from sklearn_crfsuite import metrics
    from sklearn_crfsuite import scorers
    y_pred=crf.predict(X_test)

    print("F1 score on Test Data ")
    f1_test = metrics.flat_f1_score(y_test, y_pred,average='weighted',labels=crf.classes_)
    print(str(f1_test.astype("str")))

    print("F score on Training Data ")
    y_pred_train=crf.predict(X_train)
    f_train = metrics.flat_f1_score(y_train, y_pred_train,average='weighted',labels=crf.classes_)
    print(str(f_train.astype("str")))

    ### Look at class wise score
    print(metrics.flat_classification_report(
        y_test, y_pred, digits=3
     ))

    with open("results/f1_dev_results"+str(len(conf))+".txt","a") as out:
        out.write(str(conf))
        out.write("\t")
        out.write(str(f1_test.astype("str")))
        out.write("\n")
        out.close()

    with open("results/f_train_results"+str(len(conf))+".txt","a") as out:
        out.write(str(conf))
        out.write("\t")
        out.write(str(f_train.astype("str")))
        out.write("\n")
        out.close()

    with open("results/class_report_dev_results"+str(len(conf))+".txt","a") as out:
        out.write(str(conf))
        out.write("\n")
        out.write(metrics.flat_classification_report(y_test, y_pred, digits=3))
        out.write("\n")
        out.close()

    print("\n\n")
    print("most common feature transitions")
    print(Counter(crf.transition_features_).most_common(100))
    print("\n\n")
    print("least common feature transitions")
    print(Counter(crf.transition_features_).most_common()[-100:])
    print("\n\n")
    print("most common state transitions")
    print(Counter(crf.state_features_).most_common(100))
    print("\n\n")
    print("least common state transitions")
    print(Counter(crf.state_features_).most_common()[-100:])

conf = ['cur_word', 'word_index', 'is_first_capital', 'is_first_word', 'is_last_word', 'is_complete_capital', 'prev_word_prefix_4', 'prev_word_suffix_4', 'next_word_prefix_4', 'next_word_suffix_4', 'prev_word', 'prev_word2', 'next_word', 'next_word2', 'is_numeric', 'is_alphanumeric', 'prefix_1', 'prefix_2', 'prefix_3', 'prefix_4', 'suffix_1', 'suffix_2', 'suffix_3', 'suffix_4', 'word_has_hyphen']

configurations = list(combinations(conf,len(conf)))

for i in range(0,len(configurations)):
    corpora_root = "corpora"
    corp = TaggedCorpusReader(corpora_root,".txt")

    tagged_sentence = corp.tagged_sents("train.txt")
    tagged_sentence_dev = corp.tagged_sents("test.txt")

    # print("Number of Tagged Sentences ",len(tagged_sentence))
    # tagged_words=[tup for sent in tagged_sentence for tup in sent]
    # print("Total Number of Tagged words", len(tagged_words))
    # vocab=set([word for word,tag in tagged_words])
    # print("Vocabulary of the Corpus",len(vocab))
    # tags=set([tag for word,tag in tagged_words])
    # print("Number of Tags in the Corpus ",len(tags))

    #train_set, test_set = train_test_split(tagged_sentence,test_size=0.2,random_state=1234)
    train_set = tagged_sentence
    test_set = tagged_sentence_dev
    print(list(configurations[i]))
    helper(list(configurations[i]))