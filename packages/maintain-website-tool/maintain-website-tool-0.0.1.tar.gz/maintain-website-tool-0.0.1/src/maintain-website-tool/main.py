#!/bin/env python3
from link import link
import argparse

def main():
    parser = argparse.ArgumentParser(prog="maintain-website-tool")
    parser.set_defaults(func=lambda args: parser.print_usage())

    subparsers = parser.add_subparsers()

    # Init subcommands
    link(subparsers)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
