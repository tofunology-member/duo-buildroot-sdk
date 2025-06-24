import cv2
import time

# =============================================
# RTSPストリームから画像を取得して保存するサンプル
# =============================================
# 必要なもの:
#   - OpenCV (cv2)
#   - GStreamer (OpenCVがGStreamer対応でビルドされていること)
#
# このスクリプトは、ローカルのRTSPサーバー(127.0.0.1)からH264映像を受信し、
# 画像ファイルとして保存します。
#
# GStreamerパイプラインの各要素:
#   rtspsrc         : RTSPストリームの受信元
#   protocols=tcp   : TCPで受信（UDPにしたい場合はudpに変更）
#   latency=0       : レイテンシ最小化
#   drop-on-latency : レイテンシが高い場合はフレームをドロップ
#   !               : 前の要素の出力を次の要素の入力に接続（GStreamerのパイプ記号）
#   rtph264depay    : RTPパケットからH264データを抽出
#   h264parse       : H264データをパース
#   avdec_h264      : H264デコード
#   videoconvert    : OpenCVで扱える形式に変換
#   appsink         : OpenCVでフレームを受け取る
#   sync=false      : 同期を無効化（高速化）
#   max-buffers=1   : バッファ数を1に制限（低遅延化）
#   drop=true       : バッファが溜まったら古いフレームをドロップ

# --- GStreamerパイプライン文字列 ---
gst_str = (
    "rtspsrc location=rtsp://127.0.0.1/h264 "  # RTSPサーバーのURL
    "protocols=tcp "  # TCPで受信
    "latency=0 "  # レイテンシ最小化
    "drop-on-latency=true "  # レイテンシが高い場合はフレームをドロップ
    "! rtph264depay "  # RTPパケットからH264データを抽出
    "! h264parse "  # H264データをパース
    "! avdec_h264 "  # H264デコード
    "! videoconvert "  # OpenCVで扱える形式に変換
    "! appsink "  # OpenCVでフレームを受け取る
    "sync=false "  # 同期を無効化
    "max-buffers=1 "  # バッファ数を1に制限
    "drop=true"  # バッファが溜まったら古いフレームをドロップ
)

print("RTSPストリームに接続中...")
start_time = time.time()

# --- GStreamerパイプラインでVideoCaptureを開く ---
# cv2.CAP_GSTREAMER を指定することで、OpenCVがGStreamerパイプラインを利用
cap = cv2.VideoCapture(gst_str, cv2.CAP_GSTREAMER)

# --- 接続チェック ---
if not cap.isOpened():
    print("GStreamerパイプラインでRTSPストリームに接続できません")
    exit(1)

print(f"接続完了: {time.time() - start_time:.2f}秒")

# --- ウォームアップ ---
# 最初の数フレームは捨てて、デコーダやバッファを安定させる
for _ in range(3):
    ret, _ = cap.read()
    if not ret:
        print("ウォームアップ中にフレーム取得失敗")
        break

# --- 画像取得と保存 ---
# 2回フレーム取得を試みて、それぞれ保存
for i in range(2):
    ret, frame = cap.read()
    if ret and frame is not None:
        # フレームをJPEG画像として保存
        filename = f"snapshot_fast{i}.jpg"
        cv2.imwrite(filename, frame)
        print(
            f"画像を保存しました：{filename} (総時間: {time.time() - start_time:.2f}秒)"
        )
    else:
        print(f"{i}回目: フレームの取得に失敗しました")

# --- リソース解放 ---
cap.release()
