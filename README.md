

<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/rahmadai/Widya-Audio-Augmentation">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Widya Wicara Audio Augmentaton</h3>

  <p align="center">
    Audio Augmentation for STT or WakeWord
    <br />
<!--     <a href="https://github.com/rahmadai/Widya-Audio-Augmentation"><strong>Explore the docs »</strong></a> -->
    <br />
    <br />
    <a href="https://colab.research.google.com/drive/12bomPPjC8Jjp0bEH0VDl1nTrXBuJif5I?usp=sharing">View Demo</a>
    <!-- ·
    <a href="https://github.com/rahmadai/Widya-Audio-Augmentation">Report Bug</a>
    ·
    <a href="https://github.com/rahmadai/Widya-Audio-Augmentation">Request Feature</a> -->
  </p>
</p>

<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

Use miniconda to isolated the environment
* <a href="https://conda.io/projects/conda/en/latest/user-guide/install/index.html#regular-installation">Install Miniconda</a>
* Create new environment with python 3.7
  ```sh
  conda create --name widya_audio_augmentation python=3.7
  ```
  
* Activate the new environment 
  ```sh
  conda activate widya_audio_augmentation
  ```
### Installation
 1. Clone repo
  ```sh
  git clone https://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@github.com/rahmadai/Widya-Audio-Augmentation.git
  ```
 2. Install package & depedencies
  ```sh
  cd Widya-Audio-Augmentation
  pip install -r requirements.txt 
  ```


  
## Usage
### Audio augmentation
Here is how to use this audio augmentations
1. First, your audio files need to be stored in a folder. For this example we will augmentaton three audios in **samples/** directory.
2. Then, Use **conf.yaml** to change configuration that will be used for augmentation process.<br />
 ##### conf.yaml
 ```sh
  name: widya audio augmentation configuration

  apply_impulse_response:
    #Convolve the audio with a random impulse response
    active: True
    ir_conf: ir_config/echo.txt
    ir_audio_dict: ir_audio
    probability: 1

  normalize:
    #Apply a constant amount of gain, so that highest signal level present in the 
    #sound becomes 0 dBFS, i.e. the loudest level allowed if all samples must be 
    #between -1 and 1. Also known as peak normalization.
    active: False
    probability: 1


  frequency_mask:
    #Mask some frequency band on the spectrogram. 
    #Inspired by https://arxiv.org/pdf/1904.08779.pdf
    active: False
    min_frequency_band: 0.5
    max_frequency_band: 0.6
    probability: 1

  loudness_normalization:
    #Apply a constant amount of gain to match a specific loudness. 
    #This is an implementation of ITU-R BS.1770-4.
    #Warning: This transform can return samples outside the [-1, 1] range, 
    #which may lead to clipping or wrap distortion, depending on what you do 
    #with the audio in a later stage
    active: False
    min_lufs_in_db : -31
    max_lufs_in_db : -13
    probability : 0.5

  pitch_shift:
    #Pitch shift the sound up or down without changing the tempo
    active: False
    min_semitones: -4
    max_semitones: -4
    probability : 1
 ```
  In **conf.yaml** you can change the effect that will applied for augmentation such as impulse response, normalize, freqeuency mask, loudness normalization and     pitch shift. You can also change parameters for each effect based on your needs.
  
  3.  Use this script below to process augmentations. **--audio_dir** is your audio files directory path, **--output_dir** is your output augmented audio files   directory path, **--config_file** is augmentation configuration file (in this case we used **conf.yaml**) path and **--target_sr** is sampling rate output parameter.
   ```sh
   python widya_audio_augmentations.py --audio_dir samples --output_dir out_test --config conf.yaml --target_sr 16000
   ```
### Change IR Effect
In the example above we applied **impulse response** and the effect of impulse response defined by **ir_conf** parameters that reference to **ir_config/echo.txt**. <br />
##### ir_config/echo.txt
```sh
h252_Auditorium_1txts
h251_Hallway_MITCampus_1txts
```
You can change effect of impulse response by change **ir_conf** parameters and reference it to ir_config file (.txt) path. We provided four example of inf_config in **ir_config/**. If you wanna create your own ir_config file just create txt file and insert all of ir effect names that will be used (directory name inside **ir_audios/**). If you wanna heard the effect of each ir effect, you can follow step below to create augmented audio samples for all of impulse response effect. 
### Generate audio samples for each impulse response effect
  ```sh
  python widya_generate_ir_samples.py --audio_dir samples --output_dir ir_output_samples --ir_path ir_audio --target_sr 16000
  ```
  With those script it will generated audio samples for each impulse response effect
  
  ```sh
  tree ir_output_samples/
  ```
  Output Directory
  ```sh
  ir_output_samples/
  ├── air_booth_0_0_1
  │   ├── sample_1.wav
  │   ├── sample_2.wav
  │   └── sample_3.wav
  ├── air_booth_0_0_2
  │   ├── sample_1.wav
  │   ├── sample_2.wav
  │   └── sample_3.wav
  ├── air_booth_0_0_3
  │   ├── sample_1.wav
  │   ├── sample_2.wav
  │   └── sample_3.wav
  ├── air_booth_0_1_1
  │   ├── sample_1.wav
  │   ├── sample_2.wav
  │   └── sample_3.wav
  ├── air_booth_0_1_2
  │   ├── sample_1.wav
  │   ├── sample_2.wav
  │   └── sample_3.wav
  .
  .
  ├── h267_MITCampus_Atrium_1txts
  │   ├── sample_1.wav
  │   ├── sample_2.wav
  │   └── sample_3.wav
  ├── h268_BasementOfSuburbanHome_1txts
  │   ├── sample_1.wav
  │   ├── sample_2.wav
  │   └── sample_3.wav
  ├── h269_Office_ConferenceRoom_1txts
  │   ├── sample_1.wav
  │   ├── sample_2.wav
  │   └── sample_3.wav
  ├── h270_Hallway_House_1txts
  │   ├── sample_1.wav
  │   ├── sample_2.wav
  │   └── sample_3.wav
  └── h271_Outside_InTramStopRainShelter_2txts
      ├── sample_1.wav
      ├── sample_2.wav
      └── sample_3.wav
  ```
  

<!-- LICENSE -->
## License
Copyright (C) Widya Wicara, Inc - All Rights Reserved </br>
For internal use only </br>
Written by Rahmad Kurniawan & Ilham Fazri, 2021

<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements
* [Audiomentations](https://github.com/iver56/audiomentations)
* [MIT Acoustical Reverberation Scene Statistics Survey](https://mcdermottlab.mit.edu/Reverb/IR_Survey.html)
* [Aachen Impulse Response Database](https://www.openslr.org/20/)

