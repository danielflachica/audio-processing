from pydub import AudioSegment
from os import listdir
import sys
import audio_utils as au


def convert_file_to_wav(mp3_file, filepath, outdir='wav'):
	au.create_dir_if_none(outdir)

	sound = AudioSegment.from_mp3(filepath+'/'+mp3_file)
	wav_file = outdir + '/' + au.add_extension(au.strip_extension(mp3_file), 'wav')
	sound.export(wav_file, format='wav')


def convert_dir_to_wav(mp3_list, filepath, outdir='wav'):
	au.create_dir_if_none(outdir)

	for mp3_file in mp3_list:
		sound = AudioSegment.from_mp3(filepath+'/'+mp3_file)
		wav_file = outdir + '/' + au.add_extension(au.strip_extension(mp3_file), 'wav')
		sound.export(wav_file, format='wav')



if __name__=="__main__":
	file_path_args = sys.argv[1:] # the first argument is the script itself

	if len(file_path_args) > 2:
		print('Error: More thah 2 arguments were supplied')
		exit()
	elif len(file_path_args) < 1:
		print("Error: No input argument was supplied")
		exit()
	else:
		# convert args into string
		fpath = file_path_args[0]
		
		if len(file_path_args) == 2:
			outdir = file_path_args[1]
		else:
			outdir = 'wav'

	# get a list of the files inside the given directory
	# flist = listdir(fpath if len(file_path_args) > 0 else None)
	flist = listdir(fpath)

	# batch convert
	convert_dir_to_wav(flist, fpath, outdir)