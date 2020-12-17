from pydub import AudioSegment
from pydub.playback import play

play(AudioSegment.from_mp3("./sound/passed.mp3"))