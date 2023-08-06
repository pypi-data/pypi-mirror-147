#!/bin/env python3
import os
import sys
import argparse
from .extract_links import extract_links
from .check import check_locations
from .sort_result import sort_result
from .diff_results import diff_results
from .visualize import visualize
from urllib.parse import urlparse

def link(subparsers):
    links_parser = subparsers.add_parser("link", help="Tools to maintain the links on a website")

    formats = ["csv", "yaml", "yml", "json"]
    links_parser.add_argument("--format", "-f", help="Format to expect for input and output (is overwritten by in-format and out-format", choices=formats, default="json")
    links_parser.add_argument("--in-format", "-in-f", help="Format to expect from input only", choices=formats)
    links_parser.add_argument("--out-format", "-out-f", help="Format to use for output only", choices=formats)

    subparsers = links_parser.add_subparsers()

    # check
    check_parser = subparsers.add_parser("check", help="Check all the locations in the locations for their reachability, latency and status")
    check_parser.add_argument("locations", help="File of the locations to check")
    check_parser.add_argument("--num-processes", "-j",
                              type=int,
                              default=6,
                              help="Number of processes to run in parallel")
    check_parser.add_argument("--estimate-total", "-t",
                              type=int,
                              default=None,
                              help="Estimated number of total sites that'll be checked. Useful for nice progress bars")
    check_parser.set_defaults(func=check_locations)

    # sort
    sort_parser = subparsers.add_parser("sort", help="Sort the results from check according to some options")
    sort_parser.add_argument("filename",
                             help="Filename of the result",
                             default="-")
    sort_parser.add_argument("--ok",
                             action=argparse.BooleanOptionalAction,
                             help="Only return entries where the status was ok")
    sort_parser.add_argument("--status-code", "-s",
                             type=int,
                             help="Only return entries where the status code was this")
    sort_parser.add_argument("--latency", "-l",
                             type=float,
                             help="Only return entries where the latency was larger than this")
    sort_parser.add_argument("--error", "-e",
                             action=argparse.BooleanOptionalAction,
                             help="Only return entries where an error has occured")
    sort_parser.set_defaults(func=sort_result)

    # diff
    diff_parser = subparsers.add_parser("diff", help="Take the difference between two check results")
    diff_parser.add_argument("filename_a",
                             help="Filename of the first file. Cannot be - for stdin.")
    diff_parser.add_argument("filename_b",
                             help="Filename of the second file. Can be - for stdin.")
    diff_parser.set_defaults(func=diff_results)

    # visualize
    visualize_parser = subparsers.add_parser("visualize", help="Visualize the results of a page as a graph stored in a static HTML.")
    visualize_parser.add_argument("filename",
                                  default="-",
                                  help="Filename of the result")
    visualize_parser.add_argument("--output-filename", "-o",
                                  help="Filename to store the static HTML File in")
    visualize_parser.set_defaults(func=visualize)
