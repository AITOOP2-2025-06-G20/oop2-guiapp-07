import cv2

class MyVideoCapture:
    def __init__(self, video_source=0):
        # カメラまたは動画ファイルを開く
        self.cap = cv2.VideoCapture(video_source)

        if not self.cap.isOpened():
            raise ValueError("Unable to open video source", video_source)

    def capture_single_frame(self):
        """
        GUI のタイマーイベントから呼ばれる前提。
        1フレームだけ読み込んで返す。
        """
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                return frame
        return None  # 取得失敗時

    # ======== 画像処理ロジック（ここは自由に追加） ========

    def to_gray(self, frame):
        """グレースケール変換"""
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    def blur(self, frame, k=5):
        """平滑化（ぼかし）"""
        return cv2.GaussianBlur(frame, (k, k), 0)

    def edge(self, frame, th1=100, th2=200):
        """エッジ検出"""
        return cv2.Canny(frame, th1, th2)

    def release(self):
        """リソース解放"""
        if self.cap.isOpened():
            self.cap.release()
