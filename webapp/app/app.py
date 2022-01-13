from turtle import st
from flask import Flask
import numpy as np
from joblib import load

app = Flask(__name__)

@app.route("/")
def hello_world():
    test_np_input = np.array([[2021,24,1,100],[2021,5,80,80],[2021,24,8,55],[2021,24,20,67]])
    model = load('model.joblib')
    preds = model.predict(test_np_input)
    preds_as_str = str(preds)
    return preds_as_str
    