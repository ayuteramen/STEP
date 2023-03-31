# -*- coding: utf-8 -*-
"""0520281B-exp4-3-寺面杏優（課題6）.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1sxRel1OhJJm-EPnpnt0lueJYGjyqG6Bv
"""

# ライブラリの導入
import numpy as np
import pandas as pd

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

fin8=open('/content/label.EVAL.txt')
label_EVAL=fin8.read()
#print(label_EVAL)
fin8.close()

pip install janome

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

#リスト化する
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

label_list_train = label_train.split("\n")
label_list_dev = label_dev.split("\n")
label_list_test = label_test.split("\n")
label_list_EVAL = label_EVAL.split("\n")

print(label_list_train)
print(type(label_list_train))

label_list2_train = [int(s)+2 for s in label_list_train]
label_list2_dev = [int(s)+2 for s in label_list_dev]
label_list2_test = [int(s)+2 for s in label_list_test]
label_list2_EVAL = [int(s)+2 for s in label_list_EVAL]
print(label_list2_train)
print("変換後：", type(label_list2_train))

# ====================
# データ形式の変換 (list --> ndarray --> Tensor)
# ====================

import torch

print("変換前：", type(feature_vector_list_train), type(label_list2_train))
tensor_train = torch.tensor(feature_vector_list_train, dtype=torch.float32)
tensor_dev = torch.tensor(feature_vector_list_dev, dtype=torch.float32)
tensor_test = torch.tensor(feature_vector_list_test, dtype=torch.float32)
tensor_eval = torch.tensor(feature_vector_list_eval, dtype=torch.float32)

label_array_train = np.array(label_list2_train)
label_array_dev = np.array(label_list2_dev)
label_array_test = np.array(label_list2_test)
label_array_EVAL = np.array(label_list2_EVAL)
print("変換中：", type(label_array_train))

label_tensor_train = torch.tensor(label_array_train, dtype=torch.int64)
label_tensor_dev = torch.tensor(label_array_dev, dtype=torch.int64)
label_tensor_test = torch.tensor(label_array_test, dtype=torch.int64)
label_tensor_EVAL = torch.tensor(label_array_EVAL, dtype=torch.int64)

print("変換後：", type(tensor_train), type(label_tensor_train))

# ====================
# DataLoaderに格納
# ====================

from torch.utils.data import TensorDataset
from torch.utils.data import DataLoader

train = TensorDataset(tensor_train, label_tensor_train)
dev = TensorDataset(tensor_dev, label_tensor_dev)
test = TensorDataset(tensor_test, label_tensor_test)
EVAL = TensorDataset(tensor_eval, label_tensor_EVAL)

batch_size = 10

train_loader = DataLoader(train, batch_size, shuffle=True)
dev_loader = DataLoader(dev, batch_size, shuffle=False)
test_loader = DataLoader(test, batch_size, shuffle=False)
EVAL_loader = DataLoader(EVAL, batch_size, shuffle=False)

len = 0
for i in word_list:
    len += 1
print(len)

train_loader

# ====================
# ネットワークを定義
# ====================

import torch.nn as nn
import torch.nn.functional as F

class Net(nn.Module):

    # モデルの構造
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(len, 10)  # 5次元の入力層から4次元の中間層への全結合
        self.fc2 = nn.Linear(10, 5)  # 4次元の中間層から3次元の出力層への全結合
    
    # 順伝播
    def forward(self, x):
        h = F.relu(self.fc1(x))  # xを線形変換（fc1）し、非線形変換（relu）し、中間表現hを得る
        y = self.fc2(h)  # 中間表現hを線形変換（fc2）し、出力yを得る
        return y

# ネットワークのインスタンスを作成
net = Net()
net



criterion = nn.CrossEntropyLoss()

optimizer = torch.optim.SGD(net.parameters(), lr=0.1)

# ====================
# モデルをGPUへ転送
# ====================

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

net = net.to(device)

device

import torch

# ====================
# 学習ループ
# ====================

max_epoch = 10

for epoch in range(max_epoch):

    # ミニバッチ学習
    for batch in train_loader:

        # バッチサイズ分のサンプルを抽出
        x, t = batch 

        # データをGPUへ転送
        x = x.to(device)
        t = t.to(device)

        # 勾配を初期化
        optimizer.zero_grad()

        # 順伝播
        y = net(x)
        loss = criterion(y, t)  

        # 誤差逆伝播
        loss.backward() 
        optimizer.step()
    
    # 更新と切り離し、検証データの性能を確認
    with torch.no_grad():
        losses = list()
        for batch in dev_loader:
            x, t = batch
            x = x.to(device)
            t = t.to(device)
            y = net(x) 
            loss = criterion(y, t)
            losses.append(loss)
    val_loss = torch.tensor(losses).mean()
    print("Epoch: %02d  val_loss: %.3f" % (epoch+1, val_loss))
    #print(type(y),type(t))
    #print((y),len(t))

# ====================
# 推定したラベルを獲得
# ====================

with torch.no_grad():
    preds = list()
    for batch in test_loader:
        x, t = batch  
        x = x.to(device)
        t = t.to(device)
        y = net(x) 
        preds.append(y.argmax(axis=1))  # 事例ごとに最高の予測値を持つラベルを選ぶ
    preds = torch.concat(preds)

preds

from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score

golds = torch.concat([t for x, t in test_loader])
#print(classification_report(golds, preds, digits=3))
print(accuracy_score(golds, preds))

with torch.no_grad():
    preds1 = list()
    for batch in EVAL_loader:
        x, t = batch  
        x = x.to(device)
        t = t.to(device)
        y = net(x) 
        preds1.append(y.argmax(axis=1))  # 事例ごとに最高の予測値を持つラベルを選ぶ
    preds1 = torch.concat(preds1)-2

preds1

f = open('Answer_6.txt', 'w')
for answer in preds1:
    f.write(str(answer.item())+ "\n")
f.close()

f=open('/content/Answer_6.txt')
Answer=f.read()
#print(Answer)
f.close()

print(sum([1 for _ in open('Answer_6.txt')]))