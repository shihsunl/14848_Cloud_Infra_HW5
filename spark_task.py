'''
import sys
from pyspark import SparkContext, SparkConf
conf = SparkConf()
# create Spark context with necessary configuration
sc = SparkContext.getOrCreate(conf=conf)
# Conduct MapReduce and write the output to folder
wordCounts = sc.textFile("/testData").flatMap(lambda line: line.split(" "))\
 .map(lambda word: (word, 1)).reduceByKey(lambda a,b:a +b).saveAsTextFile("/output")
'''
from nltk.tokenize import word_tokenize
import nltk
from nltk.corpus import stopwords
from pyspark import SparkContext
import json

nltk.download('stopwords')
sc = SparkContext("local", "app")
stop_words = set(stopwords.words('english'))

customized_stopwords = ['they','she','he','it','the','as','is','and']
punctuation_signs = list("?:!.,;")

def process(content):
    output = []
    filename = content[0]
    word_set = content[1].lower().split()

    for word in word_set:
        if word in stopwords.words():
            continue
        else:
            output.append((word, filename))

    return output

def merge(content):
    word = content[0]
    filename_set = content[1]
    filename_cnt_obj = {}
    for filename in filename_set:
        if filename not in filename_cnt_obj:
            filename_cnt_obj[filename] = 1
        else:
            filename_cnt_obj[filename]+=1

    output_arr = []
    for filename in filename_cnt_obj:
        output_arr.append((filename, filename_cnt_obj[filename]))

    return (word, output_arr)

path = '/temp/Data/txt_files/'
rdd = sc.wholeTextFiles(path)

output = rdd.flatMap(lambda content: ((word, [content[0]]) for word in content[1].lower()\
         .replace(';',' ').replace(',',' ').replace('\n',' ').replace('\r',' ')\
         .replace('"','').replace('  ',' ').replace("'s","").replace('!','')\
         .replace('?','').replace('.','').replace(':','').split()))\
         .filter(lambda mapping: mapping[0] not in customized_stopwords)\
         .reduceByKey(lambda a,b: a+b).map(lambda mapping: merge(mapping))

output_data = output.collect()
print(output_data)
output_str = json.dumps(output_data)

# output file
f = open("output.txt", "w")
f.write(output_str)
f.close()


