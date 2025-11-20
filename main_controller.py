from PySide6.QtCore import QTimer
import cv2  # 追加

class MainController:
    def __init__(self, model, view):
        self.model = model  # CameraProcessor（Model）
        self.view = view    # MainView（View）

        # --- ボタンとモデル処理の接続 ---
        self.view.start_button.clicked.connect(self.start_camera)
        self.view.stop_button.clicked.connect(self.stop_camera)
        self.view.process_button.clicked.connect(self.run_processing)
        self.view.save_button.clicked.connect(self.save_result)

        # --- QTimer：一定間隔でフレームを更新 ---
        self.timer = QTimer()
        self.timer.setInterval(30)  # 30ms間隔（≈33fps）
        self.timer.timeout.connect(self.update_frame)

    # --------------------------------------------------
    # カメラ開始
    # --------------------------------------------------
    def start_camera(self):
        self.model.open_camera()
        self.timer.start()
        self.view.show_status("Camera started")

    # --------------------------------------------------
    # カメラ停止
    # --------------------------------------------------
    def stop_camera(self):
        self.timer.stop()
        self.model.close_camera()
        self.view.show_status("Camera stopped")

    # --------------------------------------------------
    # QTimerで呼ばれる毎フレーム更新
    # --------------------------------------------------
    def update_frame(self):
        if not self.model.cap.isOpened():
            return
        
        ret, frame = self.model.cap.read()
        if not ret:
            self.view.show_status("カメラフレーム取得失敗")
            return

        # ターゲットマーク描画
        rows, cols, _ = frame.shape
        center = (cols // 2, rows // 2)
        frame = cv2.circle(frame, center, 30, (0, 0, 255), 3)
        frame = cv2.circle(frame, center, 60, (0, 0, 255), 3)
        frame = cv2.line(frame, (center[0], center[1] - 80), (center[0], center[1] + 80), (0, 0, 255), 3)
        frame = cv2.line(frame, (center[0] - 80, center[1]), (center[0] + 80, center[1]), (0, 0, 255), 3)
        frame = cv2.flip(frame, 1)

        self.model.captured_img = frame  # Model の captured_img に保存
        qimg = self.view.to_qimage(frame)
        self.view.update_image(qimg)

    # --------------------------------------------------
    # タイル置換処理（GPU処理）
    # --------------------------------------------------
    def run_processing(self):
        if self.model.google_img is None or self.model.capture_img is None:
            self.view.show_status("画像が揃っていません")
            return

        self.model.result_img = self.model.tile_replace_gpu(
            self.model.google_img,
            self.model.capture_img
        )
        qimg = self.view.to_qimage(self.model.result_img)
        self.view.update_image(qimg)
        self.view.show_status("処理完了")

    # --------------------------------------------------
    # 結果画像の保存
    # --------------------------------------------------
    def save_result(self):
        if self.model.result_img is None:
            self.view.show_status("保存する画像がありません")
            return

        self.model.save_image("output.png")
        self.view.show_status("Saved: output.png")
