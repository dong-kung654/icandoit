from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QVBoxLayout, QLabel, QInputDialog, QMessageBox, QDialog, QLineEdit
from PyQt6.QtCore import QMimeData
from PyQt6.QtGui import QClipboard
import json
import os
from hash_make import save_hashes_to_json
from upload import upload_file_to_github

class SimpleGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Hash Generator and Uploader")
        self.setGeometry(200, 200, 400, 400)
        
        self.init_ui()
        
    def init_ui(self):
        self.layout = QVBoxLayout()
        
        self.folder_path = None
        self.hashes_json_path = None
        self.repo_owner = ""
        self.repo_name = ""
        self.token = ""
        self.target_path = ""
        self.file_path = ""
        
        self.label = QLabel("No folder selected.", self)
        self.layout.addWidget(self.label)
        
        self.folder_button = QPushButton("Find Folder", self)
        self.folder_button.clicked.connect(self.find_folder)
        self.layout.addWidget(self.folder_button)
        
        self.hash_button = QPushButton("Generate Hashes", self)
        self.hash_button.clicked.connect(self.generate_hashes)
        self.layout.addWidget(self.hash_button)
        
        self.check_button = QPushButton("Check Hashes", self)
        self.check_button.clicked.connect(self.check_hashes)
        self.layout.addWidget(self.check_button)
        
        self.upload_button = QPushButton("Upload Files", self)
        self.upload_button.clicked.connect(self.upload_files)  # 변경된 부분
        self.layout.addWidget(self.upload_button)
        
        self.save_button = QPushButton("Save Settings", self)
        self.save_button.clicked.connect(self.save_settings)
        self.layout.addWidget(self.save_button)
        
        self.load_button = QPushButton("Load Settings", self)
        self.load_button.clicked.connect(self.load_settings)
        self.layout.addWidget(self.load_button)
        
        self.setLayout(self.layout)
        
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f8ff;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                font-size: 14px;
            }
            QPushButton {
                background-color: #ffb6c1;
                color: #ffffff;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ff69b4;
            }
            QLabel {
                font-size: 16px;
                color: #333333;
                padding: 10px;
                text-align: center;
            }
        """)
        
    def find_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.folder_path = folder
            self.label.setText(f"Selected folder: {folder}")
        
    def generate_hashes(self):
        if self.folder_path:
            self.hashes_json_path = os.path.join(self.folder_path, "file_hashes.json")
            save_hashes_to_json(self.folder_path, self.hashes_json_path)
            self.label.setText(f"Hashes saved to: {self.hashes_json_path}")
        
    def check_hashes(self):
        if self.hashes_json_path and os.path.exists(self.hashes_json_path):
            try:
                with open(self.hashes_json_path, 'r') as file:
                    data = json.load(file)
                    hashes_str = ""
                    for file_data in data:
                        hashes_str += f"File: {file_data['file_name']}\nHash: {file_data['sha256_hash']}\n\n"
                    self.show_hashes_popup(hashes_str)
            except Exception as e:
                self.label.setText(f"Error reading hashes: {e}")
        else:
            self.label.setText("No hashes file found.")
        
    def show_hashes_popup(self, hashes_str):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("File Hashes")
        msg_box.setText("Hashes for files:\n\n" + hashes_str)
        msg_box.setIcon(QMessageBox.Icon.Information)
        copy_button = msg_box.addButton("Copy to Clipboard", QMessageBox.ButtonRole.AcceptRole)
        close_button = msg_box.addButton("Close", QMessageBox.ButtonRole.RejectRole)
        copy_button.clicked.connect(lambda: self.copy_to_clipboard(hashes_str))
        close_button.clicked.connect(msg_box.close)
        msg_box.exec()

    def copy_to_clipboard(self, text):
        clipboard = QApplication.clipboard()
        clipboard.setText(text)
        print("Hashes copied to clipboard.")
        
    def upload_files(self):
        self.upload_popup()
        
    def upload_popup(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Upload File")
        
        layout = QVBoxLayout(dialog)
        
        # URL 입력
        url_input_label = QLabel("Enter GitHub Repo URL:", dialog)
        layout.addWidget(url_input_label)
        
        url_input = QLineEdit(dialog)
        url_input.setText(self.repo_owner)
        layout.addWidget(url_input)
        
        # GitHub 리포지토리 정보
        repo_owner_input, ok = QInputDialog.getText(dialog, "GitHub Repo Owner", "Enter GitHub repo owner:")
        if ok:
            self.repo_owner = repo_owner_input
        
        repo_name_input, ok = QInputDialog.getText(dialog, "GitHub Repo Name", "Enter GitHub repo name:")
        if ok:
            self.repo_name = repo_name_input
        
        token_input, ok = QInputDialog.getText(dialog, "GitHub Token", "Enter GitHub personal access token:")
        if ok:
            self.token = token_input
        
        target_path_input, ok = QInputDialog.getText(dialog, "Target Path", "Enter target file path:")
        if ok:
            self.target_path = target_path_input
        
        # 파일 선택
        file_path_input = QFileDialog.getOpenFileName(dialog, "Select file to upload")
        if file_path_input:
            self.file_path = file_path_input[0]
        
        upload_button = QPushButton("Upload", dialog)
        upload_button.clicked.connect(self.upload_files)  # 변경된 부분
        layout.addWidget(upload_button)
        
        save_button = QPushButton("Save", dialog)
        save_button.clicked.connect(self.save_settings)
        layout.addWidget(save_button)
        
        dialog.setLayout(layout)
        dialog.exec()

    def save_settings(self):
        settings = {
            "repo_owner": self.repo_owner,
            "repo_name": self.repo_name,
            "token": self.token,
            "target_path": self.target_path,
            "file_path": self.file_path
        }
        with open("settings.json", "w") as f:
            json.dump(settings, f)
        
    def load_settings(self):
        if os.path.exists("settings.json"):
            with open("settings.json", "r") as f:
                settings = json.load(f)
                self.repo_owner = settings.get("repo_owner", "")
                self.repo_name = settings.get("repo_name", "")
                self.token = settings.get("token", "")
                self.target_path = settings.get("target_path", "")
                self.file_path = settings.get("file_path", "")
                self.label.setText(f"Settings Loaded: {self.repo_owner} - {self.repo_name}")
        else:
            self.label.setText("No settings file found.")
        
if __name__ == "__main__":
    app = QApplication([])
    window = SimpleGUI()
    window.show()
    app.exec()
