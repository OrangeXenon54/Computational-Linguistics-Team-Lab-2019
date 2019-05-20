import json
import math
import csv


#resource paths
MODEL_PATH = "7000 model.txt"
TAG_COUNT_PATH = "7000 tag_count.txt"
TEST_PATH = 'model with dev data as training/test.col'
RESULT_PATH = 'result_on_small.col'


# load the model
dict_pos = json.load(open(MODEL_PATH))

print(len(dict_pos))
print('done')

#load tag counts, for calculating  probabilities
dict_tag_count = json.load(open(TAG_COUNT_PATH))

print(len(dict_tag_count))
print('done')

#load test file, with original label
original_label = {}
words = {}
with open(TEST_PATH) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='\t')
    i = 0
    for row in csv_reader:
        if len(row) != 0:
            original_label[i] = row[1]
            words[i] = row[0]
        else:
            original_label[i] = 'STT'
            words[i] = '<S>'
        i +=1

print(len(words))
print(len(dict_pos))


# function to get features of current word
def get_feature_list(i):

    global words
    f_index = 0
    f = {}

    try:
        f[f_index] = words[i]
    except:
        f[f_index] = 'nil'

    f_index += 1

    try:
        f[f_index] = words[i] + words[i - 1]
    except:
        f[f_index] = 'nil'
    f_index += 1

    try:
        f[f_index] = words[i] + words[i - 2]
    except:
        f[f_index] = 'nil'
    f_index += 1

    try:
        f[f_index] = words[i] + words[i - 1] + words[i - 2]
    except:
        f[f_index] = 'nil'
    f_index += 1

    try:
        f[f_index] = words[i] + words[i + 1]
    except:
        f[f_index] = 'nil'
    f_index += 1

    try:
        f[f_index] = words[i] + words[i + 2]
    except:
        f[f_index] = 'nil'
    f_index += 1

    try:
        f[f_index] = words[i] + words[i + 1] + words[i + 2]
    except:
        f[f_index] = 'nil'
    f_index += 1

    try:
        f[f_index] = words[i + 1]
    except:
        f[f_index] = 'nil'
    f_index += 1

    try:
        f[f_index] = words[i + 1] + words[i + 2]
    except:
        f[f_index] = 'nil'
    f_index += 1

    try:
        f[f_index] = words[i - 1]
    except:
        f[f_index] = 'nil'
    f_index += 1

    try:
        f[f_index] = words[i - 1] + words[i - 2]
    except:
        f[f_index] = 'nil'
    f_index += 1

    try:
        f[f_index] = words[i - 1] + words[i + 1]
    except:
        f[f_index] = 'nil'
    f_index += 1

    try:
        f[f_index] = words[i - 2] + words[i - 1] + words[i + 1] + words[i + 2]
    except:
        f[f_index] = 'nil'
    f_index += 1

    return f


# create a file to write predicted result from test file
f = open(RESULT_PATH, "w")


# for each word
# get features
# calculate probability using model for each POS of that word
# take the argmax
for word_index in range(len(words)):

    feature_map = get_feature_list(word_index)
    probability_feature_score = {}
    pos_score = {}

    for pos in dict_pos.keys():

        total_pos_count_i = dict_tag_count[pos]
        feature_map_pre = dict_pos[pos]
        probability_feature_score_list = []

        # print pos
        #print feature_map_pre
        for f_index in range(len(feature_map)):
            if feature_map[f_index] in feature_map_pre[str(f_index)] and feature_map[f_index] != 'nil':
                conditional_count_score = feature_map_pre[str(f_index)][feature_map[f_index]]
                probability_feature_score_list.append(float(math.log(conditional_count_score)-math.log(total_pos_count_i)))

        if sum(probability_feature_score_list)!= 0:
            pos_score[pos] = sum(probability_feature_score_list)
          #  print pos_score[pos]
        else:
            pos_score[pos] = 10000

    pos_score_sorted_keys = sorted(pos_score, key=pos_score.get, reverse=False)

    """""
    print(" ")
    print words[word_index]
    print original_label[word_index]
    print pos_score_sorted_keys[0]
    print pos_score[pos_score_sorted_keys[0]]
    print(" ")
    """""

    if words[word_index] != '<S>':
        f.write(words[word_index] + "\t" +  pos_score_sorted_keys[0]+'\n')
    else:
        f.write("\n")


""""" p(pos_i|features) = p(f_1|pos_i) * ... * p(f_n|pos_i) * p(pos_i)
                        = c(f_1 | pos_i)/c(f_1) *..... * c(f_n|pos_i)/c(f_n) * c(pos_i)* c(pos)        
"""""
