import pandas as pd
from transformers import AutoTokenizer, AutoModelForQuestionAnswering, pipeline
from app.TextCleanFiles import TextCleaning


class QA:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("lserinol/bert-turkish-question-answering")
        self.model = AutoModelForQuestionAnswering.from_pretrained("lserinol/bert-turkish-question-answering")
        self.nlp = pipeline("question-answering", model=self.model, tokenizer=self.tokenizer)
        self.laws = pd.read_csv("../LawsFiles/LawsLabelClean.csv")

    def QuestionAnswerProcces(self, input):
        scoreDict = dict()

        for index, row in self.laws.iterrows():
            law = row["CleanLaw"]

            try:
                result = self.nlp(question=input, context=law)
                if index in scoreDict:
                    if result["score"] > scoreDict[index]:
                        scoreDict[index] = result["score"]
                else:
                    scoreDict[index] = result["score"]
            except Exception as e:
                pass

        my_list = list(scoreDict.items())
        return my_list

    def LawCleaning(self):
        self.laws = pd.read_csv("../LawsFiles/Laws_TCK.csv")
        cleanLaws = []
        for index, row in self.laws.iterrows():
            law = row["Law"]
            law = TextCleaning.clean_tex(law)
            cleanLaws.append(law)

        self.laws['CleanLaw'] = cleanLaws
        self.laws.to_csv("LawsLabelClean.csv", index=False)
