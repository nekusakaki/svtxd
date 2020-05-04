from datetime import datetime



class StopWatch(object):
    def __init__(self, fhandle):
        self.fhandle = fhandle

    def readTimes(self):
        print('\nStart Time\t\tStop Time\t\tElapse Time')
        print('=' * 70 + '\n')
        self.fhandle.seek(0, 0)
        for line in self.fhandle:
            print(line)

        print('\n')

    def startTime(self):
        self.startTime = datetime.now()

    def stopTime(self):
        self.stopTime = datetime.now()
        self.elapseTime = self.stopTime - self.startTime
        print("Start Time:  " + str(self.startTime.hour).zfill(2) + ":" +
              str(self.startTime.minute).zfill(2) + ":" +
              str(self.startTime.second).zfill(2) + "." +
              str(self.startTime.microsecond))
        print("Stop Time:   " + str(self.stopTime.hour).zfill(2) + ":" +
              str(self.stopTime.minute).zfill(2) + ":" +
              str(self.stopTime.second).zfill(2) + "." +
              str(self.stopTime.microsecond))
        print("Elap. Time:  %s" % self.elapseTime)
        self.fhandle.write(str(self.startTime.hour).zfill(2) + ":" +
                           str(self.startTime.minute).zfill(2) + ":" +
                           str(self.startTime.second).zfill(2) + "." +
                           str(self.startTime.microsecond) + '\t\t' +
                           str(self.stopTime.hour).zfill(2) + ":" +
                           str(self.stopTime.minute).zfill(2) + ":" +
                           str(self.stopTime.second).zfill(2) + "." +
                           str(self.stopTime.microsecond) +
                           '\t\t' + str(self.elapseTime) + '\n')

    def closeFile(self):
        self.fhandle.close()


def main():
    newSession = StopWatch(open('stopWatchTimes.txt', 'a+'))
    newSession.readTimes()
    signalStart = input("Press ENTER to start.")
    newSession.startTime()
    print("\n**Stopwatch Starting...**\n")
    signalStop = input("Press ENTER to stop.")
    print("\n")
    newSession.stopTime()
    newSession.closeFile()


if __name__ == "__main__":
    main()