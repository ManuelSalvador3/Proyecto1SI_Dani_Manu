import moviepy.editor as mp
import speech_recognition as sr
import os 
from pydub import AudioSegment
from pydub.silence import split_on_silence
import time
import nltk
import moviepy.editor as mp
from pydub.utils import make_chunks


def video_to_audio():
    miVideo = mp.VideoFileClip("GOPR1286.mp4")
    miVideo.audio.write_audiofile("gopro.wav")
    

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
    whole_text = ""
    file1 = open("chunks.txt","a")
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
                #print(chunk_filename, ":", text)
                whole_text += text
                file1.write(text)
                file1.write("\n\n")
    ####################TOKENIZAR ############################
    print("Fichero escrito")
    word_tokens = nltk.word_tokenize(whole_text)
    #Ya funciona
    return word_tokens

def codigos(path):
    data = transcription(path)
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
        
        
        
        #if data[x] == 'hola' and data[x+1] == 'buenas':
            #data.insert(2, '[FV]')
    #print(data)




if __name__ == "__main__":
    #video_to_audio()
    path = os.getcwd() + '\\' +  'gopro.wav' 
    codigos(path)

