from moviepy.editor import *
import os

#Converts all mp4 files into mp3 files in the current direcotry
def convert_mp4_to_mp3():
    """
    Converts mp4 video to mp3
    """
    #find all .mp4 files in current directory
    files = os.listdir()
    mp4_files = [x for x in files if '.mp4' in x]

    #convert all .mp4 into .mp3
    for f in mp4_files:
        mp3_file = f.strip('.mp4') + '.mp3'
        clip = AudioFileClip(f)
        clip.write_audiofile(mp3_file)
        clip.close()
        os.remove(f)
