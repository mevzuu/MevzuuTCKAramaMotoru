from flask import Flask, render_template, request, redirect, url_for
from app.NLP_Files import MevzuuNLP
from app.TextCleanFiles import TextCleaning

nlpOperator = MevzuuNLP.Operator()
app = Flask(__name__)


@app.route('/', methods=["POST", "GET"])
def start():
    if request.method == "POST":
        searchKey = request.form["search"]
        qaFlag = request.form.get("qa_chcbx")
        if qaFlag == None:
            qaFlag = False
        else:
            qaFlag = True

        return redirect(url_for("Searcher", search=searchKey, qaFlag=qaFlag))

    return render_template("index.html", search="", len=0, results=[], lawHeaders=[], scores=[])


@app.route("/<search>/<qaFlag>", methods=["POST", "GET"])
def Searcher(search, qaFlag):
    if request.method == "POST":
        search = request.form["search"]
        qaFlag = request.form.get("qa_chcbx")  # We used this structure because QA is very slow than Lemmaziation

    if (qaFlag == None or type(qaFlag)==str):
        qaFlag = False
    else:
        qaFlag = True

    print(qaFlag)
    print(type(qaFlag))

    searchClean = TextCleaning.clean_tex(search)

    results, lawHeaders, scores = nlpOperator.Main(searchClean, qaFlag)

    return render_template("index.html", search=search, len=len(results), results=results, lawHeaders=lawHeaders,
                           scores=scores)


if __name__ == '__main__':
    app.run()
