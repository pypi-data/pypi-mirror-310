# SidTools

SidTools is a Python package for splitting `.xyz` files into individual trajectories and organizing them into directories.

## Installation

```bash
pip install .
```

## Usage

Use the `s_make` command to process your `.xyz` files:

```bash
s_make -T input.xyz --base output_directory
```

### Options:
- `-T`, `--trajectory`: Path to the input `.xyz` file.
- `--base`: Name of the base directory to create.
- `-F`, `--files`: Optional. List of files/folders to copy into each trajectory directory.
