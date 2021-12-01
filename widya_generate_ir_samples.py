import argparse
import os
import scipy.io.wavfile as wavfile
import warnings

from tqdm import tqdm
from audiomentations.core.utils import convert_float_samples_to_int16
from audiomentations.augmentations.transforms import ApplyImpulseResponse
from audiomentations.core.audio_loading_utils import load_wav_file
from audiomentations import Compose
from utils import find_wav_files, get_basename, create_folder, copy_file

warnings.filterwarnings("ignore")


def get_parser():
    parser = argparse.ArgumentParser(
        description="generate audio samples for each ir sound"
    )
    parser.add_argument(
        "--audio_dir", type=str, default=None, help="path to your audio files directory"
    )
    parser.add_argument(
        "--output_dir", type=str, default=None, help="path to your output directory"
    )
    parser.add_argument(
        "--ir_path", type=str, default=None, help="impulse response type"
    )
    parser.add_argument(
        "--target_sr", type=int, default=16000, help="target sampling rate output audio"
    )

    return parser


def main():
    args = get_parser().parse_args()

    print("\n\nWidya Generate IR Samples")
    print("Audio Directory : {}".format(args.audio_dir))
    print("Output Directory : {}".format(args.output_dir))
    print("IR Audio Directory : {}".format(args.ir_path))
    print("Target Sample Rate : {}".format(args.target_sr))

    ir_list = os.listdir(args.ir_path)
    create_folder(args.output_dir)

    for ir in tqdm(ir_list):
        ir_path = os.path.join(args.ir_path, ir)
        wav_files = find_wav_files(args.audio_dir)
        augment = Compose([ApplyImpulseResponse(ir_path=ir_path, p=1)])

        output_ir_path = os.path.join(args.output_dir, ir)
        create_folder(output_ir_path)

        for wav_file in wav_files:
            wav_path = os.path.join(args.audio_dir, wav_file)
            raw_audio_data, sample_rate = load_wav_file(
                wav_path, args.target_sr, mono=True
            )
            aug_audio_data_float = augment(raw_audio_data, args.target_sr)

            aug_audio_data_pcm16 = convert_float_samples_to_int16(aug_audio_data_float)

            basename = get_basename(wav_path)
            output_wav_path = os.path.join(output_ir_path, basename)

            wavfile.write(
                output_wav_path, rate=args.target_sr, data=aug_audio_data_pcm16
            )


if __name__ == "__main__":
    main()
