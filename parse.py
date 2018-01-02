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
    with open("time-output.md", "w") as data:
        data.write("date,time\n")
    with open("bullet.md", "r") as source:
        # FIXME: use all data after testing
        lines = source.readlines()

        sleepHours = 0
        carryHours = 0
        firstPass = True

        for line in lines:
            if line[0] == "#":
                date = line[2:-7] # EX: Jun 2
                with open("time-output.md", "a") as data:
                    if firstPass:
                        firstPass = False
                        data.write(date + ",")
                    else:
                        data.write(str(sleepHours/4.0) + "\n" + date + ",")
                sleepHours = carryHours # reset hours
                carryHours = 0
            elif "* sleep" in line or "* nap" in line:
                chunks = line.split()
                time1 = chunks[2] + " " + chunks[3]
                time2 = chunks[5] + " " + chunks[6]
                # spans two days
                if dateutil.parser.parse(time1) > dateutil.parser.parse(time2):
                    #print("two dates from " + date)
                    diff = dateutil.parser.parse("12:00 am") - (dateutil.parser.parse(time1) + dateutil.relativedelta.relativedelta(days=-1))
                    hours = str(diff).split(':')
                    hours = int(hours[0]) * 4 + int(hours[1]) / 15
                    #print("time1: " + str(time1))
                    #print("hours: " + str(hours))
                    sleepHours += hours

                    carryDiff = dateutil.parser.parse(time2) - dateutil.parser.parse("12:00 am")
                    carryHours = str(carryDiff).split(':')
                    carryHours = int(carryHours[0]) * 4 + int(carryHours[1]) / 15
                    #print("time2: " + str(time2))
                    #print("carry-hours: " + str(carryHours))
                else:
                    #print("same date from " + date)
                    diff = dateutil.parser.parse(time2) - dateutil.parser.parse(time1)
                    # add new hours to running total
                    hours = str(diff).split(':')
                    hours = int(hours[0]) * 4 + int(hours[1]) / 15
                    #print("hours: " + str(hours))
                    sleepHours += hours

    with open("time-output.md", "a") as data:
        data.write(str(sleepHours/4.0) + "\n")

if __name__ == "__main__":
  computeDailyTime()
