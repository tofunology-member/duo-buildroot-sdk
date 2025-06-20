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