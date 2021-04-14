import moviepy.editor as mp
import speech_recognition as sr
import os 
from pydub import AudioSegment
from pydub.silence import split_on_silence
import time
import nltk
import moviepy.editor as mp
from pydub.utils import make_chunks
from unidecode import unidecode


def video_to_audio():
    miVideo = mp.VideoFileClip("GOPR1286.mp4")
    hola = miVideo.audio.write_audiofile("gopro.wav")
    return hola
    

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
    lista_chunks = []
    file1 = open("chunks.txt","a")
    for i, audio_chunk in enumerate(chunks, start=0):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            try:
                text = r.recognize_google(audio_listened, language='es-ES')
                print('chunk', i)
                text = unidecode(text)
                lista_chunks.insert(i, text)
                file1.write(text)
                file1.write("\n")
                print(lista_chunks[i])
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text} "
                #print(chunk_filename, ":", text)
                whole_text += text
                
    ####################TOKENIZAR############################
    print("Fichero escrito")
    z = 0
    data = [0]
    while z < len(lista_chunks):
        data.insert(z,  nltk.word_tokenize(lista_chunks[z+1])) 
        z = z+1
    print(data)
    return data


def codigos(path):
    data = transcription(path)
    longitud = len(data[0]) #Longitus es de 78 
    longitud_interior = len(data[0][0])
    x = 0 
    y = 0  
    #Data[y][x]
    for i in 
        while x < longitud_interior:
            ##CODIGOS DE ACCIONES DE MANOS Y PIES
            if data[y][x] == 'giro' and data[y][x + 1] == 'derecha':
                data[y].insert(x+2, '[SW-TL-R]')
            elif data[y][x] == 'giro' and data[y][x + 1] == 'izquierda':
                data[y].insert(x+2, '[SW-TL-L]')
            elif data[y][x] == 'subo' and data[y][x + 1] == 'marcha':
                data[y].insert(x+2, '[GU]')
            elif data[y][x] == 'bajo' and data[y][x + 1] == 'marcha':
                data[y].insert(x+2, '[GD]')
            elif data[y][x] == 'bajo' and data[y][x + 1] == 'de' and data[y][x + 2] == 'marcha':
                data[y].insert(x+2, '[GD]')
            elif data[y][x] == 'intermitente' and data[y][x + 1] == 'izquierda':
                data[y].insert(x+2, '[LB-ON]')
            elif data[y][x] == 'intermitente' and data[y][x + 1] == 'derecha':
                data[y].insert(x+2, '[RB-ON]')
            elif data[y][x] == 'piso' and data[y][x + 1] == 'embrague':
                data[y].insert(x+2, '[G-ON]')
            elif data[y][x] == 'suelto' and data[y][x + 1] == 'embrague':
                data[y].insert(x+2, '[G-OFF]')
            elif data[y][x] == 'piso' and data[y][x + 1] == 'acelerador':
                data[y].insert(x+2, '[T-ON]')
            elif data[y][x] == 'suelto' and data[y][x + 1] == 'acelerador':
                data[y].insert(x+2, '[T-OFF]')
            elif data[y][x] == 'piso' and data[y][x + 1] == 'freno':
                data[y].insert(x+2, '[B-ON]')
            elif data[y][x] == 'piso' and data[y][x + 1] == 'frenos':
                data[y].insert(x+2, '[B-ON]')
            elif data[y][x] == 'suelto' and data[y][x + 1] == 'freno':
                data[y].insert(x+2, '[B-OFF]')
            ##CODIGOS DE ESTIMULOS
            elif data[y][x] == 'miro' and data[y][x + 1] == 'frente':
                data[y].insert(x+2, '[FV]')
            elif data[y][x] == 'mira' and data[y][x + 1] == 'enfrente':
                data[y].insert(x+2, '[FV]')
            elif data[y][x] == 'miro' and data[y][x + 1] == 'retrovisor' and data[y][x + 2] == 'central':
                data[y].insert(x+3, '[FV-MIRROR]')
            elif data[y][x] == 'mira' and data[y][x + 1] == 'retrovisor' and data[y][x + 2] == 'central':
                data[y].insert(x+3, '[FV-MIRROR]')
            elif data[y][x] == 'miro' and data[y][x + 1] == 'central':
                data[y].insert(x+2, '[FV-MIRROR]')
            elif data[y][x] == 'miro' and data[y][x + 1] == 'izquierda':
                data[y].insert(x+2, '[LV]')
            elif data[y][x] == 'retrovisor' and data[y][x + 1] == 'izquierda':
                data[y].insert(x+2, '[LV-MIRROR]')
            elif data[y][x] == 'miro' and data[y][x + 1] == 'retrovisor' and data[y][x + 2] == 'izquierda':
                data[y].insert(x+3, '[LV-MIRROR]')
            elif data[y][x] == 'miro' and data[y][x + 1] == 'frente' and data[y][x + 2] == 'izquierda':
                data[y].insert(x+3, '[FLV]')
            elif data[y][x] == 'miro' and data[y][x + 1] == 'derecha':
                data[y].insert(x+2, '[RV]')
            elif data[y][x] == 'miro' and data[y][x + 1] == 'retrovisor' and data[y][x + 2] == 'derecha':
                data[y].insert(x+3, '[RV-MIRROR]')
            elif data[y][x] == 'miro' and data[y][x + 1] == 'frente' and data[y][x + 2] == 'derecha':
                data[y].insert(x+3, '[FRV]')
            elif data[y][x] == 'miro' and data[y][x + 1] == 'detras':
                data[y].insert(x+2, '[BV]')
            x = x+1
            longitud_interior = len(data[y][x])
        y = y+1
        longitud = len(data[y])

    print(data)
    return data
        
        
        
        #if data[x] == 'hola' and data[x+1] == 'buenas':
            #data.insert(2, '[FV]')
    #print(data)




if __name__ == "__main__":
    #video_to_audio()
    path = os.getcwd() + '\\' +  'gopro.wav' 
    codigos(path)

