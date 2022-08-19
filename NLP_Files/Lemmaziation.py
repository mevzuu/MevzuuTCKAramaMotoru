import pandas as pd
from fuzzywuzzy import fuzz
from nltk.tokenize import word_tokenize
import zeyrek
from fuzzywuzzy import process

analyzer = zeyrek.MorphAnalyzer()

class Lemmaziation:

    def __init__(self):
        self.laws=pd.read_csv("../LawsFiles/LawsLabelClean.csv")

    def LemmaziationForRoot(self,inputWords):
        lemmaziationResults1 = []

        for i in analyzer.lemmatize(inputWords):
            lemmaziationResults1.append(i[1])

        roots = []

        for i in lemmaziationResults1:
            roots.append(i[0])

        filtretedRootWords = " ".join(roots)
        return filtretedRootWords

    def LawLemma(self,input=""):
        input=str(word_tokenize(input))
        input=self.LemmaziationForRoot(input)

        scoreDict={}
        for index, row in self.laws.iterrows():
            try:
                law=row["CleanLaw"]
                score = process.extract(input, [law],scorer=fuzz.ratio)
                if index in scoreDict:
                    if score[0][1]>scoreDict[index]:
                        scoreDict[index]=score[0][1]
                else:
                    scoreDict[index]=score[0][1]
            except Exception as e:
                pass

        my_list = list(scoreDict.items())
        for mx in range(len(my_list) - 1, -1, -1):
            swapped = False
            for i in range(mx):
                if my_list[i][1] < my_list[i + 1][1]:
                    my_list[i], my_list[i + 1] = my_list[i + 1], my_list[i]
                    swapped = True
            if not swapped:
                break
        return my_list