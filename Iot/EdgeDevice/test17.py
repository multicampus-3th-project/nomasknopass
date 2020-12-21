from pydub.playback import play
from pydub import AudioSegment 
import time
import pygame
pygame.mixer.init()

setuptime = time.time()
play(AudioSegment.from_mp3("./normal.mp3"))
finished = time.time()
print("pydub 소요 시간, {0:.1f}".format(finished-setuptime))

setuptime = time.time()
pygame.mixer.music.load("./normal.mp3")
pygame.mixer.music.play()
while pygame.mixer.music.get_busy() == True:
    continue
finished = time.time()
print("pygame 소요 시간, {0:.1f}".format(finished-setuptime))

