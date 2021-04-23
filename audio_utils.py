# class Utils:
from os import path
from os import mkdir

def strip_extension(filename):
	return filename[:len(filename)-4]


def add_extension(filename, extension: str):
	return filename + '.' + extension


# Checks if directory exists. If not, makes it
def create_dir_if_none(dir):
	if not path.exists(dir):
		mkdir(dir)


def convert_seconds_to_minutes(seconds):
	mins = seconds / 60
	secs = seconds % 60
	return "%02d:%02d" % (mins, secs)


def convert_bytes_to_megabytes(bytes):
	return '{:.1f} MB'.format(bytes * 0.000001)
