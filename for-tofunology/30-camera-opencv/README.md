# 前準備：ネットワーク上のデバイスを探す
`enx00e04cf8f720`の部分は`ifconfig`で確認（例：`en0`）
```
sudo arp-scan -I enx00e04cf8f720 -l
```

# milkvのカメラについて
現状`/dev/`にマウントする方法がない。
唯一C++でCVITEKの独自ライブラリ（SDK）を使うことで取得できる。
とりあえず用意した方法は2つ
1. 公式が用意したRTSPサーバを立ち上げた後、pythonから接続して画像を取得（遅い）
2. C++を書く（早くできる可能性あり）
    - C++でカメラからjpeg画像を生成←作った
    - 標準入出力で画像データをC++→Pythonに送信←つくってない

# 公式が用意したRTSPサーバを立ち上げた後、pythonから接続して画像を取得

## 1. milkvにスクリプトをコピー
```bash
# 192.168.40.243はmilkvのIPアドレス。適宜変更する
# -Oが不要な場合ある
sudo scp -O get-image-from-rtsp.py launch-rtsp-server-without-stdout.sh root@192.168.40.243:/root/
```

### 2. `launch-rtsp-server-without-stdout.sh`の権限を変更
```bash
chmod 755 ./launch-rtsp-server-without-stdout.sh 
```

### 3. `launch-rtsp-server-without-stdout.sh`をバックグラウンドで実行
```bash
./launch-rtsp-server-without-stdout.sh &
```

### 4. `get-image-from-rtsp.py`を実行
```bash
python get-image-from-rtsp.py
```

### 5. 出力ファイルをmilkvからホストコンピュータにコピーしてチェック
```bash
# 192.168.40.202はホストコンピュータのIPアドレス。適宜変更する
# /home/gitefu/Downloads部分はホストコンピュータに合わせる
# -Oが必要な場合ある
scp snapshot_fast0.jpg snapshot_fast1.jpg gitefu@192.168.40.202:/home/gitefu/Downloads
```