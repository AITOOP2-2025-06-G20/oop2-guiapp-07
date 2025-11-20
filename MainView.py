import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QFrame, QSizePolicy
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QPixmap


class MainView(QMainWindow):
    """
    GUIアプリケーションのメインウィンドウクラス。
    ウィジェットの配置とレイアウトを定義します。
    """

    # ロジック側（Controller）からアクセスするためのオブジェクト名
    WIDGET_NAMES = {
        "camera_preview": "cameraPreviewLabel",
        "result_image": "resultImageLabel",
        "start_capture_button": "startCaptureButton",
        "stop_capture_button": "stopCaptureButton",
        "process_button": "processButton",
        "save_button": "saveButton",
        "status_label": "statusLabel"
    }

    def __init__(self):
        super().__init__()
        self.setWindowTitle("画像タイリング合成アプリケーション (PySide6)")
        
        # 写真のサイズ感を再現するため、初期サイズを大きめに設定
        self.setGeometry(100, 100, 1000, 700) 

        # メインウィジェットとレイアウトの設定
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # UIの構築
        self._setup_ui(main_layout)

    def _setup_ui(self, main_layout: QHBoxLayout):
        """
        ウィジェットの生成、命名、およびレイアウトへの配置を行います。
        """

        # --- 1. 左側エリア: カメラプレビューと操作ボタン (写真のIDEのコードエリア相当) ---

        left_side_widget = QWidget()
        left_layout = QVBoxLayout(left_side_widget)
        left_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # 1-1. カメラプレビュー (QLabel)
        # Cさん (カメラ担当) からのフィードを表示
        self.camera_preview_label = QLabel("■ カメラプレビュー (Cさんの非同期スレッドが描画)")
        self.camera_preview_label.setObjectName(self.WIDGET_NAMES["camera_preview"])
        self.camera_preview_label.setFixedSize(640, 480) # 標準的なカメラ解像度に合わせて固定サイズを設定
        self.camera_preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.camera_preview_label.setStyleSheet("border: 2px solid #333; background-color: #DDD;")
        left_layout.addWidget(self.camera_preview_label)

        # 1-2. 操作ボタンエリア (QGridLayout)
        button_group = QWidget()
        button_layout = QGridLayout(button_group)

        # カメラ操作ボタン (Cさんロジックとの連携用)
        self.start_capture_button = QPushButton("🔴 カメラ開始")
        self.start_capture_button.setObjectName(self.WIDGET_NAMES["start_capture_button"])
        button_layout.addWidget(self.start_capture_button, 0, 0)

        self.stop_capture_button = QPushButton("■ キャプチャ停止＆画像確定")
        self.stop_capture_button.setObjectName(self.WIDGET_NAMES["stop_capture_button"])
        button_layout.addWidget(self.stop_capture_button, 0, 1)

        # 処理実行ボタン (Bさんロジックとの連携用)
        self.process_button = QPushButton("▶ 画像処理実行 (タイリング合成)")
        self.process_button.setObjectName(self.WIDGET_NAMES["process_button"])
        self.process_button.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.process_button.setStyleSheet("background-color: #aaddff;")
        button_layout.addWidget(self.process_button, 1, 0, 1, 2) # 1行目で2列を結合

        left_layout.addWidget(button_group)

        # ステータス表示
        self.status_label = QLabel("待機中...")
        self.status_label.setObjectName(self.WIDGET_NAMES["status_label"])
        self.status_label.setFont(QFont("Arial", 10))
        left_layout.addWidget(self.status_label)

        main_layout.addWidget(left_side_widget)

        # --- セパレータ ---

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.VLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(separator)

        # --- 2. 右側エリア: 結果画像表示と保存ボタン (写真のチャット/ターミナルエリア相当) ---

        right_side_widget = QWidget()
        right_layout = QVBoxLayout(right_side_widget)
        right_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # 2-1. 結果画像表示 (QLabel)
        # Bさん (ロジック担当) の処理結果を表示
        self.result_image_label = QLabel("■ 結果画像 (1280x640相当)")
        self.result_image_label.setObjectName(self.WIDGET_NAMES["result_image"])
        self.result_image_label.setFixedSize(640, 320) # google.pngの縦横比1280:640 (2:1) を維持し、画面に収まるよう半分のサイズで表示
        self.result_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_image_label.setStyleSheet("border: 2px solid #333; background-color: #EEE;")
        right_layout.addWidget(self.result_image_label)

        # 2-2. 保存ボタン
        self.save_button = QPushButton("💾 結果画像をファイルに保存")
        self.save_button.setObjectName(self.WIDGET_NAMES["save_button"])
        self.save_button.setStyleSheet("background-color: #ccffcc;")
        right_layout.addWidget(self.save_button)

        right_layout.addStretch(1) # 下部の余白を埋める
        main_layout.addWidget(right_side_widget)


if __name__ == '__main__':
    # 動作確認のためのプレビュー実行
    app = QApplication(sys.argv)
    window = MainView()
    
    # 仮の表示内容 (起動確認用)
    window.camera_preview_label.setText("カメラが開始されるとここに映像が表示されます")
    window.result_image_label.setText("画像処理実行後にここに結果が表示されます")

    window.show()
    sys.exit(app.exec())