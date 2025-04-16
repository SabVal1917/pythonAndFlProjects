#!/bin/python

from src.launcher import ConsoleLauncher
import sys

if __name__ == "__main__":
    launcher = ConsoleLauncher()
    try:
        launcher.start()
    except:
        sys.exit(0)
