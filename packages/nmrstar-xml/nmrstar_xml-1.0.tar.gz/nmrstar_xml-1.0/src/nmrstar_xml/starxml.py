#!/usr/bin/env python3
import argparse

from nmrstar_xml import Translator


def main( ):
    parser = argparse.ArgumentParser(description="Translate NMR-STAR file to XML" )
    parser.add_argument('-i','--input',help="NMR-STAR input file (default stdin)")
    parser.add_argument('-o','--output',help="XML output file (default stdout)")
    parser.add_argument('--starxml',action='store_true',help=argparse.SUPPRESS) #only used for test call
    args = parser.parse_args()
    with Translator(args.input,args.output) as tr:
        tr.star_translate()

if __name__ == "__main__":
    main()
