import numpy as np
import csv


ORIGINAL_LABEL_PATH = "model with dev data as training/dev.col"
PREDICTED_LABEL_PATH = "dev-predict.col"

words = {}
indexes = {}
original_label =  {}
predicted_label =  {}
tagset = set([])
taglist = []
tag_index = {}

with open(ORIGINAL_LABEL_PATH) as csv_file: # file with original label
    csv_reader = csv.reader(csv_file, delimiter='\t')
    line_count = 0
    for row in csv_reader:
        if len(row) != 0:
            original_label[line_count] = row[1]
            words[line_count] = row[0]
            tagset.add(row[1])
        else:
            original_label[line_count] = 'STT'
            words[line_count] = '<S>'
            tagset.add('STT')
        line_count +=1

with open(PREDICTED_LABEL_PATH) as csv_file:  # file with predicted label
    csv_reader = csv.reader(csv_file, delimiter='\t')
    line_count = 0
    for row in csv_reader:
        if len(row) != 0:
            predicted_label[line_count] = row[1]
        else:
            predicted_label[line_count] = 'STT'
        line_count += 1

print(len(words))
print(len(original_label))
print(len(predicted_label))
print(len(tagset))

i = 0
for tag in tagset:
    tag_index[tag] = i
    taglist.append(tag)
    i+=1

cm = np.zeros((len(tagset), len(tagset)))
for i in range(len(words)):

    row = tag_index[original_label[i]]
    col = tag_index[predicted_label[i]]

    cm[row][col] = cm[row][col] + 1


print cm

from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt


def plot_confusion_matrix(cm, title='Confusion matrix', cmap=plt.cm.Blues):
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(tagset))
    plt.xticks(tick_marks, taglist, rotation=45)
    plt.yticks(tick_marks, taglist)
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')


# Compute confusion matrix
np.set_printoptions(precision=2)
print('Confusion matrix, without normalization')
print(cm)
plt.figure()
plot_confusion_matrix(cm)
plt.show()

