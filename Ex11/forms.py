from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import SubmitField, FieldList, IntegerField, FormField, StringField, FloatField,SelectField
from wtforms.validators import DataRequired, Length
from wtforms.widgets import TextArea
from approximation_schemes_AAWY import *
app = Flask(__name__)
app.config["SECRET_KEY"] = "RandomString"


@app.route('/')
def getParams():
    form = Params()
    return render_template("enterParams.html", form=form)

class Params(FlaskForm):
    f = StringField("enter your f() function in this format: lambda x: f(x)")
    e= FloatField("enter your epsilon")
    jobs=StringField("enter your list of jobs in this format: [j1,j2,..,jn] or [(i1,j1),...,(in,jn)]")
    bins=IntegerField("enter number of bins")
    sumsOrContent=SelectField(u'Bins type', choices=['Bins Keeping sums','Bins Keeping contents'])
    s = SubmitField("Submit")


@app.route('/rank', methods=["POST"])
def AlgoInput():
    f = request.form["f"]
    e = request.form["e"]
    jobs = request.form["jobs"]
    bins = request.form["bins"]
    sumsOrContent = request.form["sumsOrContent"]
    form = CalcAlgo(f,e,jobs,bins,sumsOrContent,1)
    return render_template("Algo.html", form=form, f=f,e=e,jobs=jobs,bins=bins,sumsOrContent=sumsOrContent, ans=0)


class CalcAlgo(FlaskForm):
    def __init__(self,f,e,jobs,bins,sumsOrContent, ans):
        self.f=f
        self.e=e
        self.jobs=jobs
        self.bins=bins
        self.sumsOrContent=sumsOrContent
        self.ans=readInputFromWeb(f,e,jobs,bins,sumsOrContent)
        super(CalcAlgo, self).__init__([f,e,jobs,bins,sumsOrContent, ans])  
        
def readInputFromWeb(f,e,jobs,bins,sumsOrContent):
    #bins definition:
    if sumsOrContent=='Bins Keeping contents':
        content=True
    else:
        content=False 
    binsNum=int(bins)
    #jobs definition
    jobsList=list(eval(jobs))
    #epsilon definition
    epsilon=float(e)
    #f() definition
    f= eval(f)
    if content:
        ans=mainAlgorithm(BinsKeepingContents(binsNum),jobsList,epsilon, f)
    else:    
        ans=mainAlgorithm(BinsKeepingSums(binsNum),jobsList,epsilon, f)
    return ans    





app.run()