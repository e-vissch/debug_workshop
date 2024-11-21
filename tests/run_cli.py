import sys
from bin.cli import main


def run_whole_model(command_line_args):
    main(command_line_args)
    

if __name__ == "__main__":
    run_whole_model(sys.argv[1:])