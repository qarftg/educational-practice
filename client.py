import sys
import requests
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QPushButton, QListWidget, QLineEdit, QLabel,
                             QMessageBox, QHBoxLayout)
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt

BASE_URL = 'http://localhost:5000'


class StyledButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px;
                font-size: 14px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)


class UserManagerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('User Manager')
        self.setGeometry(100, 100, 500, 500)

        # Основные настройки стиля
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 14px;
            }
            QListWidget {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 14px;
            }
        """)

        self.init_ui()

    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        # Заголовок
        title = QLabel("Управление пользователями")
        title.setFont(QFont('Arial', 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(title)

        # Форма добавления
        self.create_form()

        # Список пользователей
        self.users_list = QListWidget()
        self.users_list.setStyleSheet("""
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #eee;
            }
        """)
        self.main_layout.addWidget(self.users_list)

        # Статус
        self.status_label = QLabel("Готово")
        self.status_label.setAlignment(Qt.AlignRight)
        self.status_label.setStyleSheet("color: #666; font-size: 12px;")
        self.main_layout.addWidget(self.status_label)

        # Загружаем пользователей
        self.show_users()

    def create_form(self):
        form_layout = QVBoxLayout()

        # Поля ввода
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Введите имя пользователя")
        form_layout.addWidget(QLabel("Имя пользователя:"))
        form_layout.addWidget(self.username_input)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Введите email")
        form_layout.addWidget(QLabel("Email:"))
        form_layout.addWidget(self.email_input)

        # Кнопки в горизонтальном layout
        btn_layout = QHBoxLayout()

        self.add_btn = StyledButton("Добавить")
        self.add_btn.clicked.connect(self.add_user)
        btn_layout.addWidget(self.add_btn)

        self.refresh_btn = StyledButton("Обновить")
        self.refresh_btn.clicked.connect(self.show_users)
        btn_layout.addWidget(self.refresh_btn)

        form_layout.addLayout(btn_layout)
        self.main_layout.addLayout(form_layout)

    def add_user(self):
        username = self.username_input.text()
        email = self.email_input.text()

        if not username or not email:
            self.show_error("Ошибка", "Все поля должны быть заполнены")
            return

        try:
            response = requests.post(
                f"{BASE_URL}/users",
                json={'username': username, 'email': email}
            )

            if response.status_code == 201:
                self.show_success("Успех", "Пользователь добавлен")
                self.username_input.clear()
                self.email_input.clear()
                self.show_users()
            else:
                self.show_error("Ошибка", response.json().get('error', 'Неизвестная ошибка'))

        except requests.exceptions.RequestException as e:
            self.show_error("Ошибка соединения", str(e))

    def show_users(self):
        try:
            response = requests.get(f"{BASE_URL}/users")
            self.users_list.clear()

            for user in response.json():
                item = f"{user['username']} <{user['email']}> (ID: {user['id']})"
                self.users_list.addItem(item)

            self.status_label.setText(f"Найдено пользователей: {self.users_list.count()}")

        except requests.exceptions.RequestException as e:
            self.show_error("Ошибка соединения", str(e))

    def show_error(self, title, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: white;
            }
            QLabel {
                font-size: 14px;
            }
        """)
        msg.exec_()

    def show_success(self, title, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: white;
            }
            QLabel {
                font-size: 14px;
            }
        """)
        msg.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Установка стиля для всего приложения
    app.setStyle('Fusion')
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(245, 245, 245))
    app.setPalette(palette)

    window = UserManagerApp()
    window.show()
    sys.exit(app.exec_())