# coding: UTF-8

import sys
import re
import os
from time import sleep
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import matplotlib.pyplot as plt
from matplotlib import rcParams

ver = "Ver. 1.4.3"



# matplotlibのフォント設定
rcParams['font.family'] = 'sans-serif' # フォント設定
rcParams['font.sans-serif'] = ['Hiragino Maru Gothic Pro', 'Yu Gothic', 'Meirio', 'Takao', 'IPAexGothic', 'IPAPGothic', 'VL PGothic', 'Noto Sans CJK JP']


# リソースファイルを参照する関数（参考：https://qiita.com/firedfly/items/f6de5cfb446da4b53eeb）
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


# 文字列がfloatに変換できるかどうかを判断する関数（入力されたTargetが適切かをチェックするため）
def is_float(s):
  try:
    float(s)
  except:
    return False
  return True



### ログ編集に使う関数 ###
# キーワードをファイル名に含むファイルの一覧を取得
def searchFile(keyword):
        dir = os.getcwd()
        files = []
        getfiles=[]
        
        # 同じディレクトリにある全ファイルの名前を取得
        for name in os.listdir(dir):
                if os.path.isfile(os.path.join(dir, name)):
                        files.append(name)

        # そのうち、キーワードを含むものだけをリストアップ
        regex = re.compile(r"(" + keyword + r")")
        for name in files:
                if regex.search(name):
                        getfiles.append(name)
        return getfiles

# ファイルの読み込み
def readFile(fileName):
        f = open(fileName, 'r', encoding='utf-8')
        file = f.readlines()
        f.close()
        return file

# 0.1秒後のファイルサイズが同じかどうかをチェック
def checkSize(size, logfile):
        size[0] = os.path.getsize(logfile)
        sleep(0.1)
        size[1] = os.path.getsize(logfile)
        if size[0] == size[1]:
                return True
        else:
                return False

# 指定した文字列を消す
def deleteStr(strings, *delList):
        for i in delList:
                strings = strings.replace(i, "")
        return strings

# 文字列中のアルファベットを消す
def deleteAlphabet(strings):
        strings = re.sub(r"[a-z]", "", strings)
        strings = re.sub(r"[A-Z]", "", strings)
        return strings

# keywordが含まれる行数を返す
def searchIndex(list, keyword):
        index=[]
        for i in range(len(list)):
                if keyword in list[i]:
                        index.append(i)
        return index

# スペースの数を調整の関数
def adjustSpace(str):
        if len(str) < 5:
                str = " "*(5-len(str)) + str
        return str



### GUI作成 ###
class FiledialogSampleApp(ttk.Frame):
        def __init__(self, app):
                super().__init__(app)
                self.pack()

                # Widget用変数を定義
                self.filename = tk.StringVar() # 入力したパスを入れる変数
                self.bln = tk.BooleanVar() # Targetを出力するかどうか
                self.bln.set(True) # 初期設定：Targetを出力する
                self.target = tk.StringVar() # Relative LoudnessのTargetを入れる変数
                self.target.set("-14") # Targetを-14 LUFSに設定
                self.setDir = os.getcwd() # カレントディレクトリ取得

                self.filenameEntry = ttk.Entry(self,text="", font=("","10"), width=100, textvariable= self.filename) # パス入力
                self.targetCheck = tk.Checkbutton(self,text="Set a target of relative loudness.", font=("","12"), variable=self.bln, command=self.setBln) # Relative Loudnessを使うかチェック
                self.targetEntry = ttk.Entry(self,text="", font=("","10"), width=100, justify="center", textvariable= self.target, state="active") # Target入力
                self.analyzeButton = ttk.Button(self,text="Analyze",command = self.startAnalyze) # アナライズボタン
                self.textbox = tk.Text(self) # Resultのテキストボックス

                label_title = ttk.Label(self, text="Loudness Checker", font=("","20","bold")) # タイトル
                label_title.pack(side="top", pady=5)

                label_ex = ttk.Label(self, justify="center",text="- {} -\nAlgorithm: EBU R128\n".format(ver), font=("","12")) # 説明文1
                label_ex.pack(side="top")
                
                label_path = ttk.Label(self,justify="center",text="【Audio / Video file path】", font=("","14","bold")) # Auidio / Video file path
                label_path.pack(side="top")

                label_Codecs = ttk.Label(self,justify="center",text="Codecs: wav, mp3, ogg, flac, mp4, avi, flv, etc.", font=("","12")) # 対応コーデック説明
                label_Codecs.pack(side="top")

                self.filenameEntry.pack(side="top", padx=5) # パス入力ウィジェット配置

                openButton = ttk.Button(self,text="Browse…",command = self.openFileDialog) # 参照ボタン
                openButton.pack(side="top")
                
                label_target = ttk.Label(self,justify="center",text="\n【Target (LUFS)】", font=("","14","bold")) # Target
                label_target.pack(side="top")

                self.targetCheck.pack(side="top")

                self.targetEntry.pack(side="top", padx=5) # Target入力ウィジェット配置

                self.analyzeButton.pack(side="top") # 分析ボタンウィジェット配置

                label_res = ttk.Label(self,text="\n【Result】", font=("","14","bold")) # Result
                label_res.pack(side="top")
                self.textbox.pack(side="top", padx=5, pady=5) # Resultウィジェット配置

        # ファイルダイアログを開いてfilenameEntryに反映させる
        def openFileDialog(self):
                file = filedialog.askopenfilename(initialdir = self.setDir)
                if file == "":
                        return "break"
                self.setDir = file[0:file.rfind( "/" ) + 1]
                self.filename.set(file)
        
        def setBln(self):
                if self.bln.get() == True:
                        self.targetEntry.config(state="active")
                else:
                        self.targetEntry.config(state="disable")
        
        # アナライズボタンクリック時
        def startAnalyze(self):
                if self.filename.get() == "":
                        messagebox.showerror("ERROR", "Please enter a valid path!")
                        return "break"
                
                if self.bln.get() == True:
                        target = self.targetEntry.get()
                        if is_float(target) == False:
                                messagebox.showerror("ERROR", "Please set a valid target!")
                                return "break"
                        target = float(target)

                self.analyzeButton.config(state="disable", text="Runing…") # ボタン止める
                plt.close() # グラフ開いてたら閉じる
                
                res, time, mLoud, sLoud, iLoud, audioName = self.audioAnalyze()

                if res == "b":
                        return
                
                self.analyzeButton.config(state="active", text="Analyze") # ボタン復活

                self.textbox.delete("1.0", "end")
                for i in range(len(res)):
                        self.textbox.insert(str(i+1)+".0", res[i]+"\n") # 結果出力
                
                # グラフ出力
                g_m = plt.plot(time, mLoud, label="Momentary", color="blue")
                g_s = plt.plot(time, sLoud, label="Short-term", color="yellow")
                g_i = plt.plot(time, iLoud, label="Integrated", color="red")
                
                RL = iLoud[round(len(iLoud)/2)] - 10 # 下方向の表示範囲
                RH = max(mLoud) + 5 # 上方向の表示範囲
                if self.bln.get() == True:
                        targetLine = plt.hlines([target], time[0], time[len(time)-1], "black", linestyles="dashed")
                        if RL > target:
                                RL = target - 2
                                RH = max(mLoud) + 3
                        if RH < target:
                                RL = iLoud[len(iLoud)-1] - 3
                                RH = target + 2
                plt.ylim(RL, RH)
                plt.title("Result - {}".format(audioName), fontsize=18)
                plt.ylabel("Loudness [LUFS]")
                plt.xlabel("Time [s]")
                plt.legend()
                plt.show()
        


        # 音声処理
        def audioAnalyze(self):
                path = self.filenameEntry.get()
                path = deleteStr(path, '"', "'") # pathに " とか ' が含まれていても一旦消す
                path = path.replace("\\", "/") # スラッシュを統一
                audioName = path[path.rfind( "/" ) + 1 : len(path)] # ファイル名取得
                ext = path[path.rfind(".")+1 : len(path)] # 拡張子取得

                # ffmpegが対応しているフォーマットのリストを取得
                ext_list = readFile(resource_path("src/FFmpeg_FileExtention.txt"))
                ext_list[0] = deleteStr(ext_list[0], "'")
                ext_list[0] = ext_list[0].split(", ")

                # 入力されたファイルがffmpegに対応しているかチェック
                if ext not in ext_list[0]:
                        messagebox.showerror("ERROR", "This file or path is invalid!")
                        self.analyzeButton.config(state="active", text="Analyze")
                        return "break!"
                
                # ffmpegコマンド実行
                path = '"{}"'.format(path) # タイトルにスペースがあるとコマンドがバグるんで、その対策

                cmd = ["" for i in range(2)]
                cmd[0] = "start ffmpeg -report -hide_banner -nostats -i {} -filter_complex ebur128=peak=true -f null -".format(path) # ラウドネス関連の情報取得
                cmd[1] = "start ffmpeg -report -hide_banner -nostats -i {} -filter_complex ebur128=peak=sample -f null -".format(path) # 通常ピークの情報取得

                for i in range(len(cmd)):
                        os.system(cmd[i]) # コマンドプロンプトを別で起動してコマンド実行
                        sleep(1.1) # .logファイル上書き対策

                # .logのファイル名を抽出
                logfiles = searchFile(r"^ffmpeg-\d{8}-\d{6}.log$")

                # コマンドが終了するまで待つ
                size=[0,0]
                while True:
                        if checkSize(size, logfiles[0]) == True: # 0.1秒後にファイルサイズが変わっているかをチェック
                                if checkSize(size, logfiles[1]) == True:
                                        log_0 = readFile(logfiles[0]) # ラウドネス関連のログ読み込み
                                        log_1 = readFile(logfiles[1]) # サンプルピーク関連のログ読み込み
                                        TF_0 = "AVIOContext" in log_0[len(log_0)-1] # 分析終わってたらTrue
                                        TF_1 = "AVIOContext" in log_1[len(log_1)-1] # 分析終わってたらTrue
                                        if TF_0 == True and TF_1 == True:
                                                break
                                        else:
                                                messagebox.showerror("ERROR", "Measurement failed!\n\nPlease exit the ffmpeg.exe and restart this application.")
                                                sys.exit() # エラったら強制終了
                        

                ### mLoud, sLoudを取得 ###
                processing = [] # ログの情報を編集するために使う
                for i in log_0:
                        if "TARGET:-23 LUFS" in i: # mLoudとsLoudの情報が載っている行だけ残す
                                processing.append(i)
                
                time = [0 for i in range(len(processing))] # time
                iLoud = [0 for i in range(len(processing))] # Integrated loudness
                mLoud = [0 for i in range(len(processing))] # Momentary loudness
                sLoud = [0 for i in range(len(processing))] # Short-term loudness
                for i in range(len(processing)): # いらん文字消して、欲しい数値だけ取得
                        processing[i] = processing[i].split("FTPK")[0] # FTPK以降の文字列をカット

                        processing[i] = deleteStr(processing[i], " ", "\n")
                        processing[i] = deleteAlphabet(processing[i]) # ここまでの状態→"(なんちゃら):t:TARGET:M:S:I:LRA"
                        splt = processing[i].split(":") # ここまでの状態→[(なんちゃら), t, TARGET, M, S, I, LRA]
                        
                        time[i] = round(float(splt[1]), 1)
                        if splt[3] == '':
                                mLoud[i] = -200.0
                        else:
                                mLoud[i] = float(splt[3])
                        if splt[4] == '':
                                sLoud[i] = -200.0
                        else:
                                sLoud[i] = float(splt[4])
                        if splt[5] == '':
                                iLoud[i] = -200.0
                        else:
                                iLoud[i] = float(splt[5])
                
                max_mLoud_value = str(max(mLoud)) # Momentary Loudnessの最大値を取得
                max_mLoud_value = adjustSpace(max_mLoud_value) # スペース調整
                max_mLoud_index = mLoud.index(max(mLoud)) # Momentary Loudnessの最大値とそのインデックスを取得

                max_sLoud_value = str(max(sLoud)) # Short-term Loudnessの最大値を取得
                max_sLoud_value = adjustSpace(max_sLoud_value) # スペース調整
                max_sLoud_index = sLoud.index(max(sLoud)) # Short-term Loudnessの最大値のインデックスを取得


                ### ラウドネス関連情報の取得 ###
                summary_index = max(searchIndex(log_0, "Summary:")) # ログの中から"Summary:"って書かれた行を探す
                summary = log_0[summary_index+2:summary_index+14] # 最後の出力結果のある行を取得

                # いらん行を指定して消す
                n=0 # 消した行分リストが短くなるので、そのつじつま合わせ
                for i in [0, 2, 3, 4, 6, 9, 10]:
                        del summary[i-n]
                        n += 1

                # いらん文字を消す
                for i in range(len(summary)):
                        summary[i] = deleteStr(summary[i], " ", "\n", ":")
                        summary[i] = deleteAlphabet(summary[i]) # こうなる→[Integrated Loudness, Loudness Range, - low, - high, True Peak]
                        summary[i] = adjustSpace(summary[i]) # スペース調整


                ### 通常ピークの取得 ###
                PK_index = max(searchIndex(log_1, "Sample peak:")) # "Sample peak:"って書かれた行を探す
                PK = log_1[PK_index+1] # 通常ピークの行を取得

                # いらん文字消す
                PK = deleteStr(PK, " ", "\n", ":")
                PK = deleteAlphabet(PK)

                # 入力ファイルのビット深度を取得
                bit_rate_index = min(searchIndex(log_1, "Audio: "))
                bit_rate = log_1[bit_rate_index]

                # 通常ピークが（なぜか）0dBFSを越えたときの対策
                bit_float = ["f32le", "f32be", "f64le", "f64be"]
                int_or_float = "int"
                for i in bit_float:
                        if i in bit_rate:
                                int_or_float = "float" # bit floatなら対策不要
                                break
                
                if int_or_float == "int":
                        if float(PK) > 0:
                                PK = "  0.0"
                
                PK = adjustSpace(PK) # スペース調整



                ### 結果まとめ ###
                # 作ったファイル消す
                for i in range(len(cmd)):
                        os.remove(logfiles[i])
                
                res = ["" for i in range(18)]
                n = 0
                res[0] = "Title: {}".format(audioName)
                res[1] = ""
                res[2] = "Peak"
                res[3] = "  Sample Peak               :  {} dBFS".format(PK)
                res[4] = "  True Peak                 :  {} dBTP ".format(summary[4])
                res[5] = ""
                res[6] = "Absolute Loudness"
                res[7] = "  Integrated Loudness       :  {} LUFS".format(summary[0])
                res[8] = "  Max. Momentary Loudness   :  {} LUFS (time: {} s)".format(max_mLoud_value, time[max_mLoud_index])
                res[9] = "  Max. Short-term Loudness  :  {} LUFS (time: {} s)".format(max_sLoud_value, time[max_sLoud_index])
                res[10] = ""
                
                if self.bln.get() == True:
                        LU = str(round(float(summary[0]) - float(self.targetEntry.get()), 1)) # iLoud(absolute) - target = iLoud(relative)
                        LU = adjustSpace(LU)
                        res[11] = "Relative Loudness"
                        res[12] = "  Integrated Loudness       :  {} LU".format(LU)
                        res[13] = ""
                        n = 3
                
                res[11+n] = "Loudness Range (LRA)"
                res[12+n] = "  Loudness Range            :  {} LU".format(summary[1])
                res[13+n] = "    - High                  :  {} LUFS".format(summary[3])
                res[14+n] = "    - Low                   :  {} LUFS".format(summary[2])

                return res, time, mLoud, sLoud, iLoud, audioName
        


if __name__ == '__main__':
        # 残ってしまった.logを消す
        logfiles = searchFile(r"^ffmpeg-\d{8}-\d{6}.log$")
        if len(logfiles) != 0:
                for i in range(len(logfiles)):
                        os.remove(logfiles[i])

        app  = tk.Tk()
        app.geometry("430x620")
        app.resizable(0,0)
        app.title("Loudness Checker {}".format(ver))

        app.iconbitmap(default=resource_path("src/icon.ico"))

        frame = FiledialogSampleApp(app)

        app.mainloop()