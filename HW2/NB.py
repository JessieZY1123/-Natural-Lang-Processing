import math
import os
import re
import json
from pathlib import Path
# Make sure the home directory under the 'movie-review-HW2'
# To calculate the big dataset
home_dir = os.getcwd()
print(home_dir)
total_file = 0
outputfile = open("outputFile.txt", "w", encoding="utf-8")

path1 = Path(r"movie-review-train-pos.NB")
path2 = Path(r"movie-review-train-neg.NB")


# Get the number of file to calculate the prior probability
def get_number_of_file(file_directory, tag):
    os.chdir(file_directory)
    number_file = []
    file_list = list(f for f in os.listdir('.') if re.match(r'[0-9]+.*\.txt', f))
    number_of_file = len(file_list)
    number_file.append(tag)
    number_file.append(number_of_file)
    return number_file


pos_train_file = get_number_of_file("aclImdb/train/pos", "pos")

os.chdir(home_dir)
neg_train_file = get_number_of_file("aclImdb/train/neg", "neg")

total_files = pos_train_file[1] + neg_train_file[1]

p_prior_pos = pos_train_file[1] / total_files
p_prior_neg = neg_train_file[1] / total_files

os.chdir(home_dir)
vocab = open("aclImdb/imdb.vocab", 'r', encoding="utf-8")
vocab_list = list(vocab.read().split())
# print(vocab_list)
start_dict = {word: 0 for word in vocab_list}
os.chdir(home_dir)

# Combine each train dictionary to a big file, counting all words (BOW train dict)
def combine_each_file(parameter_file):
    inputfile = json.loads(open(parameter_file, "r", encoding="utf-8").read())
    total_dict = dict(start_dict)
    for i in inputfile:
        for key, value in i.items():
            for word in value:
                total_dict[word] += value[word]
    return total_dict

# Combine each train dictionary to a big file, only count each word once in each file.(Binary_NB train dict)
def combine_each_file_binary(parameter_file):
    inputfile = json.loads(open(parameter_file, "r", encoding="utf-8").read())
    total_dict = dict(start_dict)
    for i in inputfile:
        for key, value in i.items():
            for word in value:
                total_dict[word] += 1
    return total_dict


# To calculate probabilities of each test file
def compute_prob(prior, test_dict, total_train_dict, tag):
    prob = 0.0
    count_tag = sum(total_train_dict.values())
    # print(count_tag)

    result = 0
    for word in test_dict:
        if word in total_train_dict:
            prob = (total_train_dict[word] + 1) / (count_tag + len(vocab_list))
        else:
            prob = 1 / (count_tag + len(vocab_list))
        result += math.log2(prob) * test_dict[word]

    result = result + math.log2(prior)
    return result


def compute_prob_binary(prior, test_dict, total_train_dict, tag):
    prob = 0.0
    count_tag = sum(total_train_dict.values())
    # print(count_tag)

    result = 0
    for word in test_dict:
        if word in total_train_dict:
            prob = (total_train_dict[word] + 1) / (count_tag + len(vocab_list))
        else:
            prob = 1 / (count_tag + len(vocab_list))
        result += math.log2(prob)

    result = result + math.log2(prior)
    return result


# determine the tag of each test file, and compute the accuracy
def get_NB_classifier_tag(test_file, train_dict_file_pos, train_dict_file_neg):
    count_pos = 0
    count_neg = 0
    count_list = []
    count_list.append(count_pos)
    count_list.append(count_neg)
    for i in test_file:
        for key, value in i.items():
            pos_test_prob = compute_prob(p_prior_pos, value, train_dict_file_pos, "pos")
            # print("pos_prob: " + str(pos_test_prob))
            neg_test_prob = compute_prob(p_prior_neg, value, train_dict_file_neg, "neg")
            # print("neg_prob: " + str(neg_test_prob))
            test_file_cal_tag = []
            if pos_test_prob > neg_test_prob:
                test_file_cal_tag.append(key)
                test_file_cal_tag.append("pos")
                if key == "pos":
                    count_list[0] += 1
            else:
                test_file_cal_tag.append(key)
                test_file_cal_tag.append("neg")
                if key == "neg":
                    count_list[1] += 1
            outputfile.write(json.dumps(test_file_cal_tag) + '\n')
    match_file = count_list[0] + count_list[1]
    outputfile.write("The number of match file using BOW_NB is  " + str(match_file) + '\n')
    print("The number of match file using BOW_NB is  " + str(match_file))
    accuracy = (count_list[0] + count_list[1]) / len(test_file) * 100
    print("The BOW_NB accuracy is: " + str("%.3f" % accuracy) + "%")
    outputfile.write("The BOW_NB accuracy is " + str("%.3f" % accuracy) + "%"+'\n')
    return accuracy


def get_BinaryNB_classifier_tag(test_file, train_dict_file_pos, train_dict_file_neg):
    count_pos = 0
    count_neg = 0
    count_list = []
    count_list.append(count_pos)
    count_list.append(count_neg)
    for i in test_file:
        for key, value in i.items():
            pos_test_prob = compute_prob_binary(p_prior_pos, value, train_dict_file_pos, "pos")
            # print("pos_prob: " + str(pos_test_prob))
            neg_test_prob = compute_prob_binary(p_prior_neg, value, train_dict_file_neg, "neg")
            # print("neg_prob: " + str(neg_test_prob))
            test_file_cal_tag = []
            if pos_test_prob > neg_test_prob:
                test_file_cal_tag.append(key)
                test_file_cal_tag.append("pos")
                if key == "pos":
                    count_list[0] += 1
            else:
                test_file_cal_tag.append(key)
                test_file_cal_tag.append("neg")
                if key == "neg":
                    count_list[1] += 1
            # outputfile.write(json.dumps(test_file_cal_tag) + '\n')
    match_file = count_list[0] + count_list[1]
    outputfile.write("The number of match file using Binary_NB is " + str(match_file) + '\n')
    print("The number of match file using Binary_NB is " + str(match_file))
    accuracy = (count_list[0] + count_list[1]) / len(test_file) * 100
    print("The Binary_NB accuracy is: " + str("%.3f" % accuracy) + "%")
    outputfile.write("The Binary_NB accuracy is:" + str("%.3f" % accuracy) + "%")
    return accuracy


test_file = json.loads(open("movie-review-test.NB", "r", encoding="utf-8").read())

positive_train_dict = combine_each_file(path1)
negative_train_dict = combine_each_file(path2)

positive_train_dict_bin = combine_each_file_binary(path1)
negative_train_dict_bin = combine_each_file_binary(path2)

get_NB_classifier_tag(test_file, positive_train_dict, negative_train_dict)
get_BinaryNB_classifier_tag(test_file, positive_train_dict_bin, negative_train_dict_bin)

