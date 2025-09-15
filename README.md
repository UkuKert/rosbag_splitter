# Rosbag splitter
Pure python script to easily split rosbag from commandline.
This script is made to cut rosbags without having to install ros and also to allow cutting bags without knowing the UNIX timestamps of the starting and end times.
## Requirements
The requirements are managed by poetry and can be seen in the `pyproject.toml` file. To install the dependencies, [install poetry](https://python-poetry.org/docs/#installing-with-the-official-installer) and then run
```bash
git clone https://github.com/UkuKert/rosbag_splitter.git 
cd rosbag_splitter
sudo apt update && sudo apt install liblz4-dev
poetry install 
```
## Usage

The following example takes a bag called "input_bag.bag" as an input and makes a 5 second small bag from 20s - 25s and saves that to "small_bag.bag".
**Note** The input bag is preserved.
```bash
poetry run python3  rosbag_splitter.py  -i  input_bag.bag -o small_bag.bag -b 20 -e 25
```

The following example takes a bag called "input_bag.bag" as an input and saves the first 25 seconds of it to "input_bag_cut.bag".
**Note** When begin time is not specified it is assumed to be 0. When output bag is not specified a new name is created with the suffix "_cut" added to the input bag path root.
```bash
poetry run python3  rosbag_splitter.py -i input_bag.bag -e 25
```
For more help run the script with the argument "-h"

```bash
poetry run python3  rosbag_splitter.py  rosbag_splitter.py -h
```

## Development

We are using RUFF for static formatting and linting. Use the `Makefile` to run the linter and formatter:

```bash
make fmt
make lint
```
