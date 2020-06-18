import pyaudio
import wave
import os
from sets import Set

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

CHUNK = 512
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 22050
RECORD_SECONDS = 1

digitsLower = Set(['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine'])

name = "y"

while name!= "x":
    print bcolors.HEADER + "WELCOME to SPOKEN WORD RECOGNIZER!"  + bcolors.ENDC
    print "This program will record your voice for 1 second to transcribe it"
    name = raw_input(bcolors.WARNING + "Type R (or r) to record your voice \n" + bcolors.ENDC)
    
    if name == "r" or name == "R":
        expected = raw_input(bcolors.WARNING + "Type what you expect to see \n" + bcolors.ENDC).lower()

        # If block to check whether that we can transcribe or not
        if expected not in digitsLower:
            print "Unfortountely we can not transcribe " + expected + "at the moment"
            break
        
        # The recorded voice will be recorded to a labeled folder
        WAVE_OUTPUT_FILENAME = "digits_test/" + expected +"/" + expected + ".wav"
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        # TODO: Countdown to recording

        print "* recording"

        frames = []

        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        print "* done recording"

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        #os.system('mv one.wav md_test/one/one.wav')
        
        os.system('python speech.py --input digits --transcribe ' + WAVE_OUTPUT_FILENAME)
        

print bcolors.WARNING + "Thank your for using our spoken word recognizer \n" + bcolors.ENDC
print bcolors.BOLD + bcolors.UNDERLINE + "see for details: https://github.com/mtunad/SpokenDigitRecognizer" + bcolors.ENDC + bcolors.ENDC
