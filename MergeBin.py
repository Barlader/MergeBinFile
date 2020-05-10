
import struct
import os
import configparser

bin1StartAddr = 0
bin2StartAddr = 16384

class MergeBin:
    def __init__(self, bin1Bytes=None, bin2Bytes=None, fillByte=bytes.fromhex("FF")):
        self.bin1Bytes = bin1Bytes
        self.bin2Bytes = bin2Bytes
        self.fillByte = fillByte
        self.bin1StartAddr = bin1StartAddr
        self.bin2StartAddr = bin2StartAddr
        self.binFile = None
        pass

    def fillPlainSpace(self, start, end):
        if self.binFile is None:
            return -1

        if start >= end:
            return -1

        self.binFile.seek(start)
        for cnt in range(start, end):
            cnt += 1
            self.binFile.write(self.fillByte)
        return 0

    def writeBinApp(self):
        with open(".\\App.bin", "wb") as self.binFile:
            self.binFile.seek(bin1StartAddr)
            self.binFile.write(self.bin1Bytes)
            curPos = self.binFile.tell()
            endPos = 0
            if curPos % 16 != 0:
                endPos = int(int(curPos / 16 + 1) * 16)
            else:
                endPos = int(int(curPos / 16) * 16)

            if self.bin1StartAddr < self.bin2StartAddr:
                endPos = self.bin2StartAddr

            print("fill start addr:", curPos)
            print("fill end addr:", endPos)

            self.fillPlainSpace(curPos, int(endPos))

            self.binFile.write(self.bin2Bytes)

            addStartAddr = self.binFile.tell()
            addEndAddr = 0
            if curPos % 16 != 0:
                addEndAddr = int(int(addStartAddr / 16 + 1) * 16)
            else:
                addEndAddr = int(int(addStartAddr / 16) * 16)

            print("add start addr:", addStartAddr)
            print("add end addr:", addEndAddr)

            self.fillPlainSpace(addStartAddr, int(addEndAddr))
        pass



def main():
    global bin1StartAddr, bin2StartAddr
    parser = configparser.ConfigParser()
    if not os.path.exists(".\\config.ini"):
        print("No Config.ini File")
        return
    print("Found the config.ini")
    parser.read(".\\config.ini")
    sections = parser.sections()

    secName = 'config'
    try:
        index = sections.index(secName)
    except ValueError:
        print("Section name is not config")
        return

    options = parser.items(sections[index])
    print(options)
    dicOptions = {}
    for item in options:
        dicOptions[item[0]] = item[1]

    # print(dicOptions)
    bin1Name = dicOptions['binapp1']
    bin1StartAddr = int(dicOptions['bin1startaddr'])
    bin2Name = dicOptions['binapp2']
    bin2StartAddr = int(dicOptions['bin2startaddr'])

    bin1Bytes = None
    bin2Bytes = None
    with open(bin1Name, "rb") as f1:
        bin1Bytes = f1.read()

    with  open(bin2Name, "rb") as f2:
        bin2Bytes = f2.read()

    MergeBinFile = MergeBin(bin1Bytes, bin2Bytes)
    MergeBinFile.writeBinApp()



if __name__ == '__main__':
    main()


