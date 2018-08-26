#! /usr/bin/env python
## vim:set ts=4 sw=4 et: -*- coding: utf-8 -*-
#
#
# Find all the whitespace format issues in the source
# 1.) No trailing whitespace
# 2.) No tab indentation
# 3.) Nor CR/LF or LF/CR lineendings
#
# sample run:
# find .. -type f -name '*.cpp' -print0 -name '*.h' -print0 | xargs -r0 ./check_code_format.py

import getopt, os, re, sys

class opts:
    verbose = 1
    recursive = False
    warn = False


class globs:
    whitespace_on_line_end = re.compile("[ \t\f\v][\r\n]")
    tab_indent = re.compile("^\t", re.MULTILINE)
    crlf_lineend = re.compile("\r\n") # windows
    cr_lineend = re.compile("\r") # classicc MAC
    binary = re.compile("[\x00\x01\x02\xfe\xff]") # some binary


# try to find a correct linenumber - even if lines are CR/LF, CR or LF terminated
def determine_linenumber(data, pos):
    lineend = "\n"

    crlf = data.find("\r\n")
    if crlf != -1:
        lineend = "\r\n"
    else:
        cr = data.find("\r")
        if cr != -1:
            lineend = "\r"

    line = 1
    p = 0
    while True:
        p = data.find(lineend, p)
        if p == -1:
            return line
        if p >= pos:
            return line
        line += 1
        p += len(lineend)


def print_error(filename, data, errorposition, errormessage):
    if opts.warn:
        m = "Warning:"
    else:
        m = "Error:"
    linenumber = determine_linenumber(data, errorposition)
    print m, filename, errormessage + " (line %d)" % linenumber
    # we could make an early exit here


def do_one_file(filename):
    r = 0
    if opts.verbose >= 3:
        print "checking", filename

    fp = open(filename, "rb")
    data = fp.read()
    fp.close()

    if globs.binary.search(data):
        if opts.verbose >= 2:
            print filename, " is a binary"
        return r

    tab_indent = globs.tab_indent.search(data)
    if tab_indent:
        r = 1
        if opts.verbose > 0:
            print_error(filename, data, tab_indent.start(), "contains tab indent")

    crlf = globs.crlf_lineend.search(data)
    cr = globs.cr_lineend.search(data)
    if crlf or cr:
        r = 1
        if crlf and cr:
            if crlf.start() <= cr.start():
                cr = None
            else:
                crlf = None
        if crlf:
            if opts.verbose > 0:
                print_error(filename, data, crlf.start(), "contains CR/LF linefeed")
        else:
            if opts.verbose > 0:
                print_error(filename, data, cr.start(), "contains CR linefeed")

    whitespace_on_line_end = globs.whitespace_on_line_end.search(data)
    if whitespace_on_line_end:
        if filename.endswith(".md"):
            pass # currently skip .md files
        else:
            r = 1
            if opts.verbose > 0:
                print_error(filename, data, whitespace_on_line_end.start(), "contains whitespaces at the line end")

    return r


def do_one_directory(directory):
    r = 0

    for root, dirs, files in os.walk(directory, topdown=True):
        for name in files:
            #print(os.path.join(root, name))
            if do_one_file(os.path.join(root, name)):
                r = 1
        if not opts.recursive:
            break
    return r


def display_usage(argv):
    print "USAGE: %s -a arch [options] file" % os.path.basename(argv[0])
    print "  -v, --verbose                  increase logging level"
    print "  -q, --quiet                    decrease logging level"
    print "  -h, --help                     display this page"
    print
    print "  -r, --recursive                if given a directory check all recursive"
    print "  -w, --warn                     just warn, don't exit with an error"


def main(argv):
    try: assert 0
    except AssertionError: pass
    else: raise Exception("fatal error - assertions not enabled")
    shortopts, longopts = "hqvrw", [
        "help", "quiet","verbose",
        "recusrive", "warn",
    ]
    xopts, args = getopt.gnu_getopt(argv[1:], shortopts, longopts)
    for opt, optarg in xopts:
        if opt in ["-q", "--quiet"]:
            opts.verbose = opts.verbose - 1
        elif opt in ["-v", "--verbose"]:
            opts.verbose = opts.verbose + 1
        elif opt in ["-h", "--help"]:
            display_usage(argv)
            return 0
        elif opt in ["-r", "--recursive"]:
            opts.recursive = True
        elif opt in ["-w", "--warn"]:
            opts.warn = True

    if not args:
        r = do_one_directory(".")
    else:
        r = 0
        for arg in args:
            if os.path.isdir(arg):
                if do_one_directory(arg):
                    r = 1
            else:
                if do_one_file(arg):
                    r = 1

    if opts.warn:
        return 0
    return r


if __name__ == "__main__":
    sys.exit(main(sys.argv))
