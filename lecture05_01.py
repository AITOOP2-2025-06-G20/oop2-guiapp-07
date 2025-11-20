import numpy as np
import cv2
from my_module.K24091.lecture05_camera_image_capture import MyVideoCapture

def lecture05_01():
    # カメラキャプチャ実行
    app = MyVideoCapture()
    app.run()
    
    # 画像をローカル変数に保存
    google_img : np.ndarray = cv2.imread('images/google.png')
    capture_img : np.ndarray = app.get_img()
    
    # 画像の読み込みチェック
    if google_img is None:
        print("エラー: 'images/google.png'を読み込めませんでした。ファイルパスを確認してください。")
        return
    if capture_img is None:
        print("エラー: カメラキャプチャ画像が取得できませんでした。")
        return

    # 画像のサイズ情報を取得
    g_hight, g_width, g_channel = google_img.shape
    c_hight, c_width, c_channel = capture_img.shape
    print(f"Google画像サイズ (H, W, C): {google_img.shape}")
    print(f"キャプチャ画像サイズ (H, W, C): {capture_img.shape}")

    # 白色 (B=255, G=255, R=255) の条件マスクを作成
    # OpenCVはBGR形式で画像を読み込むため、(B, G, R) == (255, 255, 255)で判定
    is_white = np.all(google_img == 255, axis=-1)

    # 置き換え用のキャプチャ画像のタイルパターンを作成
    
    # 1. Google画像と同じ高さ/幅のインデックス配列を作成
    # 0からg_width-1までのx座標、0からg_hight-1までのy座標
    y_indices, x_indices = np.ogrid[0:g_hight, 0:g_width]

    # 2. キャプチャ画像上で繰り返すためのモジュロ演算
    # c_width, c_hightを法として、x, y座標の剰余を求める
    tiled_x = x_indices % c_width
    tiled_y = y_indices % c_hight
    
    # 3. タイル状に敷き詰められたキャプチャ画像データを作成
    # google_imgのサイズに合うように、キャプチャ画像からピクセルを選択
    tiled_capture_img = capture_img[tiled_y, tiled_x]

    # 4. マスクを使用して、白色の部分のみをタイル画像で置き換え
    # is_white (True/Falseの2D配列)を3チャンネルに拡張
    is_white_3d = np.stack([is_white] * 3, axis=-1)
    
    # np.where(条件, Trueの場合の値, Falseの場合の値) を使用
    # 条件: is_white_3dがTrue (元のピクセルが白)
    # Trueの場合: tiled_capture_img の対応するピクセルを使用
    # Falseの場合: google_img (元のピクセル) をそのまま使用
    google_img = np.where(is_white_3d, tiled_capture_img, google_img)

    # 書き込み処理
    output_filename = 'lecture05_01_K24091.png'
    cv2.imwrite(output_filename, google_img)
    
    print(f"処理完了: 画像を'{output_filename}'として保存しました。")
    print("カメラ画像が並べられ、途中で切れていることを確認してください。")


if __name__ == '__main__':
    lecture05_01()