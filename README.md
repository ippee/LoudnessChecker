# Loudness Checker
「**Loudness Checker**」とは、入力したオーディオやビデオのピークやラウドネス（アルゴリズム：EBU R128）を計測するプログラムおよびアプリです  
**本アプリの使用にはffmpegのインストールが必須です**、各自でインストールをお願いいたします  
  　  
DTMをやっていると、色んな曲のラウドネスを計測したくなることが多々あります  
ただ、その度にDAWを起動して、プロジェクト立ち上げて、楽曲を読み込んで……  
っていう手間が死ぬほど面倒だったので、スタンドアロンで動くアプリを作りました  
同じことを思っているDTMerは多いと思うので、このアプリが楽曲制作の手助けになれば幸いです  
  　  
  　  
## 使い方
色々とファイルがありますが、アプリ単体で使う場合は.exeファイルだけあれば大丈夫です  
  　  
使い方についてですが、難しいことは何もなくて、
1. **Loudness Checker.exe** を起動
2. **Browse…** からファイルを指定 or ファイルのパスをテキストボックスに入力
3. **Analyze** をクリックで解析開始、謎ウインドウが出てくるけど、しばし待て
4. **Result** に結果が出力される
  
これだけ、超簡単です  
  　  
アプリにファイルを入力すると、
- **Peak** \[dBFS]
- **True Peak** \[dBTP]
- **Integrated Loudness** \[LUFS]
- **Max. Momentary Loudness** \[LUFS]
- **Max. Short-term Loudness** \[LUFS]
- **Loudness Range** \[LU]
  - **High** \[LUFS]
  - **Low** \[LUFS]
  
を、一括出力します  
  　  
対応ファイルは、  
- Audio: mp3, ogg, wav, flac, aac, ac3, m4a, wma, mp1, mp2, aif, aiff, alac, aifc, opus, asf  
- Video: mp4, avi, flv, webm, wmv, mpg, m2ts, vob, mov, mkv, tc7, 3gp, 3g2

です  
有名所は揃ってると思うので、とりあえずは困らないかと  
ffmpeg自体はもっと多くのファイルに対応していますが、これ以上調べるのは面倒なのでもう増やさないと思います（おい）  
増やせッ！っていう要望があれば考えます  
  　  
### バグったら？
私が把握している範囲で起きたバグについて対処法を書きます
- 何らかの理由で処理が止まったりフリーズしたらアプリを再起動してください、大体治ると思います
- コマンドプロンプトが消えたらすぐに結果が出力されますが、稀に出力されないまま **Running…** で止まっていることがあります  
そういう時は再起動してもう一回分析してみてください  
- ファイルのパスをコピぺして入力した場合、パスの前後に **"** が含まれます  
そのまま **Analyze** を押しても読み取ってくれないので、**"** を消してから実行してください

他に謎現象が起きたら連絡ください（Twitter:@ippee1410）  
  　  
### アプリ実行したら謎ファイルが生成されるんだけど……！？
このアプリは、分析中に「ffmpeg-(日付)-(時間).log」を生成します  
.logファイルには分析結果などが書いており、これを編集して **Result** に出力するために使います  
  　  
分析終了時にファイルは自動で削除されますが、何らかの理由で処理が中断されたりすると残る場合があります  
が、アプリを再起動すると消えます、手動で消しても問題ありません  
  　  
  　  
## 注意事項
1. 例のごとく「動けばなんでもいいだろ精神」で作っているので、コードの見やすさとかほとんど考えていないです()  
見にくかったらごめんなさい  
見やすいコードを書けるようになったら改訂する<u>かも</u>しれません  
  　  
2. <font color="red">**本アプリを使用していかなる損害が発生したとしても、私は一切の責任を負いかねますのでご了承ください**</font>  
  　  
  　  
## その他（補足など）
- 作業環境
  - Windows 10
  - Python 3.6.4
  　  
  　  
## 特に参考にしたサイト
- Documentation | FFmpeg
  - https://ffmpeg.org/documentation.html
  - ffmpegの公式リファレンス
- ラウドネス測定手順 | Studio Gyokimae
  - https://pspunch.com/pd/article/measuring_loudness/
  - ffmpegでラウドネスを測れるって初めて知ったサイト
- 【Python GUIサンプル】Tkinterでfiledialog(ファイルダイアログ)を使ってみる | エンジニアになりたいブログ
  - https://suzutaka-programming.com/tkinter-filedialog/
  - このサイトが無かったらここまでのGUIは作れなかった
