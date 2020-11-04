from src.literature_conversion.src.Reader import readCompleteInstance, readPartialInstance
from src.literature_conversion.src.Writer import writeInFileCompleteInstance
from os import listdir
from os.path import isfile, join

if __name__ == '__main__':
    foldernames = ["DenseMap", "DenseRect",  "RandomMap", "RandomRect"]
    for foldername in foldernames:
        print("write set " + foldername + "...")
        onlyfiles = [f for f in listdir("../res/" + foldername) if isfile(join("../res/" + foldername, f))]
        for filename in onlyfiles:
            componentList = readCompleteInstance("../res/" + foldername + "/" + filename, 5)
            writeInFileCompleteInstance("../../../benchmark_instances/literature_instances/" + foldername + "/" + filename, componentList)
        print("completed set " + foldername + "...")

    foldernames = ["HardGrid", "MunichDrillholes", "RegularGrid", "VariableDensity"]
    for foldername in foldernames:
        print("write set " + foldername + "...")
        onlyfiles = [f for f in listdir("../res/" + foldername) if isfile(join("../res/" + foldername, f))]
        for filename in onlyfiles:
            componentList = readPartialInstance("../res/" + foldername + "/" + filename, 6)
            writeInFileCompleteInstance("../../../benchmark_instances/literature_instances/" + foldername + "/" + filename, componentList)
        print("completed set " + foldername + "...")
