import argparse
import os
import scipy.io.wavfile as wavfile
import numpy as np
import yaml
import warnings

from tqdm import tqdm
from audiomentations.augmentations.transforms import (
    ApplyImpulseResponse,
    FrequencyMask,
    Normalize,
    PitchShift,
)
from audiomentations.augmentations.transforms import LoudnessNormalization
from yaml.loader import SafeLoader
from audiomentations.core.audio_loading_utils import load_wav_file
from audiomentations.core.utils import convert_float_samples_to_int16
from audiomentations import Compose, AddImpulseResponse
from utils import (
    delete_folder,
    find_wav_files,
    get_basename,
    create_folder,
    copy_file,
    delete_folder,
)


warnings.filterwarnings("ignore")

def get_parser():
    parser = argparse.ArgumentParser(description="Audio Augmentations")
    parser.add_argument(
        "--audio_dir", type=str, default=None, help="path to your audio files directory"
    )
    parser.add_argument(
        "--output_dir", type=str, default=None, help="path to your output directory"
    )
    parser.add_argument(
        "--config_file",
        type=str,
        default=None,
        help="path to your augmentation configuration yaml",
    )
    parser.add_argument(
        "--target_sr", type=int, default=16000, help="target sampling rate output audio"
    )

    return parser


def create_ir_folders():
    INPUT_PATH = "ir_dict_2"
    OUTPUT_PATH = "ir_dict_out_2"
    create_folder(OUTPUT_PATH)
    list_ir = find_wav_files(INPUT_PATH)
    for ir in list_ir:
        folder_path = os.path.join(OUTPUT_PATH, ir[:-4])
        create_folder(folder_path)
        copy_file(os.path.join(INPUT_PATH, ir), os.path.join(folder_path, ir))


def main():
    args = get_parser().parse_args()
    wav_files = find_wav_files(args.audio_dir)

    print("\n\nWidya Audio Augmentations")
    print("Audio Directory : {}".format(args.audio_dir))
    print("Output Directory : {}".format(args.output_dir))
    print("Config File : {}".format(args.config_file))
    print("Target Sample Rate : {}".format(args.target_sr))

    create_folder(args.output_dir)

    with open(args.config_file) as config_file:
        config_data = yaml.load(config_file, Loader=SafeLoader)

    augmentation_effect = []

    conf_apply_ir = config_data["apply_impulse_response"]
    if conf_apply_ir["active"]:

        with open(conf_apply_ir["ir_conf"], "r") as ir_file:
            ir_list = ir_file.readlines()
            create_folder("ir_temporary")
            # delete_folder("ir_temporary")
            for ir in ir_list:
                source_path = os.path.join(conf_apply_ir["ir_audio_dict"], ir.strip())
                source_path = os.path.join(source_path, "{}.wav".format(ir.strip()))

                destination_path = os.path.join(
                    "ir_temporary", "{}.wav".format(ir.strip())
                )
                copy_file(source_path, destination_path)

        augmentation_effect.append(
            ApplyImpulseResponse(ir_path="ir_temporary", p=conf_apply_ir["probability"])
        )

    conf_normalize = config_data["normalize"]
    if conf_normalize["active"]:
        augmentation_effect.append(Normalize(p=conf_normalize["probability"]))

    conf_frequency_mask = config_data["frequency_mask"]
    if conf_frequency_mask["active"]:
        augmentation_effect.append(
            FrequencyMask(
                min_frequency_band=conf_frequency_mask["min_frequency_band"],
                max_frequency_band=conf_frequency_mask["max_frequency_band"],
                p=conf_frequency_mask["probability"],
            )
        )

    conf_loudness_normalization = config_data["loudness_normalization"]
    if conf_loudness_normalization["active"]:
        augmentation_effect.append(
            LoudnessNormalization(
                min_lufs_in_db=conf_loudness_normalization["min_lufs_in_db"],
                max_lufs_in_db=conf_loudness_normalization["max_lufs_in_db"],
                p=conf_loudness_normalization["probability"],
            )
        )

    conf_pitch_shift = config_data["pitch_shift"]
    if conf_pitch_shift["active"]:
        augmentation_effect.append(
            PitchShift(
                min_semitones=conf_pitch_shift["min_semitones"],
                max_semitones=conf_pitch_shift["max_semitones"],
                p=conf_pitch_shift["probability"],
            )
        )

    augment = Compose(augmentation_effect)

    for wav_file in tqdm(wav_files):
        wav_path = os.path.join(args.audio_dir, wav_file)
        raw_audio_data, sample_rate = load_wav_file(wav_path, args.target_sr, mono=True)
        aug_audio_data_float = augment(raw_audio_data, args.target_sr)

        basename = get_basename(wav_path)
        output_wav_path = os.path.join(args.output_dir, basename)

        aug_audio_data_pcm16 = convert_float_samples_to_int16(aug_audio_data_float)
        wavfile.write(
            output_wav_path,
            rate=args.target_sr,
            data=aug_audio_data_pcm16.astype(np.int16),
        )
    
    delete_folder("ir_temporary")


if __name__ == "__main__":
    main()