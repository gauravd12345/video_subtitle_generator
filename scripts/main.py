import os
import moviepy.editor as mp 
import speech_recognition as sr  
from pydub import AudioSegment 
from pydub.silence import split_on_silence 
  

#  Seperates audio from video
def videoToAudio(clips):
    for clip in clips:
        print("\nClip found: " + clip)
        # Inserting video files at the specified path
        videoString = "video_files\original_videos" + "\\" + clip 
        videoFiles = mp.VideoFileClip(r"%s" % videoString) 
        
        # Creating audio files at the specified path
        extension = os.path.splitext(clip)[0]
        audioString = "audio_files" + "\\" + extension + ".wav"
        videoFiles.audio.write_audiofile(r"%s" % audioString) 


# Converts audio to text
def audioToText(path):
    # open the audio file stored in 
    # the local system as a wav file. 
    song = AudioSegment.from_wav(path) 
    print("Done1")
    # open a file where we will concatenate   
    # and store the recognized text 
    fh = open("recognized.txt", "w+") 
    print("Done1.5")      
    # split track where silence is 0.5 seconds  
    # or more and get chunks 
    chunks = split_on_silence(song, 
        # must be silent for at least 0.5 seconds 
        # or 500 ms. adjust this value based on user 
        # requirement. if the speaker stays silent for  
        # longer, increase this value. else, decrease it. 
        min_silence_len = 500, 
  
        # consider it silent if quieter than -16 dBFS 
        # adjust this per requirement 
        silence_thresh = -16
    ) 
    print("Done2")
    # create a directory to store the audio chunks. 
    #try: 
        #os.mkdir('audio_chunks') 
    #except(FileExistsError): 
        #pass
  
    # move into the directory to 
    # store the audio files. 
    #os.chdir('audio_chunks') 
  
    i = 0
    print("Done3")
    # process each chunk 
    for chunk in chunks: 
              
        # Create 0.5 seconds silence chunk 
        chunk_silent = AudioSegment.silent(duration = 10) 
  
        # add 0.5 sec silence to beginning and  
        # end of audio chunk. This is done so that 
        # it doesn't seem abruptly sliced. 
        audio_chunk = chunk_silent + chunk + chunk_silent 
  
        # export audio chunk and save it in  
        # the current directory. 
        print("saving chunk{0}.wav".format(i)) 
        # specify the bitrate to be 192 k 
        audio_chunk.export("./chunk{0}.wav".format(i), bitrate ='192k', format ="wav") 
  
        # the name of the newly created chunk 
        filename = 'chunk'+str(i)+'.wav'
  
        print("Processing chunk "+str(i)) 
  
        # get the name of the newly created chunk 
        # in the AUDIO_FILE variable for later use. 
        file = filename 
  
        # create a speech recognition object 
        r = sr.Recognizer() 
  
        # recognize the chunk 
        with sr.AudioFile(file) as source: 
            # remove this if it is not working 
            # correctly. 
            r.adjust_for_ambient_noise(source) 
            audio_listened = r.listen(source) 
  
        try: 
            # try converting it to text 
            rec = r.recognize_google(audio_listened) 
            # write the output to the file. 
            fh.write(rec+". ") 
  
        # catch any errors. 
        except sr.UnknownValueError: 
            print("Could not understand audio") 
  
        except sr.RequestError as e: 
            print("Could not request results. check your internet connection") 
  
        i += 1
  
    os.chdir('..')

  
    


# Applies the text onto the videos
def applyText():
    pass


# Removes everything within a directory
def clearDirectory(directory):
    pass


# Main method
def main():
    clips = os.listdir("video_files\original_videos")
    #videoToAudio(clips)
    audioToText("audio_files\obama.wav")


# Calling main method
if __name__ == "__main__":
    main()