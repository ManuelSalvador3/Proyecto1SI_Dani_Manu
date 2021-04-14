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
    
#FUNCIONA OSTIA PUTA
def transcription(path):
    myaudio = AudioSegment.from_file(path , "wav") 
    chunk_length_ms = 26000 # pydub calculates in millisec
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
    for i, audio_chunk in enumerate(chunks, start=0): #Antes era 1 
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
                tokenizar = nltk.word_tokenize(text) #lista
                y = 0
                while y < len(tokenizar):
                    if tokenizar[y] == 'giro' and tokenizar[y + 1] == 'derecha':
                        tokenizar.insert(y+2, '[SW-TL-R]')
                    elif tokenizar[y] == 'giro' and tokenizar[y + 1] == 'izquierda':
                        tokenizar.insert(y+2, '[SW-TL-L]')
                    elif tokenizar[y] == 'subo' and tokenizar[y + 1] == 'marcha':
                        tokenizar.insert(y+2, '[GU]')
                    elif tokenizar[y] == 'bajo' and tokenizar[y + 1] == 'marcha':
                        tokenizar.insert(y+2, '[GD]')
                    elif tokenizar[y] == 'bajo' and tokenizar[y + 1] == 'de' and tokenizar[y + 2] == 'marcha':
                        tokenizar.insert(y+2, '[GD]')
                    elif tokenizar[y] == 'intermitente' and tokenizar[y + 1] == 'izquierda':
                        tokenizar.insert(y+2, '[LB-ON]')
                    elif tokenizar[y] == 'intermitente' and tokenizar[y + 1] == 'derecha':
                        tokenizar.insert(y+2, '[RB-ON]')
                    elif tokenizar[y] == 'piso' and tokenizar[y + 1] == 'embrague':
                        tokenizar.insert(y+2, '[G-ON]')
                    elif tokenizar[y] == 'suelto' and tokenizar[y + 1] == 'embrague':
                        tokenizar.insert(y+2, '[G-OFF]')
                    elif tokenizar[y] == 'piso' and tokenizar[y + 1] == 'acelerador':
                        tokenizar.insert(y+2, '[T-ON]')
                    elif tokenizar[y] == 'suelto' and tokenizar[y + 1] == 'acelerador':
                        tokenizar.insert(y+2, '[T-OFF]')
                    elif tokenizar[y] == 'piso' and tokenizar[y + 1] == 'freno':
                        tokenizar.insert(y+2, '[B-ON]')
                    elif tokenizar[y] == 'piso' and tokenizar[y + 1] == 'frenos':
                        tokenizar.insert(y+2, '[B-ON]')
                    elif tokenizar[y] == 'suelto' and tokenizar[y + 1] == 'freno':
                        tokenizar.insert(y+2, '[B-OFF]')
                    ##CODIGOS DE ESTIMULOS
                    elif tokenizar[y] == 'miro' and tokenizar[y + 1] == 'frente':
                        tokenizar.insert(y+2, '[FV]')
                    elif tokenizar[y] == 'mira' and tokenizar[y + 1] == 'enfrente':
                        tokenizar.insert(y+2, '[FV]')
                    elif tokenizar[y] == 'miro' and tokenizar[y + 1] == 'retrovisor' and tokenizar[y + 2] == 'central':
                        tokenizar.insert(y+3, '[FV-MIRROR]')
                    elif tokenizar[y] == 'mira' and tokenizar[y + 1] == 'retrovisor' and tokenizar[y + 2] == 'central':
                        tokenizar.insert(y+3, '[FV-MIRROR]')
                    elif tokenizar[y] == 'miro' and tokenizar[y + 1] == 'central':
                        tokenizar.insert(y+2, '[FV-MIRROR]')
                    elif tokenizar[y] == 'miro' and tokenizar[y + 1] == 'izquierda':
                        tokenizar.insert(y+2, '[LV]')
                    elif tokenizar[y] == 'retrovisor' and tokenizar[y + 1] == 'izquierda':
                        tokenizar.insert(y+2, '[LV-MIRROR]')
                    elif tokenizar[y] == 'miro' and tokenizar[y + 1] == 'retrovisor' and tokenizar[y + 2] == 'izquierda':
                        tokenizar.insert(y+3, '[LV-MIRROR]')
                    elif tokenizar[y] == 'miro' and tokenizar[y + 1] == 'frente' and tokenizar[y + 2] == 'izquierda':
                        tokenizar.insert(y+3, '[FLV]')
                    elif tokenizar[y] == 'miro' and tokenizar[y + 1] == 'derecha':
                        tokenizar.insert(y+2, '[RV]')
                    elif tokenizar[y] == 'miro' and tokenizar[y + 1] == 'retrovisor' and tokenizar[y + 2] == 'derecha':
                        tokenizar.insert(y+3, '[RV-MIRROR]')
                    elif tokenizar[y] == 'miro' and tokenizar[y + 1] == 'frente' and tokenizar[y + 2] == 'derecha':
                        tokenizar.insert(y+3, '[FRV]')
                    elif tokenizar[y] == 'miro' and tokenizar[y + 1] == 'detras':
                        tokenizar.insert(y+2, '[BV]')
                    y = y+1
                #print(tokenizar)
                lista_chunks.insert(i, tokenizar)
                #print(len(lista_chunks[i]))
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text} "
                #print(chunk_filename, ":", text)
                whole_text += text
                whole_text += '\n'
    x = 0
    while x < len(lista_chunks):
        print('Chunk'+ str(x) + ': ' + str(lista_chunks[x]))
        print('\n\n')
        x = x+1
    return lista_chunks
        
        
        #if data[x] == 'hola' and data[x+1] == 'buenas':
            #data.insert(2, '[FV]')
    #print(data)




if __name__ == "__main__":
    #video_to_audio()
    path = os.getcwd() + '\\' +  'gopro.wav' 
    transcription(path)

