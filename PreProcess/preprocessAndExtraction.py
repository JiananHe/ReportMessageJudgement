#!python2
# coding: utf-8
import xlrd
import re
import nltk.stem
import math
import numpy as np
import os
from sklearn.feature_extraction.text import HashingVectorizer


def process_text(line):
    split_symbol = r"[ ;,:.\s\"]"
    line = line.lower()
    tokens = re.split(split_symbol, line)
    cleanTokens = []
    # 提取词干 词根还原
    stemmer = nltk.stem.SnowballStemmer('english')
    lemmatizer = nltk.stem.WordNetLemmatizer()
    for token in tokens:
        if token.isalpha():
            token = stemmer.stem(lemmatizer.lemmatize(token))
        else:
            match = re.findall(r'[^a-z0-9]+', token)
            for i in match:
                # 只要英文单词与数字，删掉其他字符
                token = token.replace(i, '')
            if token.isalpha():
                token = stemmer.stem(lemmatizer.lemmatize(token))
        if len(token) > 1:
            cleanTokens.append(token)

    newline = ' '.join(cleanTokens)
    return newline


def similarity(vec1, vec2):
    multi = 0
    sum1 = 0
    sum2 = 0
    for i in range(len(vec1)):
        multi += vec1[i] * vec2[i]
        sum1 += math.pow(vec1[i], 2)
        sum2 += math.pow(vec2[i], 2)

    return multi / math.sqrt(sum1 * sum2)



# 读取表格
print "read from raw data..."
raw_data = xlrd.open_workbook('High Qulity Text.xlsx')
table = raw_data.sheet_by_index(0)
print "read completed!"
# 一共11946行，每行6列

# 第一列：1；第二列：应该是标记码；第三列：应该是系统显示的错误描述；
# 第四列：自然语言描述的错误；第五列：如何得到这个错误；第六列：空
# firstline = table.row_values(1)
# for i in range(len(firstline)):
#     print firstline[i]

# 统计第四列的单词频数


text_set = []
c = 0
print "\nprocess raw data..."
# table.nrows
for i in range(table.nrows):
    line = table.row_values(i)
    if len(line) != 6 or type(line[2]) != unicode or type(line[3]) != unicode or type(line[4]) != unicode:
        continue
    line = line[2] + " " + line[3] + " " + line[4]

    newline = process_text(line)
    if len(newline.split(" ")) < 3:
        continue
    # print newline
    text_set.append(newline)
    c = c + 1
print str(c)+" lines of data are processed"

# print text_set[0]
# print len(text_set)

# text_set.append("I have a bug")

print "\ntext feature extracting..."
vector = HashingVectorizer(n_features=100)
res = vector.transform(text_set).todense()
print "text features extraction completed!..."

savePath = os.path.abspath(os.path.join(os.getcwd(), ".."))
savePath = os.path.join(savePath, "JudgementWeb", "feature_vectors.txt")
if os.path.exists(savePath):
    os.remove(savePath)
np.savetxt(savePath, res)
print "the feature vectors writed into %s" % savePath

# for x, y in [[0, 1], [0, 2], [1, 2]]:
#     print similarity((res[x].tolist())[0], (res[y].tolist())[0])
