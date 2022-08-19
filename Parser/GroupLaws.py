import pandas as pd

laws = pd.read_csv("../LawsFiles/LawsLabelClean.csv")
laws2 = laws.groupby(['Index'])

lawsList = []

for groupIndex in laws2.groups:
    indexs = laws2.groups[groupIndex]
    text = ""
    for lawIndex in indexs:
        text += laws["Law"][lawIndex] + "."

    lawsList.append(text)

df = pd.DataFrame()
df['Law'] = lawsList

df.to_csv("LawsGroupsBy.csv", index=False)
