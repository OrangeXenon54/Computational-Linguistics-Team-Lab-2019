import csv
from numpy import asarray
from numpy import zeros
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

TRAIN_PATH = "train.col"

words = {}
original_label =  {}
predicted_label =  {}
tagset = set([])


sentences = []
sentence = []

sentence_tags = []
sentence_tag = []


with open(TRAIN_PATH) as csv_file: # file with original label
    csv_reader = csv.reader(csv_file, delimiter='\t')
    line_count = 0


    for row in csv_reader:

        if len(row) != 0:
            original_label[line_count] = row[1]
            words[line_count] = row[0]
            tagset.add(row[1])

            sentence.append(row[0])
            sentence_tag.append(row[1])
        else:
            original_label[line_count] = 'STT'
            words[line_count] = '<S>'

            sentences.append(sentence)
            sentence_tags.append(sentence_tag)

            sentence = []
            sentence_tag = []

        line_count +=1

print sentences[5]
print sentence_tags[5]
 
(train_sentences,test_sentences,train_tags,test_tags) = train_test_split(sentences, sentence_tags, test_size=0.2)

words, tags = set([]), set([])
 
for s in train_sentences:
    for w in s:
        words.add(w.lower())
 
for ts in train_tags:
    for t in ts:
        tags.add(t)
 
word2index = {w: i + 2 for i, w in enumerate(list(words))}
word2index['-PAD-'] = 0  # The special value used for padding
word2index['-OOV-'] = 1  # The special value used for OOVs
 
tag2index = {t: i + 1 for i, t in enumerate(list(tags))}
tag2index['-PAD-'] = 0  # The special value used to padding


import json
with open('word2index.json', 'w') as fp:
    json.dump(word2index, fp)

print "word2index saved"

with open('tag2index.json', 'w') as fp:
    json.dump(tag2index, fp)

print "tag2index saved"

train_sentences_X, test_sentences_X, train_tags_y, test_tags_y = [], [], [], []
 
for s in train_sentences:
    s_int = []
    for w in s:
        try:
            s_int.append(word2index[w.lower()])
        except KeyError:
            s_int.append(word2index['-OOV-'])
 
    train_sentences_X.append(s_int)
 
for s in test_sentences:
    s_int = []
    for w in s:
        try:
            s_int.append(word2index[w.lower()])
        except KeyError:
            s_int.append(word2index['-OOV-'])
 
    test_sentences_X.append(s_int)
 

for s in train_tags:
    train_tags_y.append([tag2index[t] for t in s])

for s in test_tags:
    test_tags_y.append([tag2index[t] for t in s])


print(train_sentences_X[0])
print(test_sentences_X[0])
print(train_tags_y[0])
print(test_tags_y[0])

MAX_LENGTH = len(max(train_sentences_X, key=len))
print(MAX_LENGTH)  # 271

with open('MAX_LENGTH.json', 'w') as fp:
    json.dump(MAX_LENGTH, fp)

print "MAX_LENGTH saved"

from keras import backend as K
 
def ignore_class_accuracy(to_ignore=0):
    def ignore_accuracy(y_true, y_pred):
        y_true_class = K.argmax(y_true, axis=-1)
        y_pred_class = K.argmax(y_pred, axis=-1)
 
        ignore_mask = K.cast(K.not_equal(y_pred_class, to_ignore), 'int32')
        matches = K.cast(K.equal(y_true_class, y_pred_class), 'int32') * ignore_mask
        accuracy = K.sum(matches) / K.maximum(K.sum(ignore_mask), 1)
        return accuracy
    return ignore_accuracy
 
train_sentences_X = pad_sequences(train_sentences_X, maxlen=MAX_LENGTH, padding='post')
test_sentences_X = pad_sequences(test_sentences_X, maxlen=MAX_LENGTH, padding='post')
train_tags_y = pad_sequences(train_tags_y, maxlen=MAX_LENGTH, padding='post')
test_tags_y = pad_sequences(test_tags_y, maxlen=MAX_LENGTH, padding='post')
 
print(train_sentences_X[0])
print(test_sentences_X[0])
print(train_tags_y[0])
print(test_tags_y[0])

# load the whole embedding into memory
embeddings_index = dict()
f = open('glove.6B.300d.txt')
for line in f:
    values = line.split()
    word = values[0]
    coefs = asarray(values[1:], dtype='float32')
    embeddings_index[word] = coefs
f.close()
print('Loaded %s word vectors.' % len(embeddings_index))

vocab_size = len(embeddings_index)

# create a weight matrix for words in training docs
i=0
embedding_matrix = zeros((vocab_size, 300))
for word in words:
    embedding_vector = embeddings_index.get(word)
    if embedding_vector is not None:
        embedding_matrix[i] = embedding_vector
        i+=1

print('create a weight matrix for words in training docs')

 
model = Sequential()
model.add(InputLayer(input_shape=(MAX_LENGTH, )))
model.add(Embedding(vocab_size, 300, weights=[embedding_matrix], input_length=MAX_LENGTH, trainable=False))
model.add(Bidirectional(LSTM(256, return_sequences=True)))
model.add(TimeDistributed(Dense(len(tag2index))))
model.add(Activation('relu'))
 
model.compile(loss='categorical_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy', ignore_class_accuracy(0)])
 
model.summary()


def to_categorical(sequences, categories):
    cat_sequences = []
    for s in sequences:
        cats = []
        for item in s:
            cats.append(np.zeros(categories))
            cats[-1][item] = 1.0
        cat_sequences.append(cats)
    return np.array(cat_sequences)

cat_train_tags_y = to_categorical(train_tags_y, len(tag2index))
print(cat_train_tags_y[0])

model.fit(train_sentences_X, to_categorical(train_tags_y, len(tag2index)), batch_size=128, epochs=40, validation_split=0.2)


scores = model.evaluate(test_sentences_X, to_categorical(test_tags_y, len(tag2index)))
print(scores[1] * 100)   # acc: 99.09751977804825


# serialize model to JSON
model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights("model.h5")
print("Saved model to disk")

