#!/usr/bin/env python

sourceFile = "bullet.md"
dataFile = "output.md"

with open(sourceFile, "r") as source:
    lines = source.readlines()

    for line in lines:
        if line[0] == "#" or "* sleep" in line or "* nap" in line:
            with open(dataFile, "a") as data:
                data.write(line)
