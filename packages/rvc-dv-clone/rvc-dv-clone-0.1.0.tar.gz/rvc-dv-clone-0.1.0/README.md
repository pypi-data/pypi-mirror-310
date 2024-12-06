# RVC Convert

A Python package for Retrieval-based Voice Conversion, based on the [RVC-Project](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI).

## Installation

```bash
pip install rvc-convert
```
## Usage

```python
python
from rvc import rvc_convert
Convert voice using a pre-trained model
output_path = rvc_convert(
model_path="path/to/model.pth",
input_path="input.wav",
f0_up_key=0 # Pitch shift (semitones)
)
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.