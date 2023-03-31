# -*- coding: utf-8 -*-
"""0520281B-exp4-3-寺面杏優（課題3）.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1DN5NKPWWnioYyhRV982v2dAVyyo8uwaT
"""

# ライブラリの導入
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.svm import SVC
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from mlxtend.plotting import plot_decision_regions

fin1=open('/content/label.dev.txt')
label_dev=fin1.read()
#print(label_dev)
fin1.close()
fin2=open('/content/label.test.txt')
label_test=fin2.read()
#print(label_test)
fin2.close()
fin3=open('/content/label.train.txt')
label_train=fin3.read()
#print(label_train)
fin3.close()
fin4=open('/content/text.dev.txt')
t_dev=fin4.read()
#print(t_dev)
fin4.close()
fin5=open('/content/text.eval.txt')
t_eval=fin5.read()
#print(t_eval)
fin5.close()
fin6=open('/content/text.test.txt')
t_test=fin6.read()
#print(t_test)
fin6.close()
fin7=open('/content/text.train.txt')
t_train=fin7.read()
#print(t_train)
fin7.close()

pip install janome

# from janome.tokenizer import Tokenizer
# import collections
# t = Tokenizer()
# c_t_train = collections.Counter(t.tokenize(t_train, wakati=True))
# print(c_t_train.most_common())

from janome.tokenizer import Tokenizer
import collections
t = Tokenizer()
c_train = collections.Counter(t.tokenize(t_train, wakati=True))
d_train = dict(c_train)

# 出現回数が3回以上のものを列挙（重複なし）
word_list = []
for key, value in d_train.items():
    if value >= 3:
        #print(key, value)
        word_list.append(key) 
print(word_list)

l_train = t_train.split("\n")
l_dev = t_dev.split("\n")
l_test = t_test.split("\n")
l_eval = t_eval.split("\n")

feature_vector_list_train=[]
for sentence in l_train:
    #print(sentence)
    feature_vector=[]
    for word in word_list:
        #print(word)
        if word in sentence:
            feature_vector.append(1)
        else:
            feature_vector.append(0)
    feature_vector_list_train.append(feature_vector)

#print(feature_vector_list_train)

feature_vector_list_dev=[]
for sentence in l_dev:
    #print(sentence)
    feature_vector=[]
    for word in word_list:
        #print(word)
        if word in sentence:
            feature_vector.append(1)
        else:
            feature_vector.append(0)
    feature_vector_list_dev.append(feature_vector)

feature_vector_list_test=[]
for sentence in l_test:
    #print(sentence)
    feature_vector=[]
    for word in word_list:
        #print(word)
        if word in sentence:
            feature_vector.append(1)
        else:
            feature_vector.append(0)
    feature_vector_list_test.append(feature_vector)

feature_vector_list_eval=[]
for sentence in l_eval:
    #print(sentence)
    feature_vector=[]
    for word in word_list:
        #print(word)
        if word in sentence:
            feature_vector.append(1)
        else:
            feature_vector.append(0)
    feature_vector_list_eval.append(feature_vector)

print(str(np.shape(feature_vector_list_train)), str(np.shape(feature_vector_list_dev)), str(np.shape(feature_vector_list_test)), str(np.shape(feature_vector_list_eval)))

print(feature_vector_list_test[0])

label_list_train = label_train.split("\n")
label_list_dev = label_dev.split("\n")
label_list_test = label_test.split("\n")





#ロジスティック回帰
model = LogisticRegression(random_state=0,max_iter=10001)
model.fit(feature_vector_list_train, label_list_train)
y_pred = model.predict(feature_vector_list_dev)
print("正解率 = %.3f" % accuracy_score(y_pred, label_list_dev))



#線形SVM
best_acc = 0
best_c1 = 1
for c1 in [0.01, 0.1, 1, 10, 100]:
    model = LinearSVC(C=c1, random_state=0)
    model.fit(feature_vector_list_train, label_list_train)
    y_pred = model.predict(feature_vector_list_dev)
    acc = accuracy_score(y_pred, label_list_dev)
    if acc > best_acc:
        best_acc = acc
        best_c1 = c1
    print("正解率 = %.3f  C = %s" % (acc, str(c1)))
print("最適なハイパーパラメタは C = %s" % str(best_c1))

# 最適なハイパーパラメタで学習したモデルを評価
model = LinearSVC(C=best_c1, random_state=0)
model.fit(feature_vector_list_train, label_list_train)
y_pred = model.predict(feature_vector_list_test)
acc = accuracy_score(y_pred, label_list_test)
print("正解率 = %.3f" % acc)



#カーネルSVM（RBFカーネル）
best_acc = 0
best_c2 = 1
for c2 in [0.01, 0.1, 1, 10, 100]:
    model = SVC(C=c2, random_state=0)
    model.fit(feature_vector_list_train, label_list_train)
    y_pred = model.predict(feature_vector_list_dev)
    acc = accuracy_score(y_pred, label_list_dev)
    if acc > best_acc:
        best_acc = acc
        best_c2 = c2
    print("正解率 = %.3f  C = %s" % (acc, str(c2)))
print("最適なハイパーパラメタは C = %s" % str(best_c2))

# 最適なハイパーパラメタで学習したモデルを評価
model = LinearSVC(C=best_c2, random_state=0)
model.fit(feature_vector_list_train, label_list_train)
y_pred = model.predict(feature_vector_list_test)
acc = accuracy_score(y_pred, label_list_test)
print("正解率 = %.3f" % acc)



#線形SVM
model = LinearSVC(C=best_c1, random_state=0)
model.fit(feature_vector_list_train, label_list_train)
answers1 = model.predict(feature_vector_list_eval)

f = open('Answer1.txt', 'w')
for answer1 in answers1:
    f.write(answer1 + "\n")
f.close()

#カーネルSVM（RBFカーネル）
model = SVC(C=best_c2, random_state=0)
model.fit(feature_vector_list_train, label_list_train)
answers2 = model.predict(feature_vector_list_eval)

f = open('Answer2.txt', 'w')
for answer2 in answers2:
    f.write(answer2 + "\n")
f.close()



#print(answers)

# f=open('/content/Answer.txt')
# Answer=f.read()
# #print(Answer)
# f.close()

#print(sum([1 for _ in open('Answer.txt')]))

