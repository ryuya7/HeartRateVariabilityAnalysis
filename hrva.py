import os
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

print("脈波データのファイルの階層をそろえること")
print("ファイル名を入力してください(拡張子不要)\n")
FilePath1 = "e:\デスクトップ\\1EM\特別研究\予備実験データ\\"
FilePath2 = input()
FilePath3 = ".csv"
FilePath = FilePath1 + FilePath2 + FilePath3

nirr = pd.read_csv(FilePath)
num = nirr.size

PW_b = []

#csvファイルから脈波の配列を生成
for i in range(num):
    PW_b += [nirr.iat[i, 0]]

PW_b_max = max(PW_b)

#脈波を反転，値が正になるようにバイアス
for i in range(num):
    PW_b[i] = PW_b[i] * -1 + PW_b_max


#脈波の移動平均をとる，20点ぶん(0.333s)
PW = []
flg = False
for i in range(num):
    stack = 0
    for j in range(20):
        if i+j >= num:
            flg = True
            break
        stack += PW_b[i+j]
    if flg:
        break
    PW += [stack/20]

#脈波の各点の時間を算出
PW_Time = []
cou = 0
while cou <= len(PW)-1:
    PW_Time += [cou*(1/60)]
    cou += 1

#読み飛ばす点数を複数選択できる処理
print("\n何通りのスキップを行うか入力してください")
pat = int(input())
skip_list = []
for i in range(pat):
    print("\n%dパターン目" % (i+1))
    skip_list += [int(input())]
print()

#ピーク点を検出する関数
def Peak_Det(skip):
    cou = 0
    P_P_sublist = []
    global PW
    while cou < len(PW)-2:
        if PW[cou] <= PW[cou+1] and PW[cou+1] > PW[cou+2]:
            P_P_sublist += [cou]
            cou += skip
        cou += 1
    Peak_Point_list.append(P_P_sublist)

#読み飛ばしに応じたピーク点の2次元配列を作成
Peak_Point_list = []
for i in range(pat):
    Peak_Det(skip_list[i])

#ピーク点の時間を算出して瞬時心拍数を計算する関数
def Calc_PTandHR(list_index):
    cou = 0
    P_T_sublist = []
    ihr_sublist = []
    while cou < len(Peak_Point_list[list_index])-1:
        P_T_sublist += [Peak_Point_list[list_index][cou]*(1/60)]
        ihr_sublist += [3600/(Peak_Point_list[list_index][cou+1]-Peak_Point_list[list_index][cou])]
        cou += 1
    Peak_Time_list.append(P_T_sublist)
    ihr_list.append(ihr_sublist)

#それぞれのピーク点配列で，ピーク点の時間を算出し瞬時心拍数を計算
Peak_Time_list = []
ihr_list = []
for i in range(pat):
    Calc_PTandHR(i)

dirpath = ""

#画像を保存するか聞く関数
def WantSave(str):
    global dirpath
    print("保存しますか？→ %s" % str)
    YorN = input("y/n:")
    print()
    if YorN == "y":
        dirpath = "e:\デスクトップ\\1em\特別研究\画像\\%s" % FilePath2
        os.makedirs(dirpath, exist_ok=True)
        SaveFigure(str)

#画像を保存するときに呼ぶ関数
def SaveFigure(str):
    plt.savefig(os.path.join(dirpath, str))

#移動平均処理後の脈波波形と瞬時心拍数の時間変化波形を表示する関数
def Plt_PWandHR(patt):
    plt.figure(dpi=100, figsize=(16, 9))
    plt.rcParams["font.size"] = 30
    plt.title("PalseWave(SMA)")
    plt.xlabel("Time[s]")
    plt.ylabel("Freq")
    plt.plot(PW_Time, PW)
    SaveFigureName = "PalseWave(SMA).png"
    WantSave(SaveFigureName)
    for i in range(patt):
        plt.figure(dpi=100, figsize=(16, 9))
        plt.title("HeartLate-TimeVariation(Skip:%d)" % skip_list[i])
        plt.xlabel("Time[s]")
        plt.ylabel("HeartLate[bpm]")
        plt.plot(Peak_Time_list[i], ihr_list[i])
        SaveFigureName = "HLTV(%d).png" % skip_list[i]
        WantSave(SaveFigureName)

#それぞれ，最初のピーク点の出現時間が0になるよう調整
bias = min(Peak_Time_list[0])
for i in range(pat):
    for j in range(len(Peak_Time_list[i])):
        Peak_Time_list[i][j] -= bias

#それぞれの心拍数の相対値を計算
Rel_ihr_list = []
ave_ihr_list = []
for i in range(pat):
    Rel_ihr_sublist = []
    ave_ihr_list += [sum(ihr_list[i])/len(ihr_list[i])]
    for j in range(len(ihr_list[i])):
        Rel_ihr_sublist += [(ihr_list[i][j]-ave_ihr_list[i])/ave_ihr_list[i]]
    Rel_ihr_list.append(Rel_ihr_sublist)

#瞬時心拍数の時間変化波形をinterpolateで補完
#0.25s間隔の配列を用意し，FFTを実行
PT_interp_list = []
FFT_list = []
FFT_abs_list = []
for i in range(pat):
    PT_interp_sublist = []
    Graph = interp1d(Peak_Time_list[i], Rel_ihr_list[i], kind="cubic")
    for j in range(int(max(Peak_Time_list[i])*4)):
        PT_interp_sublist.append(j*0.25)
    PT_interp_list.append(PT_interp_sublist)
    FFT = np.fft.fft(Graph(PT_interp_list[i]))
    FFT_abs = np.abs(FFT)
    FFT_list.append(FFT)
    FFT_abs_list.append(FFT_abs)

#グラフの横軸用のリストを作成
Freq_list = []
for i in range(pat):
    Freq_sublist = []
    for j in range(len(FFT_abs_list[i])):
        Freq_sublist += [1/300*j]
    Freq_list.append(Freq_sublist)

#FFTで得られたパワースペクトルを表示する関数
def Plt_PS(patt):
    for i in range(patt):
        plt.figure(dpi=100, figsize=(16, 9))
        plt.title("FFT(skip:%d)" % skip_list[i])
        plt.tick_params(labelleft=False)
        plt.tick_params(left=False)
        plt.xlim([0,1])
        plt.xlabel("Frequency[Hz]")
        plt.bar(Freq_list[i], FFT_abs_list[i], width=1/300)
        SaveFigureName = "FFT_Result(%d).png" % skip_list[i]
        WantSave(SaveFigureName)

#それぞれのLFとHFを計算
#0.00333...Hz区切りでデータが出ているので，
#LF:Freq_list[][12~45] HF:Freq_list[][46~120] となる
LF_list = []
HF_list = []
LFHF_list = []
for i in range(pat):
    LF = 0
    HF = 0
    for j in range(12, 45):
        LF += FFT_abs_list[i][j]
    for j in range(46, 120):
        HF += FFT_abs_list[i][j]
    LF_list.append(LF)
    HF_list.append(HF)
    LFHF_list.append(LF/HF)

Plt_PWandHR(pat)
Plt_PS(pat)
plt.show()