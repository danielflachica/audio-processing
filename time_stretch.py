# coding=utf8
# time_stretch.py
# author: Gagandeep Singh, 29 Oct, 2018

from os import path
import argparse
import librosa
import numpy as np
import soundfile

# define standard sample rate
SAMPLE_RATE = 44100

def main(args):
    x, sr = librosa.core.load(args.in_file, sr=SAMPLE_RATE)
    # print('old:', args.factor)
    args.factor = invert_factor(args.factor)
    x_stretched = stretch(x, args.factor)
    # print('new:', args.factor)

    out_file = args.out_file
    if out_file is None:
        out_file = path.join(path.dirname(args.in_file), 'time_stretched.wav')
    
    soundfile.write(out_file, x_stretched, sr)


def invert_factor(factor):
    return factor ** -1


def stretch(x, factor, nfft=2048):
    '''
    stretch an audio sequence by a factor using FFT of size nfft converting to frequency domain
    :param x: np.ndarray, audio array in PCM float32 format
    :param factor: float, stretching or shrinking factor, depending on if its > or < 1 respectively
    :return: np.ndarray, time stretched audio
    '''
    stft = librosa.core.stft(x, n_fft=nfft).transpose()  # i prefer time-major fashion, so transpose
    stft_rows = stft.shape[0]
    stft_cols = stft.shape[1]

    times = np.arange(0, stft.shape[0], factor)  # times at which new FFT to be calculated
    hop = nfft/4                                 # frame shift
    stft_new = np.zeros((len(times), stft_cols), dtype=np.complex_)
    phase_adv = (2 * np.pi * hop * np.arange(0, stft_cols))/ nfft
    phase = np.angle(stft[0])

    stft = np.concatenate( (stft, np.zeros((1, stft_cols))), axis=0)

    for i, time in enumerate(times):
        left_frame = int(np.floor(time))
        local_frames = stft[[left_frame, left_frame + 1], :]
        right_wt = time - np.floor(time)                        # weight on right frame out of 2
        local_mag = (1 - right_wt) * np.absolute(local_frames[0, :]) + right_wt * np.absolute(local_frames[1, :])
        local_dphi = np.angle(local_frames[1, :]) - np.angle(local_frames[0, :]) - phase_adv
        local_dphi = local_dphi - 2 * np.pi * np.floor(local_dphi/(2 * np.pi))
        stft_new[i, :] =  local_mag * np.exp(phase*1j)
        phase += local_dphi + phase_adv

    return librosa.core.istft(stft_new.transpose())


if __name__ == '__main__':
    parser = argparse.ArgumentParser('speed up or speed down the audio without changing the pitch')
    parser.add_argument('-i', '--in-file',
                        type=str,
                        required=True,
                        help='path to the input wav file')
    parser.add_argument('-o', '--out-file',
                        type=str,
                        default=None,
                        help='path of the output file')
    parser.add_argument('-f', '--factor',
                        type=float,
                        required=True,
                        help='factor by which to shrink or dilate time. if FACTOR < 1.0, audio will be sped\
                        up, otherwise sped down')
    parser.add_argument('-n', '--nfft',
                        type=int,
                        default=2048,
                        help='num of FFT bins to use')
    args = parser.parse_args()
    main(args)
