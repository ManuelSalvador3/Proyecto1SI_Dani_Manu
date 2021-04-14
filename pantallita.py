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
        self.textbox = QLabel("No le de al play hasya que no salgan aqui los dialogos", self)
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
            audio = video_to_audio(filename)#Convertimos el video en audio
            codigos(audio) #Codigos ya llama por si mismo a transformation
    
    def play_video(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def video_to_audio():
        miVideo = mp.VideoFileClip("GOPR1286.mp4")
        audio = miVideo.audio.write_audiofile("gopro.wav")
        return audio
        

    def transcription(path):
        myaudio = AudioSegment.from_file(path , "wav") 
        chunk_length_ms = 25000 # pydub calculates in millisec
        chunks = make_chunks(myaudio, chunk_length_ms) #Make chunks of one sec

        folder_name = "audio-chunks"
            # create a directory to store the audio chunks
        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)

        #Export all of the individual chunks as wav files

        for i, chunk in enumerate(chunks):
            chunk_name = os.path.join(folder_name, f"chunk{i}.wav")
            #print ("exporting", chunk_name)
            chunk.export(chunk_name, format="wav")
        print("Chunks exportados correctamente...")
        r = sr.Recognizer() 
        lista_chunks = []
        for i, audio_chunk in enumerate(chunks, start=1):
            # export audio chunk and save it in
            # the `folder_name` directory.
            chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
            audio_chunk.export(chunk_filename, format="wav")
            # recognize the chunk
            with sr.AudioFile(chunk_filename) as source:
                audio_listened = r.record(source)
                try:
                    text = r.recognize_google(audio_listened, language='es-ES')
                except sr.UnknownValueError as e:
                    print("Error:", str(e))
                else:
                    text = f"{text} "
                    lista_chunks.insert(i, text)
        ####################TOKENIZAR ############################
        print("Fichero escrito")
        data = nltk.word_tokenize(whole_text)
        return data, lista_chunks


    def codigos(path):
        data, lista_chunks = transcription(path)
        longitud = len(data) #Longitus es de 78
        x = 0 
        while x < longitud:
            ##CODIGOS DE ACCIONES DE MANOS Y PIES
            if data[x] == 'giro' and data[x + 1] == 'derecha':
                data.insert(x+2, '[SW-TL-R]')
            elif data[x] == 'giro' and data[x + 1] == 'izquierda':
                data.insert(x+2, '[SW-TL-L]')
            elif data[x] == 'subo' and data[x + 1] == 'marcha':
                data.insert(x+2, '[GU]')
            elif data[x] == 'bajo' and data[x + 1] == 'marcha':
                data.insert(x+2, '[GD]')
            elif data[x] == 'bajo' and data[x + 1] == 'de' and data[x + 2] == 'marcha':
                data.insert(x+2, '[GD]')
            elif data[x] == 'intermitente' and data[x + 1] == 'izquierda':
                data.insert(x+2, '[LB-ON]')
            elif data[x] == 'intermitente' and data[x + 1] == 'derecha':
                data.insert(x+2, '[RB-ON]')
            elif data[x] == 'piso' and data[x + 1] == 'embrague':
                data.insert(x+2, '[G-ON]')
            elif data[x] == 'suelto' and data[x + 1] == 'embrague':
                data.insert(x+2, '[G-OFF]')
            elif data[x] == 'piso' and data[x + 1] == 'acelerador':
                data.insert(x+2, '[T-ON]')
            elif data[x] == 'suelto' and data[x + 1] == 'acelerador':
                data.insert(x+2, '[T-OFF]')
            elif data[x] == 'piso' and data[x + 1] == 'freno':
                data.insert(x+2, '[B-ON]')
            elif data[x] == 'piso' and data[x + 1] == 'frenos':
                data.insert(x+2, '[B-ON]')
            elif data[x] == 'suelto' and data[x + 1] == 'freno':
                data.insert(x+2, '[B-OFF]')
            ##CODIGOS DE ESTIMULOS
            elif data[x] == 'miro' and data[x + 1] == 'frente':
                data.insert(x+2, '[FV]')
            elif data[x] == 'mira' and data[x + 1] == 'enfrente':
                data.insert(x+2, '[FV]')
            elif data[x] == 'miro' and data[x + 1] == 'retrovisor' and data[x + 2] == 'central':
                data.insert(x+3, '[FV-MIRROR]')
            elif data[x] == 'mira' and data[x + 1] == 'retrovisor' and data[x + 2] == 'central':
                data.insert(x+3, '[FV-MIRROR]')
            elif data[x] == 'miro' and data[x + 1] == 'central':
                data.insert(x+2, '[FV-MIRROR]')
            elif data[x] == 'miro' and data[x + 1] == 'izquierda':
                data.insert(x+2, '[LV]')
            elif data[x] == 'retrovisor' and data[x + 1] == 'izquierda':
                data.insert(x+2, '[LV-MIRROR]')
            elif data[x] == 'miro' and data[x + 1] == 'retrovisor' and data[x + 2] == 'izquierda':
                data.insert(x+3, '[LV-MIRROR]')
            elif data[x] == 'miro' and data[x + 1] == 'frente' and data[x + 2] == 'izquierda':
                data.insert(x+3, '[FLV]')
            elif data[x] == 'miro' and data[x + 1] == 'derecha':
                data.insert(x+2, '[RV]')
            elif data[x] == 'miro' and data[x + 1] == 'retrovisor' and data[x + 2] == 'derecha':
                data.insert(x+3, '[RV-MIRROR]')
            elif data[x] == 'miro' and data[x + 1] == 'frente' and data[x + 2] == 'derecha':
                data.insert(x+3, '[FRV]')
            elif data[x] == 'miro' and data[x + 1] == 'detras':
                data.insert(x+2, '[BV]')
            x = x+1
        print(data)
        return data #Puede que no haga falta

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