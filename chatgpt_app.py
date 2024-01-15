import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget,
                             QFileDialog, QLabel, QHBoxLayout, QSizePolicy)
from PyQt5.QtCore import Qt
import requests
import json

class ChatGPTApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.is_dark_theme = False  # Track the current theme

        self.setWindowTitle("ChatGPT UI")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("font-family: 'Segoe UI'; background-color: #FFFFFF;")  # Default font and background

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        # Chat display area
        self.chat_text = QTextEdit(self)
        self.chat_text.setReadOnly(True)
        self.chat_text.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.main_layout.addWidget(self.chat_text)

        # Attachment and input layout
        self.bottom_layout = QHBoxLayout()
        self.main_layout.addLayout(self.bottom_layout)


        # Attachment display and button
        self.attachment_layout = QVBoxLayout()
        self.attachment_label = QLabel("No file attached", self)
        self.attachment_label.setFixedHeight(20)  # Adjust the height of the label
        self.attachment_button = QPushButton("Attach", self)  # Button for attaching files
        self.attachment_button.setFixedSize(80, 30)  # Adjust the size of the button

        # Connect the button to the attach_file method
        self.attachment_button.clicked.connect(self.attach_file)

        self.attachment_layout.addWidget(self.attachment_label)
        self.attachment_layout.addWidget(self.attachment_button)
        self.bottom_layout.addLayout(self.attachment_layout)

        # Input text area and send button
        self.input_layout = QVBoxLayout()
        self.input_text = QTextEdit(self)
        self.input_text.setFixedHeight(100)
        self.input_text.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        self.send_button = QPushButton("Send", self)
        self.send_button.clicked.connect(self.send_message)
        self.input_layout.addWidget(self.input_text)
        self.input_layout.addWidget(self.send_button)
        self.bottom_layout.addLayout(self.input_layout)

        # Theme toggle button
        self.theme_button = QPushButton("Switch Theme", self)
        self.theme_button.clicked.connect(self.toggle_theme)
        self.main_layout.addWidget(self.theme_button)

        # Style the widgets
        self.style_widgets()

        self.api_key = 'Your-Secure-API-Key'  # Replace with your actual API key

    def style_widgets(self):
        """ Apply CSS styles to widgets """
        self.chat_text.setStyleSheet("background-color: #FFFFFF; color: #333333; border: 1px solid #D3D3D3;")
        self.input_text.setStyleSheet("background-color: #FAFAFA; color: #333333; border: 1px solid #D3D3D3;")
        self.attachment_label.setStyleSheet("margin-top: 5px; color: #555;")
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #5C6BC0;
                color: white;
                padding: 8px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #7986CB;
            }
        """)
        self.attachment_button.setStyleSheet(self.send_button.styleSheet())  # Same style as send_button

        # Custom Scroll Bar for Chat Text
        self.chat_text.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.chat_text.verticalScrollBar().setStyleSheet("""
            QScrollBar:vertical {
                border: none;
                background: #E0E0E0;
                width: 8px;
                margin: 0px 0 0px 0;
            }
            QScrollBar::handle:vertical {
                background: #B0B0B0;
                min-height: 20px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: none;
            }
        """)

    def attach_file(self):
        file_dialog = QFileDialog()
        self.attachment_path, _ = file_dialog.getOpenFileName(self, "Attach File")
        if self.attachment_path:
            filename = os.path.basename(self.attachment_path)
            self.attachment_label.setText(f"Attached: {filename}")

    def send_message(self):
        user_input = self.input_text.toPlainText().strip()
        if not user_input and not hasattr(self, 'attachment_path'):
            self.chat_text.append("Please enter a message or attach a file.")
            return

        self.chat_text.append("You: " + user_input)

        # Handle file attachment here if necessary

        # Send user input to ChatGPT
        url = 'https://api.openai.com/v1/engines/gpt-4.0/completions'
        headers = {'Authorization': f'Bearer {self.api_key}', 'Content-Type': 'application/json'}
        data = {'prompt': user_input, 'max_tokens': 50}

        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            chat_response = response.json()['choices'][0]['text']
            self.chat_text.append("ChatGPT: " + chat_response)
        else:
            self.chat_text.append("Error: Failed to get a response from ChatGPT API")

        # Clear input text
        self.input_text.clear()

    def toggle_theme(self):
        if self.is_dark_theme:
            self.apply_light_theme()
        else:
            self.apply_dark_theme()
        self.is_dark_theme = not self.is_dark_theme

    def apply_light_theme(self):
        self.setStyleSheet("font-family: 'Segoe UI'; background-color: #FFFFFF; color: #333333;")
        self.chat_text.setStyleSheet("background-color: #FFFFFF; color: #333333; border: 1px solid #D3D3D3;")
        self.input_text.setStyleSheet("background-color: #FAFAFA; color: #333333; border: 1px solid #D3D3D3;")
        # Apply light theme styles to other widgets

    def apply_dark_theme(self):
        self.setStyleSheet("font-family: 'Segoe UI'; background-color: #424242; color: #E0E0E0;")
        self.chat_text.setStyleSheet("background-color: #333333; color: #E0E0E0; border: 1px solid #616161;")
        self.input_text.setStyleSheet("background-color: #616161; color: #E0E0E0; border: 1px solid #616161;")
        # Apply dark theme styles to other widgets
def main():
    app = QApplication(sys.argv)
    chat_app = ChatGPTApp()
    chat_app.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
