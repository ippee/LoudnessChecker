# Loudness Checker
「**Loudness Checker**」とは、入力したオーディオやビデオのピークやラウドネス（アルゴリズム：EBU R128）を計測するプログラムおよびアプリケーションです  
　  
**本アプリの使用にはFFmpegのインストールが必須です**、各自でインストールをお願いいたします  
このアプリ関係なしにFFmpegは超有能なのでインストールしましょう  
（インストール方法を１行で説明すれば、FFmpegダウンロードして解凍してどっかに保存して環境変数Path設定すれば完了）  
（ググれば具体的な方法が出てきます、下にもwindowsのリンクを貼っています）  
　  
DTMをやっていると、色んな曲のラウドネスを計測したくなることが多々あります  
ただ、その度にDAWを起動して、プロジェクト立ち上げて、楽曲を読み込んで……  
っていう手間が死ぬほど面倒だったので、スタンドアロンで動くアプリを作りました  
このアプリが楽曲制作の手助けになれば幸いです  
　  
**LoudnessChecker.exe**（Ver. 1.4.3）  
https://drive.google.com/open?id=13KVBC-UYAaCU7e76l1XcXg1h-lLkakBS  
　  
**FFmpeg**  
https://www.ffmpeg.org/ （公式HP）  
https://ffmpeg.zeranoe.com/builds/ （FFmpegダウンロード）  
　  
**【windows】FFmpegをインストールする手順｜新卒エンジニアの開発日記**（参考）  
https://fukatsu.tech/windows-ffmpeg  
　  
　  
![GUI](https://raw.githubusercontent.com/ippee/LoudnessChecker/master/Picture/GUI.jpg)

![Plot](https://raw.githubusercontent.com/ippee/LoudnessChecker/master/Picture/plot.jpg)

　  
　  
## 使い方
アプリ単体で使う場合は.exeファイルだけあれば大丈夫です（アプリはWindows専用です）  
ソースコードを使うならPythonが必要です（3.6以外のバージョンで動くかは不明、Windows以外のOSで動くかも不明）  
　  
使い方は何も難しいことはなくて、
1. **Loudness Checker.exe** を起動
2. **Browse…** からファイルを指定 or ファイルのパスをテキストボックスに入力
3. **Target** を決める（不要ならチェックを外す）
4. **Analyze** をクリックで解析開始、謎ウインドウが出てくるけど、しばし待たれよ
5. **Result** に結果（グラフ付き）が出力される
  
これだけ、超簡単です  
　  
アプリにファイルを入力すると、
- **Sample Peak** \[dBFS]
- **True Peak** \[dBTP]
- **Integrated Loudness** (Absolute Scale) \[LUFS]
- **Integrated Loudness** (Relative Scale) \[LU] (Target指定時のみ表示)
- **Max. Momentary Loudness** \[LUFS]
- **Max. Short-term Loudness** \[LUFS]
- **Loudness Range** \[LU]
  - **High** \[LUFS]
  - **Low** \[LUFS]
  
が、一括出力されます  
　  
**FFmpegがサポートしている全てのオーディオ/ビデオ形式に対応しました！**  
2.1 File Formats - General Documentation | FFmpeg  
http://www.ffmpeg.org/general.html#File-Formats
　  
### バグったら？
私が把握している範囲で起きたバグについて対処法を書きます
- 何らかの理由でアプリの処理が止まったりフリーズしたら、とりあえず再起動してください
- 分析中に出てくるコンソールの画面内をクリックすると処理が停止してバグります  
処理中の画面は触らずに待ちましょう  

他に謎現象が起きたら連絡ください（Twitter: @ippee1410）  
　  
### アプリ実行したら謎ファイルが生成されるんだけど……！？
このアプリは、分析中に「FFmpeg-(日付)-(時間).log」を生成します  
.logファイルには分析結果などが書いており、これを編集して **Result** に出力するために使います  
　  
分析終了時にファイルは自動で削除されますが、何らかの理由で処理が中断されたりすると残る場合があります  
が、アプリを再起動すると消えます、手動で消しても問題ありません  
　  
　  
## 注意事項
1. Pythonで動いているので、基本的に挙動は遅いです  
特に起動には時間がかかります、気長に待ってください  
2. 例のごとく「動けばなんでもいいだろ精神」で作っているので、コードの見やすさとかほとんど考えていないです()  
見にくかったらごめんなさい  
見やすいコードを書けるようになったら改訂する<u>かも</u>しれません  
3. <font color="red">**本アプリを使用していかなる損害が発生したとしても、私は一切の責任を負いかねますのでご了承ください**</font>  
　  
　  
## その他（補足など）
### アプリについて
- **Loudness Checker Ver. 1.4.3**
- Copyright (c) 2020 Ippee
- このソースコード、およびアプリケーションはMIT Licenseのもとで公開されています。
- 制作者: Ippee / いっぺー（Twitter: @ippee1410）
- 動作環境: 
  - Windows 10
  - FFmpeg
- 使用言語 / ライブラリ:
  - Python 3.6.4 (Copyright (c) 2001 Python Software Foundation; All Rights Reserved)
  - Matplotlib 2.2.2 (Copyright (c) 2012-2013 Matplotlib Development Team; All Rights Reserved)
　  
　  
## 更新履歴
- 2020/02/12: 測定エラー時の対応を修正（V1.4.3）
- 2020/02/11: フォーマット判別のプログラムを修正（V1.4.2）
- 2020/02/10: 対応フォーマット拡張、ファイルパス入力時のバグ対応、非bit float音源のピークが（なぜか）0dBFSを超えたときの対応を修正（V1.4）
- 2020/02/10: TargetチェックボックスのT/Fにテキストボックスが反応、ログ編集アルゴリズムの見直し（V1.3）
- 2020/02/09: Relative Scaleに対応、Resultの表示を調整（V1.2）
- 2020/02/08: グラフ出力機能の追加（V1.1）
- 2020/02/07: 本アプリ公開（V1.0）
　  
　  
## 特に参考にしたサイト
- **Documentation | FFmpeg**
  - https://ffmpeg.org/documentation.html
  - FFmpegの公式リファレンス
- **ラウドネス測定手順 | Studio Gyokimae**
  - https://pspunch.com/pd/article/measuring_loudness/
  - FFmpegでラウドネスを測れるって初めて知ったサイト
- **LUFS/LKFS…ラウドネスメーターについて復習して理解を深めよう | SOUNDEVOTEE.NET**
  - https://soundevotee.net/blog/2017/04/25/learning_about_loudness_meter/
  - ラウドネスの勉強に用いたサイト
- **【Python GUIサンプル】Tkinterでfiledialog(ファイルダイアログ)を使ってみる | エンジニアになりたいブログ**
  - https://suzutaka-programming.com/tkinter-filedialog/
  - このサイトが無かったらGUIは作れなかった
