from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QGraphicsOpacityEffect
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer, QPoint
from PyQt6.QtGui import QPixmap


class Toast(QWidget):
    def __init__(self, parent=None, message="Successfully Added!", icon_path=None, duration=2000):
        super().__init__(parent)

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)

        self.duration = duration

        # 🔹 Inner container for styling
        self.container = QWidget(self)
        self.container.setObjectName("toastContainer")
        container_layout = QHBoxLayout(self.container)
        container_layout.setContentsMargins(15, 10, 15, 10)
        container_layout.setSpacing(10)

        # 🔹 Optional icon
        if icon_path:
            icon_label = QLabel()
            pixmap = QPixmap(icon_path)
            icon_label.setPixmap(pixmap.scaled(24, 24, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            container_layout.addWidget(icon_label)

        # 🔹 Text label
        text_label = QLabel(message)
        text_label.setStyleSheet("""
            QLabel {
                color: black;
                font: 63 13pt "Montserrat SemiBold";
            }
        """)
        container_layout.addWidget(text_label)

        # 🔹 Outer layout to hold the container in center
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.container)

        # 🔹 Style only the inner container
        self.setStyleSheet("""
            QWidget#toastContainer {
                background-color: #C4C4C4;
                border-radius: 15px;
                border-bottom: 1px solid #cccccc;
                border-right: 1px solid #cccccc;
            }
        """)

        self.adjustSize()

    def show_toast(self):
        # Inside show_toast()
        if self.parent():
            content_widget = self.parent().findChild(QWidget,"MainContent")  # Or use stackedWidget.parent() if it's the content container
            if content_widget:
                content_pos = content_widget.mapToGlobal(QPoint(0, 0))
                content_width = content_widget.width()

                x = content_pos.x() + (content_width - self.width()) // 2
                y = content_pos.y() + 15

                self.move(x, y - self.height())

        self.show()
        self.raise_()

        self.slide_animation = QPropertyAnimation(self, b"pos")
        self.slide_animation.setDuration(800)
        self.slide_animation.setStartValue(self.pos())
        self.slide_animation.setEndValue(QPoint(x, y))
        self.slide_animation.setEasingCurve(QEasingCurve.Type.OutBack)
        self.slide_animation.start()

        QTimer.singleShot(self.duration + 300, lambda: self.fade_out())

    def fade_out(self):
        self.fade_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_animation.setDuration(600)
        self.fade_animation.setStartValue(1.0)
        self.fade_animation.setEndValue(0.0)
        self.fade_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.fade_animation.finished.connect(self.deleteLater)
        self.fade_animation.start()
