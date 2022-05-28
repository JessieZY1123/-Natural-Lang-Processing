import os, string
import re
import codecs
import json

# Pre-process for the big dataset
home_dir = os.getcwd()
os.chdir(home_dir)
vocab = open("aclImdb/imdb.vocab", 'r', encoding="utf-8")
vocab_list = vocab.read().split()


# print(my_punctuation)

def get_vector_train(home_dir, file_directory, tag, coupus, vocab_list):
    os.chdir(file_directory)
    all_test_file = os.listdir(".")
    print(len(all_test_file))
    output_dict = []

    for file in list(all_test_file):
        if file.endswith('.txt'):
            inputfile = codecs.open(file, 'r', encoding="utf-8")
            line_list = inputfile.read().lower()
            line_without_pun = re.sub(r'[^\w\s\'\-]+', '', line_list).split()
            test_file_dict = dict()
            word_dict = dict()
            for word in line_without_pun:
                if word in vocab_list:
                    if word in word_dict:
                        word_dict[word] += 1
                    else:
                        word_dict[word] = 1
            test_file_dict[tag] = word_dict
            output_dict.append(test_file_dict)
    os.chdir(home_dir)
    outputFile = "movie-review-" + coupus + "-" + tag + ".NB"
    outputfile = codecs.open(outputFile, "w", encoding="utf-8")
    outputfile.write(json.dumps(output_dict, indent=6))
    outputfile.close()


def get_vector_test(home_dir, file_dir_pos, tag1, file_dir_neg, tag2, vocab_list):
    os.chdir(file_dir_pos)
    all_test_file_pos = os.listdir(".")
    print(len(all_test_file_pos))
    output_dict = []
    for file in all_test_file_pos:
        if file.endswith('.txt'):
            inputfile = codecs.open(file, 'r', encoding="utf-8")
            line_list = inputfile.read().lower()
            line_without_pun = re.sub(r'[^\w\s\'\-]+', '', line_list).split()

            test_file_dict_pos = dict()
            word_dict1 = dict()
            for word in line_without_pun:
                if word in vocab_list:
                    if word in word_dict1:
                        word_dict1[word] += 1
                    else:
                        word_dict1[word] = 1
            test_file_dict_pos[tag1] = word_dict1
            output_dict.append(test_file_dict_pos)
    os.chdir(home_dir)
    os.chdir(file_dir_neg)
    all_test_file_neg = os.listdir(".")
    print(len(all_test_file_neg))
    for file in all_test_file_neg:
        if file.endswith('.txt'):
            inputfile = codecs.open(file, 'r', encoding="utf-8")
            line_list = inputfile.read().lower()
            line_without_pun = re.sub(r'[^\w\s\'\-]+', '', line_list).split()
            word_dict2 = dict()
            test_file_dict_neg = dict()
            for word in line_without_pun:
                if word in vocab_list:
                    if word in word_dict2:
                        word_dict2[word] += 1
                    else:
                        word_dict2[word] = 1
            test_file_dict_neg[tag2] = word_dict2
            output_dict.append(test_file_dict_neg)
    # print(len(output_dict))
    os.chdir(home_dir)
    outputFile = "movie-review-test.NB"
    outputfile = codecs.open(outputFile, "w", encoding="utf-8")
    outputfile.write(json.dumps(output_dict, indent=6))
    outputfile.close()


#
get_vector_test(home_dir, "aclImdb/test/pos", "pos", "aclImdb/test/neg", "neg",vocab_list)
#
train_pos_dict = get_vector_train(home_dir, "aclImdb/train/pos", "pos", "train", vocab_list)
train_neg_dict = get_vector_train(home_dir, "aclImdb/train/neg", "neg", "train",vocab_list)
