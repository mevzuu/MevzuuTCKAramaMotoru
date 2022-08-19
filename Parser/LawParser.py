import pandas as pd

temp = open("../LawsFiles/TCk.txt", encoding="utf-8")
words = []
currentWord = ""
lawName = ""
lawIndexCount = 0
indexs = []
lawNames = []

for line in temp.readlines():
    foundDotIndex = line.find(".")
    lawFindIndex = line.find("madde ")
    lawFindIndex2 = line.find("MADDE ")
    lawFindIndex3 = line.find("Madde ")

    if ((lawFindIndex != -1 or lawFindIndex2 != -1 or lawFindIndex3 != -1) and (
            (lawFindIndex == 0 or lawFindIndex2 == 0 or lawFindIndex3 == 0) or (
            lawFindIndex == 1 or lawFindIndex2 == 1 or lawFindIndex3 == 1))):
        lawIndexCount += 1
        startIndex = 0
        endIndex = 0
        if (lawFindIndex != -1):
            startIndex = lawFindIndex
        elif (lawFindIndex2 != -1):
            startIndex = lawFindIndex2
        else:
            startIndex = lawFindIndex3
        for charIndex in range(startIndex, len(line)):
            if line[charIndex] == "-":
                endIndex = charIndex
                break
        lawName = line[startIndex:endIndex]
        pass

    if foundDotIndex != -1:
        donNewLineFlag = False
        try:
            int(line[foundDotIndex - 1])
            donNewLineFlag = True
        except:
            pass

        try:
            int(line[foundDotIndex + 1])
            donNewLineFlag = True
        except:
            pass

        try:
            if line[foundDotIndex + 1].isupper():
                donNewLineFlag = True
        except:
            pass

        try:
            if line[foundDotIndex - 1].isupper():
                donNewLineFlag = True
        except:
            pass

        if donNewLineFlag:
            currentWord += " " + line
        else:
            splitDot = line.split(".")
            if len(splitDot) > 1:
                words.append(currentWord + " " + splitDot[0])
                indexs.append(lawIndexCount)
                lawNames.append(lawName)

                if splitDot[1:-1] != []:
                    words.append(splitDot[1:-1])
                    indexs.append(lawIndexCount)
                    lawNames.append(lawName)
                    currentWord = splitDot[-1]
                else:
                    currentWord = splitDot[1]
            else:
                words.append(currentWord)
                lawNames.append(lawName)
                indexs.append(lawIndexCount)
                currentWord = line

    else:
        currentWord += " " + line

d = {'Law': words, 'Index': indexs, "LawName": lawNames}
df = pd.DataFrame(d, columns=["Law", "Index", "LawName"])

df.to_csv("Laws_TCK.csv", index=False)
