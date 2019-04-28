# put this .py file into your corpus file
import wave
import contextlib

duration = 0
# change the range to the numbers of your files
for i in range(1, 101):
    fname = str(i) + '.wav'
    try:
        with contextlib.closing(wave.open(fname, 'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration += frames / float(rate)
    except Exception as e:
        print(e)
print(duration)
