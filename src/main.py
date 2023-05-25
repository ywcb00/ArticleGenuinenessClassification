#!/usr/bin/env python3

from Collector import Collector
import getopt
import sys

def main(argv):
    collector = Collector()

    try:
        opts, args = getopt.getopt(argv[1:], "hu:", ["help", "update"])
    except getopt.GetoptError:
        print("Wrong usage.")
        print("Usage:", argv[0], "[--update]")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-u", "--update"):
            collector.updateRoutine()
            sys.exit(0)

    collector.collectionRoutine()

if __name__ == '__main__':
    main(sys.argv)
