# coding: UTF-8

# 
# LoudnessChecker.py
#
# Copyright (c) 2020 Ippee
#
# Released under the MIT license.
# see https://github.com/ippee/LoudnessChecker/blob/master/LICENSE
# 
# Python 3.6.4 is:
# PSF LICENSE AGREEMENT FOR PYTHON 3.6.10 | https://docs.python.org/3.6/license.html
# 
# Matplotlib 3.1.3 is:
# License agreement for matplotlib 3.1.3 | https://matplotlib.org/users/license.html
# 

version = "Ver. 2.1.0"

import sys
import re
import os
from time import sleep
import webbrowser
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import matplotlib.pyplot as plt
from matplotlib import rcParams
from src.FFmpeg_FileExt import getExtList


### 関数定義 ###
# リソースファイルを参照する関数
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.abspath(relative_path)


# 文字列がfloatに変換できるかどうかを判断する関数
def is_float(s):
        try:
                float(s)
        except:
                return False
        return True

# キーワードをファイル名に含むファイルの一覧を取得
def searchFile(keyword):
        key_re = re.compile(r"(" + keyword + r")") # 正規表現に変換
        folders = os.listdir(os.getcwd()) # カレントディレクトリにあるファイル全部Get
        getfiles = []

        for x in folders:
                if key_re.search(x):
                        getfiles.append(x)
        return getfiles

# ファイルの読み込み
def readFile(fileName):
        f = open(fileName, 'r', encoding='utf-8')
        file = f.readlines()
        f.close()
        return file

# 0.1秒後のファイルサイズが同じかどうかをチェック
def checkSize(size, file):
        size[0] = os.path.getsize(file)
        sleep(0.1)
        size[1] = os.path.getsize(file)
        if size[0] == size[1]:
                return True
        else:
                return False

# 指定した文字を消す
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



### 音声処理 ###
class CheckLoudness:
        def __init__(self, path, target):
                self.path = path
                self.target = target
                
        def audioAnalyze(self):
                audioName = self.path[self.path.rfind( "/" ) + 1 : len(self.path)] # ファイル名取得
                self.path = '"{}"'.format(self.path) # タイトルにスペースがあるとコマンドがバグるんで、その対策

                # ffmpegコマンド定義
                cmd = ["" for i in range(2)]
                cmd[0] = "start ffmpeg -report -hide_banner -nostats -i {} -filter_complex ebur128=peak=true -f null -".format(self.path) # ラウドネス関連の情報取得
                cmd[1] = "start ffmpeg -report -hide_banner -nostats -i {} -filter_complex ebur128=peak=sample -f null -".format(self.path) # 通常ピークの情報取得

                # コマンド実行
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
                                                messagebox.showerror("ERROR", "Analysis failed!\n\nExit the ffmpeg.exe and rerun this analysis.")
                                                
                                                for i in range(len(cmd)):
                                                        os.remove(logfiles[i]) # 出力された.logファイルを消す
                                                
                                                return "break!"
                        

                ### mLoud, sLoudの時系列データを取得 ###
                processing = [] # ログの情報を編集するために使う
                for i in log_0:
                        if "TARGET:-23 LUFS" in i: # mLoudとsLoudの情報が載っている行だけ残す
                                processing.append(i)
                
                time = [0 for i in range(len(processing))] # time
                iLoud = [0 for i in range(len(processing))] # Integrated loudness
                mLoud = [0 for i in range(len(processing))] # Momentary loudness
                sLoud = [0 for i in range(len(processing))] # Short-term loudness

                for i in range(len(processing)): 
                        processing[i] = processing[i].split("FTPK")[0] # FTPK以降の文字列をカット

                        processing[i] = deleteStr(processing[i], " ", "\n") # いらん文字消す
                        processing[i] = deleteAlphabet(processing[i]) # アルファベット消す、ここまでの状態→"(なんちゃら):t:TARGET:M:S:I:LRA"
                        splt = processing[i].split(":") # ここまでの状態→[(なんちゃら), t, TARGET, M, S, I, LRA]
                        
                        # 出力結果を変数に入れる
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
                
                max_mLoud_value = max(mLoud) # Momentary Loudnessの最大値を取得
                max_mLoud_index = mLoud.index(max_mLoud_value) # Momentary Loudnessの最大値とそのインデックスを取得

                max_sLoud_value = max(sLoud) # Short-term Loudnessの最大値を取得
                max_sLoud_index = sLoud.index(max_sLoud_value) # Short-term Loudnessの最大値のインデックスを取得


                ### summaryの取得 ###
                summary_index = max(searchIndex(log_0, "Summary:")) # ログの中から"Summary:"って書かれた行を探す
                summary = log_0[summary_index+2:summary_index+14] # 最後の出力結果のある行を取得

                # いらん行を指定して消す
                n = 0 # 消した行数分リストが短くなるので、そのつじつま合わせ
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
                # 出力された.logファイルを消す
                for i in range(len(cmd)):
                        os.remove(logfiles[i])
                
                res = ["" for i in range(22)]
                n = 0
                res[0] = "Title: {}".format(audioName)
                res[1] = ""
                res[2] = "Peak"
                res[3] = "  Sample Peak               :  {} dBFS".format(PK)
                res[4] = "  True Peak                 :  {} dBTP ".format(summary[4])
                res[5] = ""
                res[6] = "Target                      :  {} LUFS".format(adjustSpace(str(self.target)))
                res[7] = ""
                res[8] = "Absolute Scale"
                res[9] = "  Integrated Loudness       :  {} LUFS".format(summary[0])
                res[10] = "  Max. Momentary Loudness   :  {} LUFS (time: {} s)".format(adjustSpace(str(max_mLoud_value)), time[max_mLoud_index])
                res[11] = "  Max. Short-term Loudness  :  {} LUFS (time: {} s)".format(adjustSpace(str(max_sLoud_value)), time[max_sLoud_index])
                res[12] = ""
                
                if self.target != "N/A":
                        iLU = str(round(float(summary[0]) - self.target, 1)) # iLoud(absolute) - target = iLoud(relative)
                        mLU = str(round(max_mLoud_value - self.target, 1)) # mLoud(absolute) - target = mLoud(relative)
                        sLU = str(round(max_sLoud_value - self.target, 1)) # sLoud(absolute) - target = sLoud(relative)

                         # スペース調整
                        iLU = adjustSpace(iLU)
                        mLU = adjustSpace(mLU)
                        sLU = adjustSpace(sLU)

                        res[13] = "Relative Scale"
                        res[14] = "  Integrated Loudness       :  {} LU".format(iLU)
                        res[15] = "  Max. Momentary Loudness   :  {} LU (time: {} s)".format(mLU, time[max_mLoud_index])
                        res[16] = "  Max. Short-term Loudness  :  {} LU (time: {} s)".format(sLU, time[max_sLoud_index])
                        res[17] = ""
                        n = 5

                res[13+n] = "Loudness Range (LRA)"
                res[14+n] = "  Loudness Range            :  {} LU".format(summary[1])
                res[15+n] = "    - High                  :  {} LUFS".format(summary[3])
                res[16+n] = "    - Low                   :  {} LUFS".format(summary[2])

                return res, time, mLoud, sLoud, iLoud, audioName



# グラフ出力
class ResultPlot:
        def __init__(self, time, mLoud, sLoud, iLoud, audioName, target):
                self.time = time
                self.mLoud = mLoud
                self.sLoud = sLoud
                self.iLoud = iLoud
                self.audioName = audioName
                self.target = target

                
                g_m = plt.plot(self.time, self.mLoud, label="Momentary", color="blue")
                g_s = plt.plot(self.time, self.sLoud, label="Short-term", color="yellow")
                g_i = plt.plot(self.time, self.iLoud, label="Integrated", color="red")

                RL = self.iLoud[round(len(self.iLoud)/2)] - 10 # 下方向の表示範囲
                RH = max(self.mLoud) + 5 # 上方向の表示範囲
                if self.target != "N/A":
                        targetLine = plt.hlines([self.target], self.time[0], self.time[len(self.time)-1], "black", linestyles="dashed")

                        # Targetに合わせてグラフの表示範囲を変更
                        if RL > self.target:
                                RL = self.target - 2
                                RH = max(self.mLoud) + 3
                        if RH < self.target:
                                RL = self.iLoud[len(self.iLoud)-1] - 3
                                RH = self.target + 2
                        
                plt.ylim(RL, RH)
                plt.title("Result - {}".format(self.audioName), fontsize=18)
                plt.ylabel("Loudness [LUFS]")
                plt.xlabel("Time [s]")
                plt.legend()
                plt.show()



### GUI作成 ###
class LoudnessCheckerGUI(ttk.Frame):
        def __init__(self, root, settings, ext_list):
                super().__init__(root)
                self.pack()
                self.settings = settings
                self.ext_list = ext_list

                # 画面の分割
                pw_main = tk.PanedWindow(self, sashwidth=4, orient="horizontal") # ペインドウインドウ作る
                pw_main.pack(side="top", fill="both")

                frm_input = tk.Frame(pw_main, bd=2, relief="ridge") # フレームを使って左右に分割
                frm_result = tk.Frame(pw_main, bd=2, relief="ridge")
                pw_main.add(frm_input)
                pw_main.add(frm_result)


                # メニューバー作成
                menubar = tk.Menu(self)
                
                menu = tk.Menu(menubar, tearoff=0)
                menu.add_command(label="Help", command=self.showHelp)
                menu.add_command(label="Preferences", command=self.showPref)
                menu.add_separator()
                menu.add_command(label="About Loudness Checker", command=self.aboutLoudnessChecker)
                menubar.add_cascade(label="Menu", menu=menu)

                root.config(menu=menubar)


                # ウィジェット用変数を定義
                self.filepath = tk.StringVar() # 入力したパスを入れる変数
                self.correntDir = os.getcwd() # カレントディレクトリ取得、ダイアログの表示に使う
                self.target = tk.StringVar() # Targetを入れる変数
                if self.settings[1]=="N/A":
                        self.target.set("")
                else:
                        self.target.set(self.settings[1])
                

                # ウィジェット配置
                label_title = ttk.Label(frm_input, text="Loudness Checker", font=("","20","bold")) # タイトル
                label_title.pack(side="top", pady=5)

                label_expainApp = ttk.Label(frm_input, justify="center",text="- {} -\nAlgorithm: EBU R128\n".format(version), font=("","12")) # アプリ説明文
                label_expainApp.pack(side="top")
                
                label_path = ttk.Label(frm_input,justify="center",text="Audio / Video file path", font=("","14","bold")) # Auidio / Video file path
                label_path.pack(side="top")

                label_Codecs = ttk.Label(frm_input,justify="center",text="Codecs: wav, mp3, ogg, flac, mp4, avi, flv, etc.", font=("","12")) # 対応コーデック
                label_Codecs.pack(side="top")

                self.entry_filepath = ttk.Entry(frm_input,text="", font=("","10"), width=62, justify="center", textvariable= self.filepath) # パス入力
                self.entry_filepath.pack(side="top", padx=5) # パス入力ボックス配置

                button_open = ttk.Button(frm_input,text="Browse…",command = self.openFileDialog) # 参照ボタン
                button_open.pack(side="top", pady=5)
                
                label_target = ttk.Label(frm_input,justify="center",text="\nTarget", font=("","14","bold")) # Target
                label_target.pack(side="top")

                label_explainTarget = ttk.Label(frm_input,justify="center",text="Set a loudness target [LUFS]\n(Leaving this field blank will disable the target. )", font=("","12")) # Target
                label_explainTarget.pack(side="top")

                self.entry_target = ttk.Entry(frm_input,text="", font=("","10"), width=62, justify="center", textvariable= self.target) # Target入力
                self.entry_target.pack(side="top", padx=5) # Target入力ボックス配置

                self.button_analyze = ttk.Button(frm_input,text="Analyze",command = self.clickedAnalyze) # アナライズボタン
                self.button_analyze.pack(side="top", pady=17) # 分析ボタン配置

                label_res = ttk.Label(frm_result,text="Result", font=("","14","bold")) # Result
                label_res.pack(side="top", pady=10)
                
                self.textbox = tk.Text(frm_result, width=400, height=400) # Resultのテキストボックス
                self.textbox.pack(side="top", padx=5) # Result配置


        # About Loudness Checkerを開く
        def aboutLoudnessChecker(self):
                aboutWindow = tk.Toplevel(self) # アプリ紹介ウインドウ表示
                aboutWindow.geometry("400x250")
                aboutWindow.resizable(0,0)
                aboutWindow.title("About Loudness Checker")

                label_appName = ttk.Label(aboutWindow, justify="center", text="Loudness Checker {}".format(version), font=("","14","bold"))
                label_appName.pack(side="top", pady=5)
                label_license = ttk.Label(aboutWindow, justify="left", text="\n- Copyright (c) 2020 Ippee\n\n- This application is released under the MIT License, \n   see MIT_LICENSE.txt.\n\n- Loudness Checker uses   Python 3.6.4\n" + " "*37 + "Matplotlib 3.1.3\n", font=("","12"))
                label_license.pack(side="top")

                # リンク追加
                link = ttk.Label(aboutWindow, justify="left", text="https://github.com/ippee/LoudnessChecker", foreground="blue", font=("","12","normal","roman", "underline"))
                link.pack(side="top")
                link.bind("<Button-1>", lambda self: webbrowser.open("https://github.com/ippee/LoudnessChecker"))

                button_close_a = ttk.Button(aboutWindow, text="Close", command=aboutWindow.destroy)
                button_close_a.pack(side="top", pady=10)
        

        # ヘルプを開く
        def showHelp(self):
                webbrowser.open(resource_path("src/Help.html"))
        

        # 設定を開く
        def showPref(self):
                # 初期設定読み込み
                def_target = tk.StringVar() 
                if self.settings[1] == "N/A":
                        def_target.set("")
                else:
                        def_target.set(self.settings[1])

                # 設定ウインドウ表示
                pref = tk.Toplevel(self) # Preferencesのウインドウ
                pref.geometry("250x150")
                pref.resizable(0,0)
                pref.title("Preferences")

                label_title_p = ttk.Label(pref, justify="left", text="Default Settings", font=("","14","bold"))
                label_title_p.pack(side="top", padx=5, pady=5)

                label_target_p = ttk.Label(pref, justify="center", text="Default target value [LUFS]", font=("","12"))
                label_target_p.pack(side="top", padx=5, pady=5)

                entry_target_p = ttk.Entry(pref,text="", font=("","10"), width=100, justify="center", textvariable=def_target)
                entry_target_p.pack(side="top", padx=5, pady=5)

                button_save_p = ttk.Button(pref, text="Save", command = lambda: self.saveSettings(pref, def_target))
                button_save_p.pack(side="left", padx=20, pady=5)

                button_close_p = ttk.Button(pref, text="Close", command = pref.destroy)
                button_close_p.pack(side="right", padx=20, pady=5)
        

        # 設定の保存
        def saveSettings(self, pref, def_target):
                if is_float(def_target.get()) == True:
                        target = def_target.get()
                elif def_target.get()=="":
                        target = "N/A"
                elif is_float(def_target.get()) == False:
                        messagebox.showerror("ERROR", "Set a valid target!")
                        return "break" # "break" ないとPreferencesが閉じる

                self.settings[1] = target

                # setting.ini書き出し
                f = open("setting.ini", 'w', encoding='utf-8')
                for i in range(len(self.settings)):
                        f.write(str(self.settings[i]))
                f.close()

                pref.destroy()

                messagebox.showinfo("Info", "Settings ware saved!")

                
        # ファイルダイアログを開いてentry_filepathに反映させる
        def openFileDialog(self):
                file = filedialog.askopenfilename(initialdir = self.correntDir)
                if file == "":
                        return "break"
                self.correntDir = file[0:file.rfind( "/" ) + 1] # 再びダイアログを開いたとき、さっき選択したファイルの所からスタートする
                self.filepath.set(file)
        

        # アナライズボタンクリック時
        def clickedAnalyze(self):
                if self.filepath.get() == "":
                        messagebox.showerror("ERROR", "Enter a valid path!")
                        return
                
                target = self.entry_target.get()
                if target == "":
                        target = "N/A"
                elif is_float(target) == False:
                        messagebox.showerror("ERROR", "Set a valid target!")
                        return
                else:
                        target = float(target)

                path = self.entry_filepath.get()
                path = deleteStr(path, '"', "'") # pathに " とか ' が含まれていても一旦消す
                path = path.replace("\\", "/") # スラッシュを統一
                ext = path[path.rfind(".")+1 : len(path)] # 拡張子取得

                # 入力されたファイルがffmpegに対応しているかチェック
                if ext not in self.ext_list:
                        messagebox.showerror("ERROR", "This file or path is invalid!")
                        self.button_analyze.config(state="active", text="Analyze")
                        return

                self.button_analyze.config(state="disable", text="Runing…") # ボタン止める
                plt.close() # グラフ開いてたら閉じる
                
                CL = CheckLoudness(path, target)
                res, time, mLoud, sLoud, iLoud, audioName = CL.audioAnalyze() # 分析結果とファイル名を取得

                if res == "b": # "break!"が帰ってきたら分析結果の出力を中止
                        return
                
                self.button_analyze.config(state="active", text="Analyze") # ボタン復活

                self.textbox.delete("1.0", "end") # テキストボックスを空にする
                for i in range(len(res)):
                        self.textbox.insert(str(i+1)+".0", res[i]+"\n") # 結果をテキストボックスに出力
                
                ResultPlot(time, mLoud, sLoud, iLoud, audioName, target) # グラフ出力
        


if __name__ == '__main__':
        # matplotlibのフォント設定
        rcParams['font.family'] = 'sans-serif' # フォント設定
        rcParams['font.sans-serif'] = ['Yu Gothic', 'Meiryo', 'Arial', 'Hiragino Maru Gothic Pro'] # ヒラギノはもしMacで動かそうとする人がいた用

        # 残ってしまった.logを消す
        logfiles = searchFile(r"^ffmpeg-\d{8}-\d{6}.log$")
        if len(logfiles) != 0:
                for i in range(len(logfiles)):
                        os.remove(logfiles[i])
        
        # root設定
        root = tk.Tk()
        root.geometry("900x370")
        root.resizable(0,0)
        root.title("Loudness Checker {}".format(version))
        root.iconbitmap(default=resource_path("src/icon.ico"))

        # 初期設定読み込み
        if "setting.ini" not in os.listdir(os.getcwd()):
                messagebox.showwarning("WARNING", '"setting.ini" is missing!\nInitialize all settings.')
                factory_settings = '[Target_value] ;Enter a float or "N/A"(strings)\nN/A'
                f = open("setting.ini", 'w', encoding='utf-8')
                f.write(factory_settings)
                f.close()
        
        settings = readFile("setting.ini") # setting.ini読み込み、targetの初期値が入ってる

        # ffmpegが対応しているコーデックのリストを取得
        ext_list = getExtList()

        # GUI生成
        LoudnessCheckerGUI(root, settings, ext_list)

        root.mainloop()