import sys
from youtube_transcript_api import YouTubeTranscriptApi
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QTextEdit, QLabel

def get_transcript(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        manual_transcripts = [t for t in transcript_list if not t.is_generated]
        if manual_transcripts:
            transcript = manual_transcripts[0].fetch()
        else:
            generated_transcripts = [t for t in transcript_list if t.is_generated]
            if generated_transcripts:
                transcript = generated_transcripts[0].fetch()
            else:
                return None, "자막을 찾을 수 없습니다."
    except Exception as e:
        return None, "Error: " + str(e)

    full_text = " ".join([text['text'] for text in transcript])
    return full_text, None

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.url_label = QLabel("유튜브 영상 URL을 입력하세요:")
        layout.addWidget(self.url_label)

        self.url_input = QLineEdit()
        layout.addWidget(self.url_input)

        self.get_transcript_button = QPushButton("자막 가져오기")
        self.get_transcript_button.clicked.connect(self.show_transcript)
        layout.addWidget(self.get_transcript_button)

        self.transcript_text_edit = QTextEdit()
        layout.addWidget(self.transcript_text_edit)

        self.setLayout(layout)

    def show_transcript(self):
        video_url = self.url_input.text()
        video_id = video_url.split("watch?v=")[-1]

        transcript_text, error = get_transcript(video_id)
        if error:
            self.transcript_text_edit.setPlainText(error)
        else:
            self.transcript_text_edit.setPlainText(transcript_text)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.setWindowTitle("유튜브 자막 추출기")
    main_window.show()

    sys.exit(app.exec_())
