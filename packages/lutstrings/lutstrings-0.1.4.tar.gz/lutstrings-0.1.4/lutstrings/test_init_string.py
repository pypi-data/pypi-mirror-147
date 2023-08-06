import rapidwright
from com.xilinx.rapidwright.design import Design
import lut


def main():
    print("Main")

def test_1():
    pathToTestDir = "../testFiles/"

    intstring = "0x0123456789ABCDEF"        # Init string as shown by rapidwright
    a = lut.hexStringToBinary(intstring)
    b = lut.binStringToList(a)

    files = ["abcdef", 
    "bcdefa", 
    "cdefab", 
    "defabc", 
    "efabcd", 
    "fabcde",
    "bacdef",
    "cbadef",
    "dbcaef",
    "ebcdaf",
    "fbcdea"]

    bitstreamFiles = []
    bitSuffix = "_pblock_bb_partial.bit"

    dcpFiles = []

    for f in files:
        bitstreamFiles.append(pathToTestDir + f + bitSuffix)
        dcpFiles.append(pathToTestDir + f + ".dcp")

    inbits = []
    arti = []

    for i in range(len(files)):
        dcpPath = dcpFiles[i]

        design_or = Design.readCheckpoint(dcpPath)

        #print("\n - - - - - - - - - - - - - - - - - - - - - - \n\n\n")

        orCells = design_or.getCells()


        for c in orCells:
            if "LUT" in str(c):
                lutCell = c

        hm = lutCell.getPinMappingsL2P()
        
        d = lut.fullConversion(hm, intstring)
        
        inbits.append(lut.getInit(bitstreamFiles[i]))
        arti.append(d)

    for i in range(len(inbits)):
        print(inbits[i])
        print(arti[i], "\n")
        assert inbits[i] == arti[i]



if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
    test_1()