# REFERENCE: https://stackoverflow.com/a/48050429/13178828
import librosa
import soundfile as sf

# define standard sample rate
SAMPLE_RATE = 44100

# load input wav file into y. sr = sample rate
y, sr = librosa.load('wav/Helpless.wav', SAMPLE_RATE)

# shift the pitch by n_steps
y_shifted = librosa.effects.pitch_shift(y, sr, n_steps=3)

# output pitch-shifted audio to wav
sf.write('wav/Helpless-pitch-shifted-3-up.wav', y_shifted, sr, subtype='PCM_24')