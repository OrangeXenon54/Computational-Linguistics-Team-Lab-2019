from nltk.corpus.reader import TaggedCorpusReader
from sklearn.model_selection import train_test_split
import numpy as np
import re

#based on: https://medium.com/analytics-vidhya/pos-tagging-using-conditional-random-fields-92077e5eaa31

corpora_root = "corpora"
corp = TaggedCorpusReader(corpora_root,".txt")

tagged_sentence = corp.tagged_sents("train.txt")
tagged_sentence_dev = corp.tagged_sents("test.txt")

print("Number of Tagged Sentences ",len(tagged_sentence))
tagged_words=[tup for sent in tagged_sentence for tup in sent]
print("Total Number of Tagged words", len(tagged_words))
vocab=set([word for word,tag in tagged_words])
print("Vocabulary of the Corpus",len(vocab))
tags=set([tag for word,tag in tagged_words])
print("Number of Tags in the Corpus ",len(tags))

#train_set, test_set = train_test_split(tagged_sentence,test_size=0.2,random_state=1234)
train_set = tagged_sentence
test_set = tagged_sentence_dev

print("Number of Sentences in Training Data ",len(train_set))
print("Number of Sentences in Testing Data ",len(test_set))


def features(sentence,index):
    ### sentence is of the form [w1,w2,w3,..], index is the position of the word in the sentence

    return {
        'cur_word':sentence[index],
        'is_first_capital':int(sentence[index][0].isupper()),
        'is_first_word': int(index==0),
        'is_last_word':int(index==len(sentence)-1),
        'is_complete_capital': int(sentence[index].upper()==sentence[index]),
        'prev_word':'' if index==0 else sentence[index-1],
        'next_word':'' if index==len(sentence)-1 else sentence[index+1],
        'is_numeric':int(sentence[index].isdigit()),
        'is_alphanumeric': int(bool((re.match('^(?=.*[0-9]$)(?=.*[a-zA-Z])',sentence[index])))),
        'prefix_1':sentence[index][0],
        'prefix_2': sentence[index][:2],
        'prefix_3':sentence[index][:3],
        'prefix_4':sentence[index][:4],
        'suffix_1':sentence[index][-1],
        'suffix_2':sentence[index][-2:],
        'suffix_3':sentence[index][-3:],
        'suffix_4':sentence[index][-4:],
        'word_has_hyphen': 1 if '-' in sentence[index] else 0
         }

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


def prepareData(tagged_sentences):
    X,y=[],[]
    for sentences in tagged_sentences:
        X.append([features(untag(sentences), index) for index in range(len(sentences))])
        y.append([tag for word,tag in sentences])
    return X,y
X_train,y_train=prepareData(train_set)
X_test,y_test=prepareData(test_set)

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
print(metrics.flat_f1_score(y_test, y_pred,average='weighted',labels=crf.classes_))
print("F score on Training Data ")
y_pred_train=crf.predict(X_train)
metrics.flat_f1_score(y_train, y_pred_train,average='weighted',labels=crf.classes_)

### Look at class wise score
print(metrics.flat_classification_report(
    y_test, y_pred, digits=3
))
