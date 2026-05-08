import sys
import os
from PyQt5.QtWidgets import QMainWindow, QLabel, QAction, QApplication, QFileDialog
from PyQt5.QtGui import QPixmap, QImage, QIcon
from PyQt5.QtCore import Qt
import cv2
from filters import grayscale, blur, edge_detect

class ImageFilterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("图片滤镜应用")
        self.setGeometry(100, 100, 800, 600)

        # ---------- 处理资源路径 ----------
        if getattr(sys, 'frozen', False):
            # exe 打包后
            base_path = sys._MEIPASS
        else:
            # 脚本运行
            base_path = os.path.dirname(__file__)
        icon_path = os.path.join(base_path, "resources", "icon.ico")
        self.setWindowIcon(QIcon(icon_path))

        # ---------- 中心显示 QLabel ----------
        self.image_label = QLabel("图片预览", self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.image_label)

        # ---------- 菜单栏 ----------
        menubar = self.menuBar()

        # 文件菜单
        file_menu = menubar.addMenu("文件")
        open_action = QAction("打开图片", self)
        save_action = QAction("保存图片", self)
        # 撤销放文件菜单，并设置 Ctrl+Z 快捷键和提示
        undo_action = QAction("撤销", self)
        undo_action.setShortcut("Ctrl+Z")
        undo_action.setStatusTip("Ctrl + Z")
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addAction(undo_action)

        # 滤镜菜单
        filter_menu = menubar.addMenu("滤镜")
        gray_action = QAction("灰度滤镜", self)
        blur_action = QAction("模糊滤镜", self)
        edge_action = QAction("边缘检测", self)
        filter_menu.addAction(gray_action)
        filter_menu.addAction(blur_action)
        filter_menu.addAction(edge_action)

        # ---------- 图片变量 ----------
        self.original_img = None
        self.cv_img = None
        self.filters_to_apply = []

        # ---------- 信号连接 ----------
        open_action.triggered.connect(self.open_image)
        save_action.triggered.connect(self.save_image)
        undo_action.triggered.connect(self.undo_filter)
        gray_action.triggered.connect(lambda: self.apply_filter("gray"))
        blur_action.triggered.connect(lambda: self.apply_filter("blur"))
        edge_action.triggered.connect(lambda: self.apply_filter("edge"))

    # ---------- 打开图片 ----------
    def open_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "选择图片", "", "Images (*.png *.jpg *.bmp)")
        if path:
            self.original_img = cv2.imread(path)
            self.cv_img = self.original_img.copy()
            self.filters_to_apply = []
            self.show_image(self.cv_img)

    # ---------- 显示图片 ----------
    def show_image(self, cv_img):
        if cv_img is None:
            return
        if len(cv_img.shape) == 2:
            rgb_img = cv2.cvtColor(cv_img, cv2.COLOR_GRAY2RGB)
        else:
            rgb_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)

        h, w, ch = rgb_img.shape
        bytes_per_line = ch * w
        qt_img = QImage(rgb_img.data, w, h, bytes_per_line, QImage.Format_RGB888)

        pixmap = QPixmap.fromImage(qt_img)
        pixmap = pixmap.scaled(
            self.image_label.width(),
            self.image_label.height(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)

    # ---------- 应用滤镜 ----------
    def apply_filter(self, filter_type):
        if self.original_img is None:
            return
        self.filters_to_apply.append(filter_type)
        self.cv_img = self.original_img.copy()
        for f in self.filters_to_apply:
            if f == "gray":
                self.cv_img = grayscale(self.cv_img)
            elif f == "blur":
                self.cv_img = blur(self.cv_img)
            elif f == "edge":
                self.cv_img = edge_detect(self.cv_img)
        self.show_image(self.cv_img)

    # ---------- 撤销滤镜 ----------
    def undo_filter(self):
        if self.filters_to_apply:
            self.filters_to_apply.pop()
            self.cv_img = self.original_img.copy()
            for f in self.filters_to_apply:
                if f == "gray":
                    self.cv_img = grayscale(self.cv_img)
                elif f == "blur":
                    self.cv_img = blur(self.cv_img)
                elif f == "edge":
                    self.cv_img = edge_detect(self.cv_img)
            self.show_image(self.cv_img)

    # ---------- 保存图片 ----------
    def save_image(self):
        if self.cv_img is None:
            return
        save_path, _ = QFileDialog.getSaveFileName(self, "保存图片", "", "Images (*.png *.jpg *.bmp)")
        if save_path:
            cv2.imwrite(save_path, self.cv_img)

# ---------- 启动程序 ----------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageFilterApp()
    window.show()
    sys.exit(app.exec_())