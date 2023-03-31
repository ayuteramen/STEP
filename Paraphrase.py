# -*- coding: utf-8 -*-
"""0520281B-exp5-4-jaja-寺面杏優.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MoGmFxbA2B0sVH3RtDGSnCQ8pqR_LfK_

# 事前にやること
1. ランタイムのタイプを "GPU" に変更
2. 設定ファイル "rnn.yaml" および "san.yaml" をアップロード
"""

from google.colab import drive
drive.mount('/content/drive')

# ライブラリのインストール

! pip install janome
! pip install sockeye==3.1.27

# 前処理（日本語の単語分割）

from janome.tokenizer import Tokenizer
tokenizer = Tokenizer()

# train
fout = open("ja.simp.train-0.txt", "w")
fin = open("/content/drive/MyDrive/translation/ja.simp.train.txt", "r")
for line in fin:
    fout.write(" ".join([token.surface for token in tokenizer.tokenize(line.strip())]) + "\n")
fin.close()
fout.close()

fout = open("ja.comp.train-0.txt", "w")
fin = open("/content/drive/MyDrive/translation/ja.comp.train.txt", "r")
for line in fin:
    fout.write(" ".join([token.surface for token in tokenizer.tokenize(line.strip())]) + "\n")
fin.close()
fout.close()

# valid
fout = open("ja.simp.valid.txt", "w")
fin = open("/content/drive/MyDrive/translation/ja.simp.valid.txt", "r")
for line in fin:
    fout.write(" ".join([token.surface for token in tokenizer.tokenize(line.strip())]) + "\n")
fin.close()
fout.close()

fout = open("ja.comp.valid.txt", "w")
fin = open("/content/drive/MyDrive/translation/ja.comp.valid.txt", "r")
for line in fin:
    fout.write(" ".join([token.surface for token in tokenizer.tokenize(line.strip())]) + "\n")
fin.close()
fout.close()

# test
fout = open("ja.simp.test.txt", "w")
fin = open("/content/drive/MyDrive/translation/ja.simp.test.txt", "r")
for line in fin:
    fout.write(" ".join([token.surface for token in tokenizer.tokenize(line.strip())]) + "\n")
fin.close()
fout.close()

fout = open("ja.comp.test.txt", "w")
fin = open("/content/drive/MyDrive/translation/ja.comp.test.txt", "r")
for line in fin:
    fout.write(" ".join([token.surface for token in tokenizer.tokenize(line.strip())]) + "\n")
fin.close()
fout.close()

# ja.comp.eval.txt
fout = open("ja.comp.eval.txt", "w")
fin = open("/content/drive/MyDrive/translation/ja.comp.eval.txt", "r")
for line in fin:
    fout.write(" ".join([token.surface for token in tokenizer.tokenize(line.strip())]) + "\n")
fin.close()
fout.close()

# データ精選
# train


with open("ja.simp.train.txt", "w") as fout1, open("ja.comp.train.txt", "w") as fout2, open("ja.simp.train-0.txt", "r") as fin1, open("ja.comp.train-0.txt", "r") as fin2:
    for i in range(50000):
          Fin1 = fin1.readline()
          Fin2 = fin2.readline()
          if abs(len(Fin1) - len(Fin2)) >= 0:
              fout1.write(Fin1)
              fout2.write(Fin2)

# 準備

! python -m sockeye.prepare_data --source "ja.comp.train.txt" --target "ja.simp.train.txt" --output "train-data"

# 訓練

! python -m sockeye.train --prepared-data "train-data" --validation-source "ja.comp.valid.txt" --validation-target "ja.simp.valid.txt" --output "sockeye" \
    --batch-size 64 --batch-type sentence --max-updates 150000 --checkpoint-interval 10000 --weight-tying-type none

# 翻訳
! python -m sockeye.translate --batch-size 128 --models "/content/drive/MyDrive/sockeye" "/content/drive/MyDrive/sockeye" "/content/drive/MyDrive/sockeye" "/content/drive/MyDrive/sockeye" "/content/drive/MyDrive/sockeye" "/content/drive/MyDrive/sockeye" \
--checkpoint 15 14 1 13 12 7 --input "ja.comp.eval.txt" --output "/content/drive/MyDrive/sockeye.en-ja.txt"

"""15 14 1 13 12 7 : 60.00  
15 9 1 13 12 7 : 59.84  
14 13 12 9 7 1 : 59.95  
9 1 13 12 7 : 59.97  
14 13 12 9 7 : 59.89  
14 13 12 7 : 59.73  
13 12 9 7 : 59.91  
1 13 12 7 : 59.91  
13 12 7 : 59.35  
12 7 : 59.28  
15 14 : 58.87  
10 9 : 59.09

58.57 150000  
58.60 140000  
58.63 130000  
58.73 120000  
58.33 110000  
58.21 100000  
58.57 90000  
58.52 80000  
58.65 70000  
58.53 60000  
58.38 50000  
58.42 40000  
58.24 30000  
58.20 20000  
58.57 10000
"""