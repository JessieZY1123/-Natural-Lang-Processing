import os,sys
import re
import string
import operator
import json
# This file to calculate the result of small corpus

home_dir = os.getcwd()
print("Home directory is "+ home_dir)
# file_directory="example/train/action"
total_file =0
outputfile = open("outputFile-small.txt", "w", encoding="utf-8")
def get_number_of_file(file_directory,tag):
    os.chdir(file_directory)
    number_file =[]
    file_list = list(f for f in os.listdir('.') if re.match(r'[0-9]+.*\.txt', f))
    number_of_file = len(file_list)
    number_file.append(tag)
    number_file.append(number_of_file)
    return number_file

action_file = get_number_of_file("example/train/action","action")
# print(action_file)
os.chdir(home_dir)
comedy_file = get_number_of_file("example/train/comedy","comedy")

total_files = action_file[1] + comedy_file[1]
# print(total_files)

p_prior_action = action_file[1] / total_files
p_prior_comedy = comedy_file[1] / total_files

os.chdir(home_dir)
vocab = open("example/example.vocab",'r',encoding="utf-8")
vocab_list = list(vocab.read().split())


def get_NB_classifier_test(prior,  test_list, para_train_file, vocab_list, tag1):

    inputfile_train = open(para_train_file, 'r', encoding="utf-8")
    train_dict = json.loads(inputfile_train.read())
    # print(train_dict)
    tag_dict = train_dict[tag1]
    count_tag = sum(tag_dict.values())
    prob_dict = {}
    # test_list = list(test_dict.keys())

    for word in test_list:
        if word in tag_dict:
            prob = (tag_dict[word] + 1) / (count_tag + len(vocab_list))
        else:
            prob = 1 / (count_tag + len(vocab_list))
        prob_dict[word] = prob
        # print("p("+ word + "|" + tag1 +")= "+ str(prob))
        outputfile.write("p("+ word + "|" + tag1 +")= "+ str(prob)+'\n')

    # print(prob_dict)
    result = 1
    for i in prob_dict:
        result *= prob_dict[i]* test_list[word]
    result = result * prior
    return result

def predict_tag(action,comedy):
    if action > comedy:
        outputfile.write("This test file predicts action class."+'\n')
        print("This test file predicts action class." )
        # result = "action"
    else:
        outputfile.write("This test file predicts comedy class."+'\n')
        print("This test file predicts comedy class." )
        # result = "comedy"
    # return result


inputfile_test = open("movie-review-small-test.NB", 'r', encoding="utf-8")
test_dict = json.loads(inputfile_test.read())
test_dict = test_dict['test']

result_action = get_NB_classifier_test(p_prior_action,test_dict,"movie-review-small.NB",vocab_list,"action")
print("test of action class is " + str(result_action))
outputfile.write("test of action class is " + str(result_action)+'\n')
result_comedy = get_NB_classifier_test(p_prior_comedy,test_dict,"movie-review-small.NB",vocab_list,"comedy")
print("test of comedy class is " + str(result_comedy))
outputfile.write("test of comedy class is " + str(result_comedy)+'\n')
predict_tag(result_action,result_comedy)
