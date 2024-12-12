import sys
import os
import logging
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                               QTextEdit, QFileDialog, QLabel, QSystemTrayIcon, QMenu, QMessageBox, QInputDialog)
from PySide6.QtGui import QIcon, QAction, QClipboard
from PySide6.QtCore import Qt
from languages import translations  # Import the translations dictionary
import win32com.client
from urllib.parse import unquote
from version import __version__, __release_date__

# Настройка логирования
log_dir = os.path.expanduser("~")  # Домашняя директория пользователя
log_file = os.path.join(log_dir, "markdown_explorer.log")

# Настройка логирования
logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logging.info("Logging initialized. Log file: %s", log_file)

EXCLUDE_DIRS = {
    ".git", ".venv", "node_modules", ".idea", "__pycache__", ".mypy_cache", ".pytest_cache",
    ".gradle", "target", "build", "dist", "venv", ".tox", ".DS_Store", "env", ".svn",
    ".hg", ".bzr", "CVS", "Thumbs.db", ".settings", ".metadata", ".history",
    ".vscode", ".cache", "logs", "tmp", "temp", "debug", "__MACOSX"
}

EXCLUDE_FILES = {
    ".DS_Store", "Thumbs.db", "desktop.ini", "ehthumbs.db", "Icon\r",
    ".gitattributes", ".editorconfig", "npm-debug.log", "yarn-error.log"
}



def generate_markdown(folder_path):
    logging.info(f"Generating markdown for folder: {folder_path}")
    lines = []

    def recurse(current_path, indent=""):
        try:
            entries = sorted(os.listdir(current_path))
            entries = [e for e in entries if e not in EXCLUDE_DIRS and e not in EXCLUDE_FILES]
            total_entries = len(entries)
            for index, entry in enumerate(entries):
                full_path = os.path.join(current_path, entry)
                is_last = index == total_entries - 1
                connector = "└── " if is_last else "├── "
                if os.path.isdir(full_path):
                    lines.append(f"{indent}{connector}{entry}/")
                    new_indent = indent + ("    " if is_last else "│   ")
                    recurse(full_path, new_indent)
                else:
                    lines.append(f"{indent}{connector}{entry}")
        except Exception as e:
            logging.error(f"Error during folder recursion: {e}")

    folder_name = os.path.basename(folder_path.rstrip("/\\"))
    lines.append(f"Directory: {folder_path}")
    lines.append(f"{folder_name}/")
    recurse(folder_path)
    logging.info("Markdown generation complete.")
    return "\n".join(lines)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.current_language = "en"  # Default language
        self.init_ui()  # Инициализация UI
        self.init_tray()  # Инициализация системного трея
        logging.info("Application started.")

    def init_ui(self):
        self.setWindowTitle(self.tr("Markdown Explorer"))
        self.setStyleSheet(self.get_dark_style())
        self.setWindowIcon(QIcon("resources/icon.ico"))

        main_layout = QVBoxLayout()

        # Language Switcher
        lang_switcher = QHBoxLayout()
        self.lang_label = QLabel(self.tr("Language:"))
        lang_switcher.addWidget(self.lang_label)

        self.lang_buttons = {
            "en": QPushButton("English"),
            "ru": QPushButton("Русский"),
            "kz": QPushButton("Қазақша"),
        }
        for lang, button in self.lang_buttons.items():
            button.clicked.connect(lambda checked, l=lang: self.change_language(l))
            lang_switcher.addWidget(button)

        main_layout.addLayout(lang_switcher)

        # Top Layout
        top_layout = QHBoxLayout()

        self.label = QLabel(self.tr(translations[self.current_language]["select_folder"]))
        top_layout.addWidget(self.label)

        self.btn_choose = QPushButton(self.tr(translations[self.current_language]["select_folder"]))
        self.btn_choose.setStyleSheet("""
            QPushButton {
                background-color: #f0b90b; 
                color: #000; 
                font-weight: bold; 
                border-radius: 5px;
                padding: 8px 12px;
            }
            QPushButton:hover {
                background-color: #dab308;
            }
        """)
        self.btn_choose.clicked.connect(self.choose_folder)
        top_layout.addWidget(self.btn_choose)

        self.btn_copy = QPushButton(self.tr(translations[self.current_language]["copy_to_clipboard"]))
        self.btn_copy.clicked.connect(self.copy_to_clipboard)
        top_layout.addWidget(self.btn_copy)

        main_layout.addLayout(top_layout)

        # Text Edit
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setStyleSheet("""
            background-color: #1e1e1e; 
            color: #c9c9c9; 
            font-family: Consolas; 
            font-size: 14px;
        """)
        main_layout.addWidget(self.text_edit)

        self.setLayout(main_layout)
        self.resize(800, 600)

    def init_tray(self):
        """Инициализация системного трея."""
        if QSystemTrayIcon.isSystemTrayAvailable():
            self.tray_icon = QSystemTrayIcon(self)
            self.tray_icon.setIcon(QIcon("resources/icon.ico"))
            self.tray_icon.setToolTip(self.tr(translations[self.current_language]["tray_tooltip"]))

            tray_menu = QMenu(self)

            # Добавляем пункт "Выбрать открытую папку"
            select_folder_action = QAction(self.tr(translations[self.current_language]["select_opened_folder"]), self)
            select_folder_action.triggered.connect(self.select_opened_folder)
            tray_menu.addAction(select_folder_action)
            logging.info("Select opened folder action added to tray menu.")

            # Пункт "Показать окно"
            show_action = QAction(self.tr(translations[self.current_language]["show_window"]), self)
            show_action.triggered.connect(self.show_window)
            tray_menu.addAction(show_action)
            logging.info("Show action added to tray menu.")

            # Пункт "О программе"
            about_action = QAction("About", self)
            about_action.triggered.connect(self.about_app)
            tray_menu.addAction(about_action)
            logging.info("About action added to tray menu.")

            # Пункт "Выход"
            quit_action = QAction(self.tr(translations[self.current_language]["exit"]), self)
            quit_action.triggered.connect(self.quit_app)
            tray_menu.addAction(quit_action)
            logging.info("Quit action added to tray menu.")

            self.tray_icon.setContextMenu(tray_menu)
            self.tray_icon.activated.connect(self.on_tray_icon_activated)
            self.tray_icon.show()
        else:
            logging.warning("System tray is not available.")
            QMessageBox.warning(self, "Error", "System tray is not available.")

    def on_tray_icon_activated(self, reason):
        """Обработчик активации иконки в трее."""
        logging.info(f"Tray icon activated: {reason}")
        if reason == QSystemTrayIcon.Trigger:  # Одинарный клик ЛКМ
            # Показать/скрыть окно
            if self.isVisible():
                self.hide()
            else:
                self.showNormal()
                self.activateWindow()
        elif reason == QSystemTrayIcon.Context:  # Клик ПКМ
            # Контекстное меню отображается автоматически
            pass
        elif reason == QSystemTrayIcon.DoubleClick:  # Двойной клик (может не работать в Windows 11)
            # Можно продублировать действия из Trigger
            if self.isVisible():
                self.hide()
            else:
                self.showNormal()
                self.activateWindow()

    def about_app(self):
        logging.info("About dialog shown.")
        QMessageBox.information(
            self,
            "About",
            f"Markdown Explorer\n\nVersion: {__version__}\nRelease Date: {__release_date__}\nDeveloped by: Bekzat Zhaksybayev",
        )

    def tr(self, text):
        """Translate text based on current language."""
        return text

    def change_language(self, language):
        logging.info(f"Changing language to: {language}")
        self.current_language = language
        self.update_ui()

    def update_ui(self):
        """Update UI elements with the selected language."""
        logging.info("Updating UI.")
        self.setWindowTitle(self.tr(translations[self.current_language]["tray_tooltip"]))
        self.lang_label.setText(self.tr("Language:"))
        self.label.setText(self.tr(translations[self.current_language]["select_folder"]))
        self.btn_choose.setText(self.tr(translations[self.current_language]["select_folder"]))
        self.btn_copy.setText(self.tr(translations[self.current_language]["copy_to_clipboard"]))
        if QSystemTrayIcon.isSystemTrayAvailable():
            self.tray_icon.setToolTip(self.tr(translations[self.current_language]["tray_tooltip"]))

    def choose_folder(self):
        logging.info("Choosing folder.")
        folder = QFileDialog.getExistingDirectory(self, self.tr(translations[self.current_language]["select_folder"]),
                                                  "")
        if folder:
            markdown = generate_markdown(folder)
            self.text_edit.setPlainText(markdown)
            self.label.setText(
                self.tr(translations[self.current_language]["directory_structure"]).format(folder=folder))
        logging.info(f"Selected folder: {folder}")

    def copy_to_clipboard(self):
        logging.info("Copying to clipboard.")
        text = self.text_edit.toPlainText()
        cb = QApplication.clipboard()
        cb.setText(text, QClipboard.Clipboard)
        QMessageBox.information(self, self.tr(translations[self.current_language]["copy_to_clipboard"]),
                                self.tr(translations[self.current_language]["copied"]))
        logging.info("Copied to clipboard.")

    def quit_app(self):
        logging.info("Quitting application.")
        if QSystemTrayIcon.isSystemTrayAvailable():
            self.tray_icon.hide()
        QApplication.quit()

    def get_dark_style(self):
        return """
        QWidget {
            background-color: #121212;
        }
        QLabel {
            color: #f0f0f0;
        }
        QTextEdit {
            background-color: #1e1e1e;
            color: #c9c9c9;
        }
        """

    def closeEvent(self, event):
        logging.info("Close event triggered.")
        event.ignore()
        self.hide()
        if QSystemTrayIcon.isSystemTrayAvailable():
            self.tray_icon.showMessage(
                self.tr(translations[self.current_language]["tray_tooltip"]),
                self.tr(translations[self.current_language]["show_window"]),
                QSystemTrayIcon.Information,
                2000,
            )

    def show_window(self):
        logging.info("Showing window.")
        self.showNormal()
        self.activateWindow()

    def select_opened_folder(self):
        """Обработчик выбора открытой папки."""
        opened_folders = self.get_opened_folders()

        if not opened_folders:
            QMessageBox.warning(
                self,
                self.tr(translations[self.current_language]["select_opened_folder"]),
                self.tr(translations[self.current_language]["no_opened_folders"])
            )
            return

        if len(opened_folders) == 1:
            # Если только одна папка открыта, выбираем её автоматически
            selected_folder = opened_folders[0]
        else:
            # Показываем пользователю выбор из найденных папок
            selected_folder, ok = QInputDialog.getItem(
                self,
                self.tr(translations[self.current_language]["select_opened_folder"]),
                self.tr("Choose from opened folders:"),
                opened_folders,
                0,
                False
            )
            if not ok or not selected_folder:
                logging.info("User canceled folder selection.")
                return

        # Генерируем Markdown для выбранной папки
        markdown = generate_markdown(selected_folder)

        # Отправляем уведомление с результатом
        self.tray_icon.showMessage(
            self.tr(translations[self.current_language]["tray_tooltip"]),
            self.tr(f"Result copied: {markdown}"),
            QSystemTrayIcon.Information,
            2000
        )

        # Копируем путь к выбранной папке в буфер обмена
        clipboard = QApplication.clipboard()
        clipboard.setText(markdown, QClipboard.Clipboard)

        # Логируем и показываем результат в логах
        logging.info(f"Markdown for {selected_folder}:\n{markdown}")
        logging.info("Selected folder copied to clipboard.")

    def get_opened_folders(self):
        """Получение списка открытых папок в проводнике с использованием pywin32."""
        folders = []
        try:
            shell = win32com.client.Dispatch("Shell.Application")
            windows = shell.Windows()

            for window in windows:
                if window.Name == "File Explorer" or "Проводник" in window.Name:
                    folder_path = window.LocationURL
                    if folder_path:
                        # Декодируем URL в путь
                        folder_path = unquote(folder_path.replace("file:///", "").replace("/", "\\"))
                        if folder_path and folder_path not in folders:
                            folders.append(folder_path)

        except Exception as e:
            logging.error(f"Ошибка получения открытых папок: {e}")

        return folders


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())