from pathlib import Path


def writeInFileCompleteInstance(outputFileName, componentList):
    """

    :type componentList: list[list[str]]
    :type outputFileName: str
    """
    decimals = 0
    for i in range(len(componentList)):
        for j in range(len(componentList[i])-1):
            try:
                if len(componentList[i][j].split('.')[1]) > decimals:
                    decimals = len(componentList[i][j].split('.')[1])
            except IndexError:
                pass

    times = 10**decimals
    for i in range(len(componentList)):
        for j in range(len(componentList[i])-1):
            componentList[i][j] = str(round(float(componentList[i][j])*times))

    Path(outputFileName).parent.mkdir(parents=True, exist_ok=True)
    file = open(outputFileName, "w+")
    file.write(str(len(componentList)))
    file.write("\n")
    for line in componentList:
        for component in line:
            file.write(component)
            file.write("\t")
        file.write("\n")
