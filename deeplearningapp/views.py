import pandas as pd
from django.shortcuts import render
import pickle
from transformers import AutoModelForSequenceClassification, AutoTokenizer, \
    TextClassificationPipeline, AutoModelForMaskedLM, AutoModelForSeq2SeqLM


# Create your views here.
def hello(request):
    return render(request, 'index.html')


def home(request):
    return render(request, 'header.html')


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'signup.html')


def use(request):
    return render(request, 'useModel.html')


def about(request):
    return render(request, 'about.html')


def model_detail(request):
    ctx = {}
    if request.POST:
        input1 = request.POST.get("input")
    #     with open("models/DecisionTree.sav", "rb") as f:
    #         model = pickle.load(f)
    #     input1 = input1.split(',')
    #     input1 = pd.DataFrame([input1], columns=['LIMIT_BAL', 'SEX', 'EDUCATION', 'MARRIAGE', 'AGE', 'PAY_0', 'PAY_2',
    #                                              'PAY_3', 'PAY_4', 'PAY_2', 'PAY_13', 'PAY_123', 'PAY1', 'PAY_22',
    #                                              'PAY_31', 'PAY_43', 'PAY_2213', 'PAY_132', 'PAY_1235', 'PAY11',
    #                                              'PAY_22A', 'PAY_43Q', 'PAY_2213W'
    #                                              ])
    #     output = model.predict(input1)
    #     ctx['outcome'] = output

        # 从hugging face直接调用
        # import requests
        # input1 = request.POST.get("input")
        #
        # API_URL = "https://api-inference.huggingface.co/models/martin-ha/toxic-comment-model"
        # headers = {"Authorization": "Bearer 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"}
        # def query(payload):
        #     response = requests.post(API_URL, headers=headers, json=payload)
        #     return response.json()
        # output = query({
        #     "inputs": input1,
        # })
        # ctx['outcome1'] = output[0][0]['label']
        # ctx['pro1'] = output[0][0]['score']
        # ctx['outcome2'] = output[0][1]['label']
        # ctx['pro2'] = output[0][1]['score']

        # 本地调用配置文件
        # model_path = "ynie/roberta-large-snli_mnli_fever_anli_R1_R2_R3-nli"
        # tokenizer = AutoTokenizer.from_pretrained(model_path)
        # model = AutoModelForSequenceClassification.from_pretrained(model_path)
        # pipeline = TextClassificationPipeline(model=model, tokenizer=tokenizer)

        # 本地调用配置文件用与toxic
        save_directory = "deeplearningapp/models/finbert-tone"  # 要保存模型的目录路径
        # model.save_pretrained(save_directory)  # 将模型保存到指定目录
        # tokenizer.save_pretrained(save_directory)
        model = AutoModelForSequenceClassification.from_pretrained(save_directory)
        tokenizer = AutoTokenizer.from_pretrained(save_directory)
        pipeline = TextClassificationPipeline(model=model, tokenizer=tokenizer)
        print(pipeline)
        ctx['outcome'] = pipeline(input1)[0]['label']

    return render(request, 'model-detail.html', ctx)


def profile(request):
    return render(request, 'profile.html')
