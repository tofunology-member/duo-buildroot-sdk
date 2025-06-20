# 特徴
- riscv向けlp64dに則ったライブラリ群サポート
- tesseractのサポート
- opencv3のpythonサポート

# 最初にやるべきこと
```bash
wget https://sophon-file.sophon.cn/sophon-prod-s3/drive/23/03/07/16/host-tools.tar.gz
tar -xvzf host-tools.tar.gz
rm host-tools.tar.gz
cp host-tools/gcc/riscv64-linux-musl-x86_64/sysroot/lib64/lp64d/* device/milkv-duo256m-sd/overlay/usr/lib
```
このコマンド実行後、`./build.sh lunch`して`4`を選択すればOK

# ネットワーク上のデバイスを探す
`enx00e04cf8f720`の部分は`ifconfig`で確認（例：`en0`）
```
sudo arp-scan -I enx00e04cf8f720 -l
```

# tesseractのテスト
## 1. ホストコンピュータで確認
まずはこのディレクトリで出力をチェック。
```bash
tesseract color.png output --psm 11 -l eng
cat output.txt
rm output.txt
```
出力例
```bash
Estimating resolution as 276
tofunology

tofunology

H / 02-03

BEQOXHRSh APUFRe

Super Deluxe Company's Exclusive Automatic Hanko Machine

ee

ws

<<.

\F

2

y

```

## 2. milkvに画像をコピー
```bash
# 192.168.40.243はmilkvのIPアドレス。適宜変更する
# -Oが不要な場合ある
sudo scp -O color.png root@192.168.40.243:/root/
```

## 3. milkvで確認
```bash
tesseract color.png output --psm 11 -l eng
cat output.txt
rm output.txt
```
1.で確認した出力みたいな感じならOK

# OpenCVのテスト
## 1. このディレクトリの`color.png`をmilkvにコピー

```bash
# 192.168.40.243はmilkvのIPアドレス。適宜変更する
# -Oが不要な場合ある
sudo scp -O color.png root@192.168.40.243:/root/
```

## 2. pythonのプログラムをmilkv上で作成
```bash
cd ~
# viコマンドでなくても、nanoでもなんでもOK
vi conv2gray.py
```

プログラムは以下の通り
```python
# OpenCVライブラリを使う準備
import cv2
# sysライブラリを使う準備
import sys

# テスト画像の読み込み
img = cv2.imread("color.png")

# テスト画面が変数imgに入っていない時は、エラーを表示してプログラムを終了
if img is None:
    print("テスト画像が正しく読み込めませんでした")
    sys.exit()

# テスト画像を白黒画像に変換
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 結果画像をパソコンに保存
cv2.imwrite("gray.png",gray)

```

## 3. 実行
```bash
python conv2gray.py
```

## 4. 出力ファイルをmilkvからホストコンピュータにコピーしてチェック
```bash
# 192.168.40.202はホストコンピュータのIPアドレス。適宜変更する
# /home/gitefu/Downloads部分はホストコンピュータに合わせる
# -Oが必要な場合ある
scp gray.png gitefu@192.168.40.202:/home/gitefu/Downloads
```

グレースケールになってたら成功