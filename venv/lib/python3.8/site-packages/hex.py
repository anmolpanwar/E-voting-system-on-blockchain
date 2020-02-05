#!/usr/bin/env python3
# ------------------------------------------------------------------------------
# Hexdump command line utility. Requires Python 3.
#
# Author: Darren Mulholland <darren@mulholland.xyz>
# License: Public Domain
# ------------------------------------------------------------------------------

import argparse
import os
import signal
import sys
import shutil


# Application version number.
__version__ = '2.2.0'


# Command line help text.
helptext = """
Usage: %s [FLAGS] [OPTIONS] [ARGUMENTS]

  Hexdump utility.

Arguments:
  [file]                File to dump. Defaults to reading from stdin.

Options:
  -l, --line <int>      Bytes per line in output (default: 16).
  -n, --number <int>    Number of bytes to read.
  -o, --offset <int>    Byte offset at which to begin reading.
  -w, --width <int>     Line number width (default: 6).

Flags:
  -h, --help            Display this help text and exit.
  -v, --version         Display version number and exit.

""" % os.path.basename(sys.argv[0])


# Custom argparse 'action' to print our own help text instead of the default.
class HelpAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        print(helptext.strip())
        sys.exit()


# Suppress 'broken pipe' warnings when piping output through pagers.
# This resolves the issue when running under Cygwin on Windows.
if hasattr(signal, 'SIGPIPE'):
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)


# Wrapper for the sys.stdout.write() function.
def write(s):
    # Suppress 'broken pipe' warnings when piping output through pagers.
    # This resolves the issue when running natively on Windows.
    try:
        sys.stdout.write(s)
    except (IOError, OSError):
        sys.exit()


# Print a single line of output to stdout.
def writeln(offset, buffer, bytes_per_line, line_num_width):

    # Write the line number.
    write('% *X \u001B[90m│\u001B[0m' % (line_num_width, offset))

    for i in range(bytes_per_line):

        # Write an extra space in front of every fourth byte except the first.
        if i > 0 and i % 4 == 0:
            write(' ')

        # Write the byte in hex form, or a spacer if we're out of bytes.
        write(' %02X' % buffer[i] if i < len(buffer) else '   ')

    write('\u001B[90m │ \u001B[0m')

    # Write a character for each byte in the printable ascii range.
    for i in range(len(buffer)):
        nonprintable = '\u001B[90m·\u001B[0m'
        write('%c' % buffer[i] if 32 <= buffer[i] <= 126 else nonprintable)

    write('\n')


# Dump the specified file to stdout.
def dump(file, offset, bytes_to_read, bytes_per_line, line_num_width):

    # If an offset has been specified, attempt to seek to it.
    if offset:
        if file.seekable():
            file.seek(offset)
        else:
            sys.exit('Error: %s is not seekable.' % file.name)

    # Print a line.
    cols, _ = shutil.get_terminal_size()
    print('\u001B[90m' + '─' * cols + '\u001B[0m')

    # Read and dump one line per iteration.
    while True:

        # If bytes_to_read < 0 (read all), try to read one full line.
        if bytes_to_read < 0:
            max_bytes = bytes_per_line

        # Else if line length < bytes_to_read, try to read one full line.
        elif bytes_per_line < bytes_to_read:
            max_bytes = bytes_per_line

        # Otherwise, try to read all the remaining bytes in one go.
        else:
            max_bytes = bytes_to_read

        # Attempt to read up to max_bytes from the file.
        buffer = file.read(max_bytes)

        # A buffer length of zero means we're done.
        if len(buffer):
            writeln(offset, buffer, bytes_per_line, line_num_width)
            offset += len(buffer)
            bytes_to_read -= len(buffer)
        else:
            break

    print('\u001B[90m' + '─' * cols + '\u001B[0m')


def main():

    # Setting add_help to false prevents the parser from automatically
    # generating a -h flag.
    parser = argparse.ArgumentParser(add_help=False)

    # The filename argument is optional. We default to reading from
    # stdin if it's omitted.
    parser.add_argument('file',
        nargs='?',
        help='file to dump (default: stdin)',
        type=argparse.FileType('rb'),
        default=sys.stdin.buffer,
    )

    # Flags.
    parser.add_argument('-h', '--help',
        action = HelpAction,
        nargs=0,
        help = 'print this help message and exit',
    )
    parser.add_argument('-v', '--version',
        action='version',
        version=__version__,
    )

    # Options.
    parser.add_argument('-l', '--line',
        help='bytes per line in output (default: 16)',
        default=16,
        type=int,
        dest='bpl',
    )
    parser.add_argument('-n', '--number',
        nargs='?',
        help='number of bytes to read (default: 256)',
        type=int,
        default=-1,
        const=256,
        dest='btr',
    )
    parser.add_argument('-o', '--offset',
        help='offset at which to begin reading (default: 0)',
        type=int,
        default=0,
        dest='offset',
    )
    parser.add_argument('-w', '--width',
        help='line number width (default: 6)',
        type=int,
        default=6,
        dest='num_width',
    )

    args = parser.parse_args()
    dump(args.file, args.offset, args.btr, args.bpl, args.num_width)


if __name__ == '__main__':
    main()
