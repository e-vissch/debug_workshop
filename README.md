# SER
Software Engineering for Research, originally from cvanea's: https://github.com/cvanea/ser/ for the CDT for Health Data Science software engineering module.

## Installation
```bash
conda create -n ser python=3.9
conda activate ser
pip install -e .
```

## PyTorch dependencies

There are instructions on the PyTorch website how to install the PyTorch versions that are correct for your system...

https://pytorch.org/get-started/locally/

Ideally install using pip.

## Startup
```bash
conda activate ser
``` 

## Run SER
```bash
ser --help
``` 

## Use the debugger to find the issues

Run run_cli.py with debug config "run_cli_train" or try "Python Debugger: Current File with Arguments" to define your own entry to cli.py.


You can also try running jupyter_eg.ipynb to try debugging in jupyter. 

- Note usually would add ".vscode" to .gitignore so not uploaded to repoitory as your personal config.