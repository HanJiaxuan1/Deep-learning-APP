import pandas as pd
from django.shortcuts import render,HttpResponse
import pickle
from transformers import AutoModelForSequenceClassification, AutoTokenizer, \
    TextClassificationPipeline, AutoModelForMaskedLM, AutoModelForSeq2SeqLM
from app.models import Model,User
from concurrent.futures import ThreadPoolExecutor
from django.contrib import auth
from werkzeug.security import generate_password_hash


# Create your views here.
def hello(request):
    return render(request, 'index.html')


def home(request):
    return render(request, 'header.html')


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'signup.html')


def LoginCheck(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    find_user = User.objects.filter(email=email).first()
    if find_user is None or find_user.verify_password(password) is False:
        return HttpResponse("0")
    request.session["uid"] = find_user.uid
    auth.login(request, find_user)
    return HttpResponse("1")


def RegisterCheck(request):
    email = request.POST.get('email')
    username = request.POST.get('username')
    password = request.POST.get('password')
    find_user = User.objects.filter(email=email).first()
    if find_user is not None:
        return HttpResponse("0")
    password_hash = generate_password_hash(password)
    new_user = User(email=email, username=username, password=password,
                    password_hash=password_hash)
    new_user.save()
    return HttpResponse("1")


def use(request):
    models = Model.objects.all()
    # models = Model.objects.defer("tokenizer_data", "model_data")

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
executor = ThreadPoolExecutor(max_workers=50)


def call_model(serialized_model, serialized_tokenizer, input1):
    dl_model = pickle.loads(serialized_model)
    tokenizer = pickle.loads(serialized_tokenizer)
    pipeline = TextClassificationPipeline(model=dl_model, tokenizer=tokenizer)
    return pipeline(input1)[0]['label']


def load_model(model_name, input1):
    save_directory = "deeplearningapp/models/" + model_name
    dl_model = AutoModelForSequenceClassification.from_pretrained(save_directory)
    tokenizer = AutoTokenizer.from_pretrained(save_directory)
    pipeline = TextClassificationPipeline(model=dl_model, tokenizer=tokenizer)
    return pipeline(input1)[0]['label']


def model_detail(request):
    model_id = request.GET.get('param')
    model = Model.objects.get(model_id=model_id)
    ctx = {}
    if request.POST:
        input1 = request.POST.get("input")
        # 在线程池中异步运行预测函数
        future = executor.submit(load_model, model.model_name, input1)
        # print(executor._work_queue.empty())
        # a = executor._work_queue.qsize()
        # print(a)
        # 你可以获取任务的结果（这会阻塞线程，直到结果可用）
        ctx['outcome'] = future.result()

        # print(1)
        # print(time.time())
        # task_id = async_task(
        #     call_model, model.model_data, model.tokenizer_data, input1,
        #     task_name='Model Prediction',
        #     hook=task_finish,
        # )
        # print(2)
        # print(time.time())
        # # task_result = result(task_id)
        # task_result = None
        # i = 1
        # while task_result is None:
        #     print(i)
        #     i += 1
        #     task_result = result(task_id)
        # print(3)
        # print(time.time())
        # ctx['outcome'] = task_result

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
        # save_directory = "deeplearningapp/models/" + model.model_name  # 要保存模型的目录路径
        # # model.save_pretrained(save_directory)  # 将模型保存到指定目录
        # # tokenizer.save_pretrained(save_directory)
        # dl_model = AutoModelForSequenceClassification.from_pretrained(save_directory)
        # tokenizer = AutoTokenizer.from_pretrained(save_directory)
        # pipeline = TextClassificationPipeline(model=dl_model, tokenizer=tokenizer)

        # task = schedule('.call_model', model.model_data, model.tokenizer_data, input1)
        # result = task.wait()  # 等待任务完成并获取结果
        # ctx['outcome'] = result

        # task = call_model.delay(model.model_data, model.tokenizer_data, input1)
        # ctx['outcome'] = task.get()

        # serialized_model = model.model_data
        # dl_model = pickle.loads(serialized_model)
        # serialized_token = model.tokenizer_data
        # tokenizer = pickle.loads(serialized_token)
        # pipeline = TextClassificationPipeline(model=dl_model, tokenizer=tokenizer)
        # ctx['outcome'] = pipeline(input1)[0]['label']

        ctx['input'] = input1
    return render(request, 'model-detail.html', context={"model": model, "ctx": ctx})


def profile(request):
    return render(request, 'profile.html')
