import argparse


parser = argparse.ArgumentParser(description='Compiler from C like language to Mindustry assembler.')
parser.add_argument('--config', action='store', type=str, help='path where config file is located.', metavar='PATH')
