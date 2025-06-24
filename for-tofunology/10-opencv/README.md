# 前準備：ネットワーク上のデバイスを探す
`enx00e04cf8f720`の部分は`ifconfig`で確認（例：`en0`）
```
sudo arp-scan -I enx00e04cf8f720 -l
```

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