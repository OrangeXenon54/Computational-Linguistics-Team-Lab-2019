import csv

words = {}
original_label =  {}
predicted_label =  {}
tagset = set([])

with open('dev.col') as csv_file:
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
        line_count +=1

with open('dev-predicted.col') as csv_file:
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

# A macro-average will compute the metric independently for each class and then take the average (hence treating all classes equally), whereas a micro-average will aggregate the contributions of all classes to compute the average metric.
# In a multi-class classification setup, micro-average is preferable if you suspect there might be class imbalance



micro_tp = 0
micro_fn = 0
micro_fp = 0

def fscore_function(pos):
    global micro_tp
    global micro_fn
    global micro_fp

    tp = 0
    tn = 0
    fp = 0
    fn = 0

    precision = 0
    recall = 0
    fscore = 0

    for i in words:
      if original_label[i] == pos:
          if predicted_label[i] == pos:
              tp+= 1
          else:
              fn+= 1

      else:
          if predicted_label[i] == pos:
              fp+= 1
          else:
              tn+=1

    print(str(tp) + " " + str(tn) + " " + str(fp) + " " + str(fn))

    micro_tp+= tp
    micro_fn+= fn
    micro_fp+= fp

    if tp+fp != 0:
        precision = float(tp/float(tp+fp))
        print('P : ' + str(precision))
    else:
        print('precission cannot be calculated, tp+fp = 0')

    if tp+fn != 0:
        recall = float(tp/float(tp+fn))
        print('R : ' + str(recall))
    else:
        print('recall cannot be calculated,  tp+fn = 0')

    if precision+recall == 0:
        fscore = 0
    else:
        fscore = 2*float(float(recall * precision) / float(recall + precision))
        print('F :' + str(fscore))

for tag in tagset:
    if len(tag) > 0:
        print(tag)
        fscore_function(tag)
        print('____________________________')


print('Micro avg')
def micro_function(tp, fn, fp):
    print(str(tp) + " " + str(fp) + " " + str(fn))
    precision = float(tp/float(tp+fp))
    recall = float(tp/float(tp+fn))

    print('P : ' + str(precision))
    print('R : ' + str(recall))

    fscore = 0

    if precision + recall == 0:
        fscore = 0
    else:
        fscore = 2 * float(float(recall * precision) / float(recall + precision))
        print('F :' + str(fscore))


micro_function(micro_tp, micro_fn, micro_fp)