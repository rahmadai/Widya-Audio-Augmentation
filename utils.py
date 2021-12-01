import os
import shutil


def find_wav_files(audio_dir):
    files = os.listdir(audio_dir)
    wav_files = []
    for file in files:
        if file[-4:] == ".WAV" or file[-4:] == ".wav":
            wav_files.append(file)
    return wav_files


def get_basename(path):
    basename = os.path.basename(path)
    return basename


def create_folder(path):
    dir = path
    check = os.path.isdir(dir)

    if not check:
        os.makedirs(dir)


def delete_folder(path):
    dir = path
    check = os.path.isdir(path)

    if check:
        shutil.rmtree(path)


def copy_file(source_path, destination_path):
    shutil.copyfile(source_path, destination_path)
