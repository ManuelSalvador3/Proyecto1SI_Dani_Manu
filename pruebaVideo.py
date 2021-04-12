from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, \
    QSlider, QStyle, QSizePolicy, QFileDialog, QLineEdit
import sys
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import QIcon, QPalette
from PyQt5.QtCore import Qt, QUrl
import moviepy.editor as mp
import speech_recognition as sr
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
import time

video = ""


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt5 Media Player")
        self.setGeometry(650, 100, 900, 800)
        self.setWindowIcon(QIcon('player.png'))

        p = self.palette()
        p.setColor(QPalette.Window, Qt.white)
        self.setPalette(p)

        self.init_ui()

        self.show()

    def init_ui(self):

        # create media player object
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        # create videowidget object

        videowidget = QVideoWidget()

        # create open button
        openBtn = QPushButton('Open Video')
        openBtn.clicked.connect(self.open_file)

        # create button for playing
        self.playBtn = QPushButton()
        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.clicked.connect(self.play_video)

        # create slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 0)
        self.slider.sliderMoved.connect(self.set_position)

        # create label
        self.label = QLabel()
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        # create field text
        self.textbox = QLabel("Aqui Manu contandonos su vida de mierda", self)
        self.textbox.move(20, 20)
        self.textbox.resize(280, 40)
        self.textbox.setFixedWidth(600)

        # create hbox layout
        hboxLayout = QHBoxLayout()
        hboxLayout.setContentsMargins(0, 0, 0, 0)

        secondHboxLayout = QVBoxLayout()
        secondHboxLayout.setContentsMargins(10, 10, 10, 10)

        # set widgets to the hbox layout

        hboxLayout.addWidget(openBtn)
        hboxLayout.addWidget(self.playBtn)
        hboxLayout.addWidget(self.slider)
        # hboxLayout.addLayout(self.textbox)
        secondHboxLayout.addWidget(self.textbox)

        # create vbox layout
        vboxLayout = QVBoxLayout()
        vboxLayout.addWidget(videowidget)
        vboxLayout.addLayout(hboxLayout)
        vboxLayout.addLayout(secondHboxLayout)
        vboxLayout.addWidget(self.label)

        self.setLayout(vboxLayout)

        self.mediaPlayer.setVideoOutput(videowidget)

        # media player signals

        self.mediaPlayer.stateChanged.connect(self.mediastate_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Video")

        if filename != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.playBtn.setEnabled(True)
            #self.conversion(filename)#TODO NO FUNCIONA COÑOOOOOOOOO

    def conversion(video):

        miVideo = mp.VideoFileClip(video)
        # Lo pasamos a wav
        miVideo.audio.write_audiofile("resultado.wav")

        # create a speech recognition object
        r = sr.Recognizer()
        with sr.WavFile("resultado.wav") as source:  # use "test.wav" as the audio source
            audio = r.record(source)
        try:
            texto = r.recognize_google(audio, language='es-ES')  # recognize speech using Google Speech Recognition
            time.sleep(1.5)
            print("Transcripcion " + texto)

        except LookupError:  # speech is unintelligible
            print("Could not understand audio")

        return texto

    def play_video(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()

        else:
            self.mediaPlayer.play()

    def mediastate_changed(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause)

            )

        else:
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay)

            )

    def position_changed(self, position):
        self.slider.setValue(position)

    def duration_changed(self, duration):
        self.slider.setRange(0, duration)

    def set_position(self, position):
        self.mediaPlayer.setPosition(position)

    def handle_errors(self):
        self.playBtn.setEnabled(False)
        self.label.setText("Error: " + self.mediaPlayer.errorString())


app = QApplication(sys.argv)
window = Window()
sys.exit(app.exec_())
