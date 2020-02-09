# Loudness Checker
「**Loudness Checker**」とは、入力したオーディオやビデオのピークやラウドネス（アルゴリズム：EBU R128）を計測するプログラムおよびアプリケーションです  
　  
**本アプリの使用にはFFmpegのインストールが必須です**、各自でインストールをお願いいたします  
（ググれば方法が出てきます、下にもwindowsのリンクを貼っています）  
このアプリ関係なしにFFmpegは超有能なのでインストールしましょう  
　  
DTMをやっていると、色んな曲のラウドネスを計測したくなることが多々あります  
ただ、その度にDAWを起動して、プロジェクト立ち上げて、楽曲を読み込んで……  
っていう手間が死ぬほど面倒だったので、スタンドアロンで動くアプリを作りました  
このアプリが楽曲制作の手助けになれば幸いです  
　  
**LoudnessChecker.exe**  
**https://drive.google.com/open?id=1yMVZuCFk6LEahGO7TRchBEN8EyZCmPeJ**  
　  
**FFmpeg**  
**https://www.ffmpeg.org/**  
　  
**【windows】FFmpegをインストールする手順｜新卒エンジニアの開発日記**  
**https://fukatsu.tech/windows-ffmpeg**  
　  
　  
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
　  
対応ファイルは、  
- Audio: mp3, ogg, wav, flac, aac, ac3, m4a, wma, mp1, mp2, aif, aiff, alac, aifc, opus, asf  
- Video: mp4, avi, flv, webm, wmv, mpg, m2ts, vob, mov, mkv, tc7, 3gp, 3g2

です  
有名所は揃ってると思うので、とりあえずは困らないかと  
FFmpeg自体はもっと多くのファイルに対応していますが、これ以上調べるのは面倒なのでもう増やさないと思います（おい）  
増やせッ！っていう要望があれば考えます  
　  
### バグったら？
私が把握している範囲で起きたバグについて対処法を書きます
- 何らかの理由でアプリの処理が止まったりフリーズしたら、とりあえず再起動してください
- FFmpegのコンソールが消えたらすぐに結果が出力されますが、稀に出力されないまま **Running…** で止まっていることがあります  
そういう時はアプリを再起動してもう一回分析してみてください
- 分析中に出てくるコンソールの画面内をクリックすると処理が停止してバグります  
処理中の画面は触らずに待ちましょう  
- ファイルのパスをコピぺして入力した場合、パスの前後に **"** が含まれます  
そのまま **Analyze** を押しても読み取ってくれないので、**"** を消してから実行してください

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
- 作業環境
  - Windows 10
  - Python 3.6.4
　  
　  
## 更新履歴
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
  - このサイトが無かったらここまでのGUIは作れなかった
