#!/usr/bin/env python
import datetime
import dateutil
import dateutil.parser

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

def computeDailyTime():
    with open("bullet.md", "r") as source:
        lines = source.readlines()[:160]

        for line in lines:
            # Identity dates
            if line[0] == "#":
                date = line[2:-1]
            # Identity and parse times
            elif "* sleep" in line or "* nap" in line:
                chunks = line.split()
                time1 = date + " " + chunks[2] + " " + chunks[3]
                time2 = date + " " + chunks[5] + " " + chunks[6]

                #print("time1: " + str(time1))
                #print("time2: " + str(time2))

                diff = dateutil.parser.parse(time2) - dateutil.parser.parse(time1)
                #print("diff: " + str(diff))

                hours = str(diff).split(':')
                hours = int(hours[0]) * 4 + int(hours[1]) / 15
                #print("hours: " + str(hours))

                with open("time-output.md", "a") as data:
                    data.write(time1 + " - " + time2)
                    data.write('\n')
                    data.write(str(hours))
                    data.write('\n')

# TODO: account for periods spanning two days
# TODO: get list of days with hours asleep

if __name__ == "__main__":
  computeDailyTime()
