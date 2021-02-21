# HeartRateVariabilityAnalysis
研究で作成した心拍変動解析プログラム

# Demo
移動平均をとった脈波波形
![PalseWave(SMA)](https://user-images.githubusercontent.com/59692525/108624288-680cac00-7487-11eb-8482-0ec9336646ac.png)
瞬時心拍数波形
![HLTV(30)](https://user-images.githubusercontent.com/59692525/108624286-6642e880-7487-11eb-993b-5557ecd4f1bd.png)
FFTによる解析結果
![FFT_Result(30)](https://user-images.githubusercontent.com/59692525/108624282-6216cb00-7487-11eb-901f-050008fbce45.png)

# Feature
解析したい脈波データのファイル名を入力すると，心拍変動解析を行う．  
その過程で，移動平均をとった脈波波形，瞬時心拍数の時間変化波形，FFTによる解析結果  
3つのグラフを表示，画像として保存できる．

# Usage
１．コマンドプロンプトでプログラムを実行  
２．解析したいファイルの名前を入力  
３．ピーク点検出後にスキップする点数およびパターンを入力  
４．解析結果が表示される

# Note
私個人が使用する前提で実装したため，ファイルパスが決め打ちになっている．  
グラフの表示と保存をする際にはプログラムを書き換える必要がある．