import csv
import json


TRAINING_PATH = "train.col"

words = {}
original_label =  {}
predicted_label =  {}
tagset = set([])
tag_count = {}
overall_counts = {}


print("Loading training data...")
# load the training data
with open(TRAINING_PATH) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='\t')
    i = 0
    for row in csv_reader:
        if len(row) != 0:
            original_label[i] = row[1]
            words[i] = row[0]
            tagset.add(row[1])
        else:
            original_label[i] = 'STT'
            words[i] = '<S>'
        i +=1

print(len(words))
print(len(tagset))

def save_tag_count(current_word_index):
    print("Saving tag count...")
    tag_count = {}
    for i in range(current_word_index):
        if original_label[i] in tag_count.keys():
            tag_count[original_label[i]] = tag_count[original_label[i]] + 1
        else:
            tag_count[original_label[i]] = 1

    with open(str(current_word_index)+' tag_count.txt', 'w') as tag_count_file:
        tag_count_file.write(json.dumps(tag_count))
        print(len(tag_count))
        print('done')


def save_model_count(dict_pos, current_word_index):
    print("Saving model...")
    with open(str(current_word_index)+' model.txt', 'w') as file:
        file.write(json.dumps(dict_pos))
        print(len(dict_pos))
        print(str(current_word_index) +' done')

# method to get the list of features of current word
def get_feature_list(i):

    global overall_counts
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

    for i in range(len(f)):
        if f[i] in overall_counts.keys():
            count = overall_counts[f[i]]
            overall_counts[f[i]] = count + 1
        else:
            overall_counts[f[i]] = 1

    return f


"""""
# count of feature given pos for every pos tag

dict_pos[pos_tag] = {} # 48 pos tags
dict_feature_given_pos[f_index] = {} # 13 features for each pos tag
dict_feature_count[feature_word] = {} # count of each features(ex. current word, next word) for each feature of each tag

"""""

dict_pos = {}
overall_counts = {}


# for each word
# get the features
# update the dictionary of each POS > feature_index=feature_token=token_count mapping
def get_count_of_features_per_pos():

    global dict_pos

    for i in range(len(words)):

        if(i % 1000) == 0:
            print("Saving the model at index " + str(i))
            save_model_count(dict_pos, i)
            save_tag_count(i)

        #       print(words[i])
        #       print(original_label[i])
        #       print("\n")

        f = get_feature_list(i)

        if original_label[i] in dict_pos.keys():

            temp_dict_feature_given_pos = dict_pos[original_label[i]]
            for f_index in range(len(temp_dict_feature_given_pos)):

                temp_feature_word_count_dict = temp_dict_feature_given_pos[f_index]

                if f[f_index] != 'nil':

                    if f[f_index] in temp_feature_word_count_dict.keys():

                        temp_feature_word_count = temp_feature_word_count_dict[f[f_index]]
                        temp_feature_word_count_dict[f[f_index]] = temp_feature_word_count + 1
                    else:

                        temp_feature_word_count_dict[f[f_index]] = 1

                temp_dict_feature_given_pos[f_index] = temp_feature_word_count_dict
            dict_pos[original_label[i]] = temp_dict_feature_given_pos

        else:

            temp_dict_feature_given_pos = {}
            temp_feature_word_count_dict = {}
            for f_index in range(len(f)):

                if f[f_index] != 'nil':

                    temp_feature_word_count_dict[f[f_index]] = 1

                temp_dict_feature_given_pos[f_index] = temp_feature_word_count_dict
            dict_pos[original_label[i]] = temp_dict_feature_given_pos


get_count_of_features_per_pos()
