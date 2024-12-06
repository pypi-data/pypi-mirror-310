# Demucs Acapella

`demucs_acapella` is a Python package that extracts vocals (acapella) from audio files using the Demucs model and embeds the key and BPM into the metadata of the output files.

## Features

- Extracts vocals (acapella) from audio files.
- Automatically embeds the detected key and BPM into the metadata of the output files.
- Supports various audio formats including `.mp3`, `.wav`, and `.flac`.
- Can be used from the command line or as a Python package.

## Installation

### From PyPI

You can install the `demucs_acapella` package directly from PyPI:

```
pip install demucs_acapella
```

### From Source

To install from source, clone the repository and install the dependencies:

```
git clone https://github.com/yourusername/demucs_acapella.git
cd demucs_acapella
pip install -r requirements.txt
```

## Dependencies

- `demucs`: For the deep learning model to extract vocals.
- `pydub`: For audio file manipulation.
- `tinytag`: For extracting BPM from audio files.
- `eyed3`: For modifying MP3 metadata.

You can install the necessary dependencies by running:

```
pip install -r requirements.txt
```

## Usage

### Command Line Interface (CLI)

To run the package and extract vocals from your audio files, use the following command:

```
demucs_acapella -i /path/to/input/folder -o /path/to/output/folder
```

#### Arguments

- `-i, --input`: Path to the input directory containing audio files. It will recursively search for audio files.
- `-o, --output`: Path to the output directory where acapella files will be stored.

### Example

```
demucs_acapella -i /path/to/your/audio/files -o /path/to/output/folder
```

This will:

1. Extract vocals from the audio files found in `/path/to/your/audio/files`.
2. Save the vocals in the `/path/to/output/folder` directory, preserving the original folder structure.

### Embedding Key and BPM Metadata

After the vocals are extracted, the script can automatically embed the key and BPM information into the metadata of the output files.

### Running from Python Script

You can also use the package programmatically in your Python code:

```
from demucs_acapella import extract_vocals

input_file = '/path/to/audio/file.mp3'
output_folder = '/path/to/output/folder'
vocals_file = extract_vocals(input_file, output_folder)

if vocals_file:
    print(f"Extracted vocals saved to {vocals_file}")
else:
    print("Failed to extract vocals.")
```

## Examples

### Example 1: CLI extraction

Run the following command to extract acapella from an entire folder of audio files:

```
demucs_acapella -i /path/to/input/folder -o /path/to/output/folder
```

This will process all supported audio files (such as `.mp3`, `.wav`, and `.flac`) inside the input folder and save the extracted acapella versions in the output folder.

### Example 2: Programmatic Usage

You can call `extract_vocals` from your Python script to extract vocals for a specific audio file:

```
from demucs_acapella import extract_vocals

vocals_file = extract_vocals('path/to/input/file.mp3', 'path/to/output/folder')
if vocals_file:
    print(f"Vocals saved to {vocals_file}")
else:
    print("Error extracting vocals.")
```

## License

`demucs_acapella` is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgements

- [Demucs](https://github.com/facebookresearch/demucs) for the deep learning model to separate vocals.
- [pydub](https://github.com/jiaaro/pydub) for audio file manipulation.
- [eyed3](https://github.com/mik3y/eyed3) for modifying MP3 metadata.

## Contributing

Feel free to open an issue or submit a pull request if you'd like to contribute to this project.
