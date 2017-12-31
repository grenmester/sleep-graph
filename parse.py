#!/usr/bin/env python
import datetime

def computeIntervals():
    sourceFile = "bullet.md"
    dataFile = "output.md"

    with open(sourceFile, "r") as source:
        lines = source.readlines()

        for line in lines:

            if line[0] == "#":
                with open(dataFile, "a") as data:
                    data.write(line)

            if "* sleep" in line or "* nap" in line:
                line = line.replace("* sleep ","").replace("* nap ","")
                dashPos = line.find("-")
                firstDate = line[:dashPos]+"\n"
                secondDate = line[dashPos+2:]
                with open(dataFile, "a") as data:
                    data.write(firstDate)
                    data.write(secondDate)

