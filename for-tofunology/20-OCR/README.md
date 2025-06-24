# 前準備：ネットワーク上のデバイスを探す
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