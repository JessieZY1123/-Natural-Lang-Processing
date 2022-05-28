import os,sys
import re
import string
import json
# Pre-process file of small corpus
home_dir = os.getcwd()
# print(home_dir)
vocab = open("example/example.vocab", 'r', encoding="utf-8")
vocab_list = list(vocab.read().split())

def get_vector_all(home_dir, file_directory, tag):
    os.chdir(file_directory)
    all_test_file = os.listdir(".")

    test_list = []
    word_dict = dict()
    for file in all_test_file:
        if file.endswith('.txt'):
            inputfile = open(file, 'r', encoding="utf-8")
            for line in inputfile:
                line = line.lower()
                line_without_pun = re.sub(r'[^\w\s]', '', line).split()
                test_list = test_list + line_without_pun
    # print(test_list)
    os.chdir(home_dir)
    vocab = open("example/example.vocab", 'r', encoding="utf-8")
    vocab_list = list(vocab.read().split())

    for word in test_list:
        if word in vocab_list:
            if word in word_dict:
                word_dict[word] += 1
            else:
                word_dict[word] = 1
        else:
            print("no this word")
    return word_dict

def get_vector_separate(home_dir, file_directory1,file_directory2, tag1,tag2,vocab_list):
    os.chdir(file_directory1)
    all_test_file1 = os.listdir(".")
    train_file_list = []
    file_dict= dict()
    for file in all_test_file1:
        if file.endswith('.txt'):
            inputfile = open(file, 'r', encoding="utf-8").readline()
            file_content = inputfile.lower()
            line_without_pun = re.sub(r'[^\w\s]', '', file_content).split()
            word_dict = dict()
            for word in line_without_pun:
                if word in vocab_list:
                    if word in word_dict:
                        word_dict[word] += 1
                    else:
                        word_dict[word] = 1
                else:
                    print("no this word")
            train_file_list.append(word_dict)
    file_dict[tag1] = train_file_list
    os.chdir(home_dir)
    os.chdir(file_directory2)
    all_test_file2 = os.listdir(".")
    train_file_list = []
    for file in all_test_file2:
        if file.endswith('.txt'):
            inputfile = open(file, 'r', encoding="utf-8").readline()
            file_content = inputfile.lower()
            line_without_pun = re.sub(r'[^\w\s]', '', file_content).split()
            word_dict = dict()
            for word in line_without_pun:
                if word in vocab_list:
                    if word in word_dict:
                        word_dict[word] += 1
                    else:
                        word_dict[word] = 1
                else:
                    print("no this word")
            train_file_list.append(word_dict)
    file_dict[tag2] = train_file_list
    os.chdir(home_dir)
    return file_dict

dict_per_file =get_vector_separate(home_dir,"example/train/action","example/train/comedy","action","comedy",vocab_list)
# comedy_dict_per_file =get_vector_separate(home_dir,"example/train/comedy","comedy",vocab_list)
# print(dict_per_file)
# print(comedy_dict_per_file)
test_dict = get_vector_all(home_dir,"example/test","test")
print("test_dict: ", test_dict)
action_dict = get_vector_all(home_dir,"example/train/action","action")
print("action_dict:",action_dict)
comedy_dict = get_vector_all(home_dir,"example/train/comedy","comedy")
print("comedy_dict: ",comedy_dict)

def output_vec_file(vector_tag1,vector_tag2,tag1,tag2,outputfile):
    outputfile = open(outputfile,"w",encoding="utf-8")
    output_dic =dict()
    output_dic[tag1]= vector_tag1
    output_dic[tag2]= vector_tag2
    outputfile.write(json.dumps(output_dic, indent=6))

def output_vec_one_tag(vector_tag1,tag1,outputfile):
    outputfile = open(outputfile,"w",encoding="utf-8")
    output_dic =dict()
    output_dic[tag1]= vector_tag1
    outputfile.write(json.dumps(output_dic,indent = 6))
    outputfile.close()

def output_vector_of_per_file(vector_tag1,outputfile):
    outputfile = open(outputfile,"w",encoding="utf-8")
    output_dic =dict()
    outputfile.write(json.dumps(vector_tag1, indent = 6))
    outputfile.close()


output_vec_one_tag(test_dict,"test","movie-review-small-test.NB")

output_vec_file(action_dict,comedy_dict,"action","comedy","movie-review-small.NB")
#
output_vector_of_per_file(dict_per_file,"movie-review-small-perfile.NB")