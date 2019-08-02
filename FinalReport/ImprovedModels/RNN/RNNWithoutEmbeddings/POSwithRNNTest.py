# later...
import csv

from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json
import os

from sklearn.model_selection import train_test_split
from keras.preprocessing.sequence import pad_sequences

from keras.models import Sequential
from keras.layers import Dense, LSTM, InputLayer, Bidirectional, TimeDistributed, Embedding, Activation
from keras.optimizers import Adam

import numpy as np

import json

with open('word2index.json', 'r') as fp:
    word2index = json.load(fp)

with open('tag2index.json', 'r') as fp:
    tag2index = json.load(fp)
    

with open('MAX_LENGTH.json', 'r') as fp:
    MAX_LENGTH = json.load(fp)

# load json and create model
json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
# load weights into new model
model.load_weights("model.h5")
print("Loaded model from disk")


test_samples = []
#load test file, with original label
original_label = {}
words = {}
with open("dev.col") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='\t')
    i = 0
    sentence=[]
    for row in csv_reader:
        if len(row) != 0:
            original_label[i] = row[1]
            words[i] = row[0]
            sentence.append(row[0])
        else:
            original_label[i] = 'STT'
            words[i] = '<S>'

            test_samples.append(sentence)
            sentence = []
        i +=1

print(test_samples)


test_samples_X = []
for s in test_samples:
    s_int = []
    for w in s:
        try:
            s_int.append(word2index[w.lower()])
        except KeyError:
            s_int.append(word2index['-OOV-'])
    test_samples_X.append(s_int)
 
test_samples_X = pad_sequences(test_samples_X, maxlen=MAX_LENGTH, padding='post')
print(test_samples_X)

predictions = model.predict(test_samples_X)
print(predictions, predictions.shape)

def logits_to_tokens(sequences, index):
	token_sequences = []
	i = 0
	for categorical_sequence in sequences:
	  	token_sequence = []
		for categorical in categorical_sequence:
		  #if (index[np.argmax(categorical)] != "-PAD-"):
		  token_sequence.append(index[np.argmax(categorical)])
		token_sequences.append(token_sequence[:len(test_samples[i])])
		i+=1

	return token_sequences

sentences_tagged = logits_to_tokens(predictions, {i: t for t, i in tag2index.items()})

print(len(test_samples))
print(len(sentences_tagged))

# create a file to write predicted result from test file
f = open("dev-predicted.col", "w")

for i in range(len(test_samples)):
	sentence = test_samples[i]
	tag_sentence = sentences_tagged[i]

	print sentence
	print tag_sentence
	print '\n'

	for j in range(len(sentence)):
		if len(' '.join(sentence[j].split())) > 0:
			f.write(sentence[j] + "\t" +  tag_sentence[j]+'\n')
		else:
			f.write("\n")
	f.write("\n")

