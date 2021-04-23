import audio_metadata
import sys
import os
import csv
import pandas as pd
import audio_utils as au


# Returns a list of dictionaries containing metadata for each track in the given input list of files
def get_track_data(track_list, filepath):
	data = []
	for track in track_list:
		metadata = audio_metadata.load(filepath+'/'+track)

		track_dict = {
			"name": track,
			"size": au.convert_bytes_to_megabytes(metadata['filesize']),
			"duration": au.convert_seconds_to_minutes(metadata['streaminfo'].duration),
			"sample_rate": "{:,} hz".format(metadata['streaminfo'].sample_rate),
		}
		
		data.append(track_dict)
	return data


# Write all of the extracted audio data to a csv file
def write_to_csv(header, data, outfile="out.csv"):
	with open(outfile, mode='w', newline='') as csv_file:
		writer = csv.DictWriter(csv_file, fieldnames=header)

		writer.writeheader()
		for track in data:
			writer.writerow(track)


# Convert given csv to an Excel file and open it
def convert_csv_to_xlsx(csv, outfile="out.xlsx"):
	csv_file = pd.read_csv(csv)
	csv_file.to_excel(outfile, index=None, header=True)



if __name__=="__main__":
	file_path_args = sys.argv[1:] # the first argument is the script itself

	if len(file_path_args) > 2:
		print('Error: More thah 2 arguments were supplied')
		exit()
	elif len(file_path_args) > 1:
		fpath = file_path_args[0]
		outfile = file_path_args[1]
	elif len(file_path_args) > 0:
		# convert arg into string
		fpath = ' '.join(file_path_args)
	else:
		print("Error: No input argument was supplied")
		exit()

	# get a list of the files inside the given directory
	# flist = os.listdir(fpath if len(file_path_args) > 0 else None)
	flist = os.listdir(fpath)

	# extract audio data from file list
	audio_data = get_track_data(flist, fpath)

	# output audio data to a csv file
	headers = ['name', 'size', 'duration', 'sample_rate']
	write_to_csv(headers, audio_data, outfile+'.csv' if len(file_path_args) == 2 else 'out.csv')

	# convert csv to excel file and open
	convert_csv_to_xlsx(outfile+'.csv' if len(file_path_args) == 2 else 'out.csv',
		outfile+'.xlsx' if len(file_path_args) == 2 else 'out.xlsx')
