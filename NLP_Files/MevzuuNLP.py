import pandas as pd
from app.NLP_Files import Lemmaziation, QA


class Operator:
    def __init__(self):
        self.Lemmaziation = Lemmaziation.Lemmaziation()
        self.laws = pd.read_csv("../LawsFiles/LawsLabelClean.csv")
        self.groupLaws = pd.read_csv("../LawsFiles/LawsGroupsBy.csv")

    def Main(self, input, QAFlag):

        self.resultDict = dict()
        self.LemmaziationResult = self.Lemmaziation.LawLemma(input=input)

        if QAFlag:
            try:
                self.QA
            except:
                self.QA = QA.QA()
            self.QuestionResult = self.QA.QuestionAnswerProcces(input=input)

            for lemmaziationResultElement in self.LemmaziationResult[:10]:
                resultIndex = lemmaziationResultElement[0]
                for questionResultElement in self.QuestionResult:
                    questionIndex = questionResultElement[0]
                    if resultIndex == questionIndex:
                        score = float((lemmaziationResultElement[1] * 0.8) + (questionResultElement[1] * 0.2 * 100))
                        if score > 40.0:
                            self.resultDict[resultIndex] = {score}

        else:
            for lemmaziationResultElement in self.LemmaziationResult[:10]:
                resultIndex = lemmaziationResultElement[0]
                score = float(lemmaziationResultElement[1])
                if score > 40.0:
                    if resultIndex not in self.resultDict:
                        self.resultDict[resultIndex] = {score}

        my_list = list(self.resultDict.items())
        for mx in range(len(my_list) - 1, -1, -1):
            swapped = False
            for i in range(mx):
                if my_list[i][1] < my_list[i + 1][1]:
                    my_list[i], my_list[i + 1] = my_list[i + 1], my_list[i]
                    swapped = True
            if not swapped:
                break

        lastResultHeaders = []
        lastResultIndexs = []
        scores = []
        for listItem in my_list:
            if not self.laws["LawName"][listItem[0]] in lastResultHeaders:
                lastResultHeaders.append(self.laws["LawName"][listItem[0]])
                lastResultIndexs.append(self.laws["Index"][listItem[0]])
                scores.append(listItem[1])

        lastResultIndexs = lastResultIndexs[:10]
        lastResultHeaders = lastResultHeaders[:10]
        scores = scores[:10]

        lastResult = []
        for listItem in lastResultIndexs:
            lastResult.append(self.groupLaws["Law"][listItem - 1])

        lastResult = lastResult[:10]

        return lastResult, lastResultHeaders, scores
