import moviepy.editor as mp

import os 
from pydub import AudioSegment
from pydub.silence import split_on_silence
import time
import nltk
import moviepy.editor as mp


def getSize(filename):
    st = os.stat(filename)
    return st.st_size

def video_to_audio():
    miVideo = mp.VideoFileClip("GOPR1286.mp4")
    miVideo.audio.write_audiofile("gopro.wav")
    




def audio(path):
    r = sr.Recognizer()
    sound = AudioSegment.from_wav(path)  
    #print(path)
    # split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
    # experiment with this value for your target audio file
    min_silence_len = 500,
    # adjust this per requirement
    silence_thresh = sound.dBFS-14,
    # keep the silence for 1 second, adjustable as well
    keep_silence=200,
    )
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # process each chunk 
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            print(getSize(chunk_filename))
            try:
                text = r.recognize_google(audio_listened, language='es-ES')
            except sr.UnknownValueError as e:
                    print("Error:", str(e))
            else:
                text = f"{text} "
                print(chunk_filename, ":", text)
                whole_text += text
        # return the text for all chunks detected
    #print(whole_text)
    #Hay que tokenizar y separar cada palabra
    
    
    
    
    
    
    
    
    
    ####################TOKENIZAR ############################
    word_tokens = nltk.word_tokenize(whole_text)
    #Ya funciona
    #print(word_tokens)
    return word_tokens

def codigos(path):
    data = audio(path)
    print(type(data))
    longitud = len(data) #Longitus es de 78
    x = 0 
    while x < longitud:
        if data[x] == 'subo' and data[x + 1] == 'marcha':
            data.insert(x+2, '[SM]')
        elif data[x] == 'bajo' and data[x + 1] == 'de' and data[x + 2] == 'marcha':
            data.insert(x+3, '[BM]')

        x = x+1
    print(data)
        
        
        
        #if data[x] == 'hola' and data[x+1] == 'buenas':
            #data.insert(2, '[FV]')
    #print(data)




if __name__ == "__main__":
    #video_to_audio()
    path = os.getcwd() + '\\' +  'stops.wav' 
    audio(path)
    codigos(path)

