import pandas as pd
from django.shortcuts import render
import pickle
from transformers import AutoModelForSequenceClassification, AutoTokenizer, \
    TextClassificationPipeline, AutoModelForMaskedLM, AutoModelForSeq2SeqLM
from app.models import Model
from concurrent.futures import ThreadPoolExecutor

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
    models = Model.objects.all()
    model_list = []
    j = 1
    for i in models:
        model_dic = {}
        if i.tag == 'option1':
            model_dic['option'] = 1
        elif i.tag == 'option2':
            model_dic['option'] = 2
        else:
            model_dic['option'] = 3
        model_dic['model_id'] = i.model_id
        model_dic['img_id'] = j % 10
        model_dic['name'] = i.model_name
        model_dic['date'] = i.upload_date
        model_dic['task_des'] = i.task_des
        model_list.append(model_dic)
        j += 1
    return render(request, 'useModel.html', context={'my_list': model_list})


def about(request):
    return render(request, 'about.html')


# 创建一个线程池
executor = ThreadPoolExecutor(max_workers=5)
def call_model(serialized_model, serialized_tokenizer, input1):
    dl_model = pickle.loads(serialized_model)
    tokenizer = pickle.loads(serialized_tokenizer)
    pipeline = TextClassificationPipeline(model=dl_model, tokenizer=tokenizer)
    return pipeline(input1)[0]['label']


def model_detail(request):
    model_id = request.GET.get('param')
    model = Model.objects.get(model_id=model_id)
    ctx = {}
    if request.POST:
        input1 = request.POST.get("input")
        # 在线程池中异步运行预测函数
        future = executor.submit(call_model, model.model_data, model.tokenizer_data, input1)
        # 你可以获取任务的结果（这会阻塞线程，直到结果可用）
        ctx['outcome'] = future.result()
    return render(request, 'model-detail.html', context={"model": model, "ctx": ctx})


# def model_detail(request):
#     model_id = request.GET.get('param')
#     model = Model.objects.get(model_id=model_id)
#     ctx = {}
#     if request.POST:
#         input1 = request.POST.get("input")
#         serialized_model = model.model_data
#         dl_model = pickle.loads(serialized_model)
#         serialized_token = model.tokenizer_data
#         tokenizer = pickle.loads(serialized_token)
#         pipeline = TextClassificationPipeline(model=dl_model, tokenizer=tokenizer)
#         ctx['outcome'] = pipeline(input1)[0]['label']
#
#     return render(request, 'model-detail.html', context={"model": model, "ctx": ctx})


def profile(request):
    return render(request, 'profile.html')
