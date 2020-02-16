# Loudness Checker
「**Loudness Checker**」とは、入力された音声/映像のピークやラウドネス（アルゴリズム：EBU R128）を計測するWindows専用アプリケーションです  
　  
**本アプリの使用にはFFmpeg (https://www.ffmpeg.org/) のインストールが必須です**  
このアプリ関係なしにFFmpegは超有能なのでインストールしましょう  
**（インストール方法を下記に記載）**  
　  
DTMをやっていると、色んな曲のラウドネスを計測したくなることが多々あります  
ただ、その度にDAWを起動して、プロジェクト立ち上げて、楽曲を読み込んで、再生して……  
っていう手間が死ぬほど面倒だったので、DAWなし単体で動くアプリを作りました  
このアプリが楽曲制作の手助けになれば幸いです  
　  
**Download: LoudnessChecker.zip**（Ver. 2.2.1）  
https://drive.google.com/open?id=13KVBC-UYAaCU7e76l1XcXg1h-lLkakBS  
　  
**Help: How To Use Loudness Checker**  
https://ippee.github.io/LoudnessChecker/  
　  
セキュリティによってダウンロードがブロックされる可能性がありますが、  
それはこのアプリにコード署名とかコードサイニング証明書がないから（らしい）ので、  
アプリ起動したらPCが爆発するとか、そういうことはないのでご安心ください  
　  
　  
![GUI](https://raw.githubusercontent.com/ippee/LoudnessChecker/master/Picture/GUI.jpg)

![Plot](https://raw.githubusercontent.com/ippee/LoudnessChecker/master/Picture/plot.jpg)  
Powered by matplotlib 3.1.3  

　  
　  
## FFmpegについて
**FFmpeg**とは、the FFmpeg developersが開発したフリーのクロスプラットフォーム・マルチメディアフレームワークであり、動画や音声の再生・記録・デコード・エンコード等の処理が行えます  
　  
下記URLより、使用しているPCに適したファイルをダウンロードし、以下の手順でインストールしてください  
　  
**Builds - Zeranoe FFmpeg**  
https://ffmpeg.zeranoe.com/builds/  
　  
### インストール手順
1. ダウンロードしたファイルを解凍し、任意の場所に保存  
（"C:\Program Files" または "C:\Program Files (x86)" をおすすめします）
2. "Windowsキー+Pause/Break" 等からコントロールパネルのシステムを起動
3. 左のリストからシステムの詳細設定をクリックし、詳細設定→環境変数を開く
4. ユーザー環境変数からPathを選択し、編集をクリック
5. 新規→参照と順にクリックするとダイアログが現れ、  
保存したFFmpegのファイルの中から "bin" フォルダを選択し、OKをクリック（インストール完了）
　  
　  
## 使い方
難しいことは何もなくて、
1. **Loudness Checker.exe** を起動（ちょっと時間かかる）
2. **Browse…** からファイルを指定 or ファイルのパスをテキストボックスに入力
3. **Target** を決める（不要なら空欄にする）
4. **Scale** でグラフの表示範囲を決める
5. **Analyze** をクリックで解析開始、謎ウインドウが出てくるけど、しばし待たれよ
6. **Result** に結果（グラフ付き）が出力される
  
これだけ、超簡単です  
　  
アプリにファイルを入力すると、
- **Sample Peak** \[dBFS]
- **True Peak** \[dBTP]
- **Target** \[LUFS] (Target指定時のみ、Relative Scaleの結果も表示する)
- **Integrated Loudness** (Absolute/Relative Loudness) \[LUFS, LU]
- **Max. Momentary Loudness** (Absolute/Relative Loudness) \[LUFS, LU]
- **Max. Short-term Loudness** (Absolute/Relative Loudness \[LUFS, LU]
- **Loudness Range** \[LU]
  - **High** \[LUFS]
  - **Low** \[LUFS]
  
が、一括出力されます  
　  
もうちょっと詳しい使い方については、下リンクより**Help**をご覧ください  
https://ippee.github.io/LoudnessChecker/  
　  
### 対応ファイル
**FFmpegがサポートしている全てのオーディオ/ビデオ形式に対応しました！**  
- Audio: wav, flac, aifc, aiff, wma, mp3, ogg, ac3, m4a, etc.
- Video: avi, wmv, flv, mp4, 3g2, 3gp, etc.

その他の対応形式については、以下のサイトをご確認ください  
2.1 File Formats - General Documentation | FFmpeg  
http://www.ffmpeg.org/general.html#File-Formats
　  
### バグったら？
私が把握している範囲で起きたバグについて対処法を書きます
- 何らかの理由でアプリの処理が止まったりフリーズしたら、とりあえず再起動してください
- 分析中に出てくるコンソールの画面内をクリックすると処理が停止してエラーを吐きます  
処理中の画面は触らずに待ちましょう  
気になる人は、ffmpeg.exeの簡易編集モードをオフにしてください

他に謎現象が起きたら連絡ください（Twitter: @ippee1410）  
　  
### アプリ実行したら謎ファイルが生成されるんだけど……！？
このアプリは、分析中に「FFmpeg-(日付)-(時間).log」を生成します  
.logファイルには分析結果などが書いており、これを編集して **Result** に出力するために使います  
　  
分析終了時にファイルは自動で削除されますが、何らかの理由で処理が中断されたりすると残る場合があります  
が、アプリを再起動すると消えます、手動で消しても問題ありません  
　  
　  
## 注意事項
<font color="red">**本アプリを使用していかなる損害が発生したとしても、私は一切の責任を負いかねますのでご了承ください**</font>  
　  
　  
## その他（補足など）
### アプリについて
- **Loudness Checker Ver. 2.2.1**
- Copyright (c) 2020 Ippee
- このアプリケーションはMIT Licenseのもとで公開されています
- 動作環境: 
  - Windows 10
  - FFmpeg
- 使用言語 / ライブラリ:
  - Python 3.6.4
  - Matplotlib 3.1.3
　  
### 今後について
　  
**本アプリの開発は事実上停止しています**  
　  
一通り欲しい機能が揃って、ちゃんと思った通りに動くようになったので、これはこれで完成ということにしてしまいます  
本当はFFmpegをインストールなしでも動くようにしたいとか、起動速度遅すぎィ！とかexeファイル重すぎィ！とかGUIダサすぎィ！とか、色々と思うところは確かにあります  
が、それをPythonのみで解決しようとするとなかなか骨が折れそうというのと、  
いい加減他のものも作りたかったり、新しい言語に触れてみたかったりと、他にもっとやりたいことが出来たのでそっちに専念してきます  
もっと技術力を身につけたら、さっき言ったようなことを解消したアプリを作るかもしれません  
　  
　  
## 特に参考にしたサイト
- **Documentation | FFmpeg**
  - https://ffmpeg.org/documentation.html
  - FFmpegの公式リファレンス
- **ラウドネス測定手順 | Studio Gyokimae**
  - https://pspunch.com/pd/article/measuring_loudness/
  - FFmpegでラウドネスを測れるって初めて知ったサイト
- **LUFS/LKFS…ラウドネスメーターについて復習して理解を深めよう | SOUNDEVOTEE.NET**
  - https://soundevotee.net/blog/2017/04/25/learning_about_loudness_meter/
  - ラウドネスの勉強に用いたサイトその１
- **EBU ラウドネス標準 R-128 | Steinberg.help**  
  - https://steinberg.help/wavelab_pro/v9.5/ja/wavelab/topics/wavelab_concepts/ebu_loudness_recommendation_r128__c.html
  - ラウドネスの勉強に用いたサイトその２
- **【Python GUIサンプル】Tkinterでfiledialog(ファイルダイアログ)を使ってみる | エンジニアになりたいブログ**
  - https://suzutaka-programming.com/tkinter-filedialog/
  - このサイトが無かったらGUIは作れなかった
