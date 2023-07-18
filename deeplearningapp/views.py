import pandas as pd
from django.shortcuts import render, HttpResponse, redirect
import pickle
from transformers import AutoModelForSequenceClassification, AutoTokenizer, \
    TextClassificationPipeline, AutoModelForMaskedLM, AutoModelForSeq2SeqLM, AutoModelForCausalLM
from transformers import pipeline
    TextClassificationPipeline, AutoModelForMaskedLM, AutoModelForSeq2SeqLM, AutoModelWithLMHead, pipeline
from app.models import Model, User
from concurrent.futures import ThreadPoolExecutor
from django.contrib import auth
from werkzeug.security import generate_password_hash
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.contrib import messages
from datetime import date


# Create your views here.
def hello(request):
    return render(request, 'index.html')


def home(request):
    print(request.user)
    print(request.user.is_authenticated)
    return render(request, 'header.html')


def deployment(request):
    context = {}
    if 'uid' not in request.session.keys():
        context['alert_message'] = 'Please log in to upload your models.'
        return render(request, 'login.html', context)
    return render(request, 'deployment.html')


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'signup.html')


def LoginCheck(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    find_user = User.objects.filter(email=email).first()
    if find_user is None or find_user.verify_password(password) is False:
        print(find_user.password)
        print(password)
        return HttpResponse("0")
    request.session["uid"] = find_user.uid
    auth.login(request, find_user)
    print("1")
    return HttpResponse("1")


def RegisterCheck(request):
    email = request.POST.get('email')
    username = request.POST.get('username')
    password = request.POST.get('password')
    find_user = User.objects.filter(email=email).first()
    if find_user is not None:
        return HttpResponse("0")
    # Check if username already exists
    find_user_by_username = User.objects.filter(username=username).first()
    if find_user_by_username is not None:
        return HttpResponse("2")
    password_hash = generate_password_hash(password)
    new_user = User(email=email, username=username, password=password,
                    password_hash=password_hash)
    new_user.save()
    return HttpResponse("1")


def logout(request):
    request.session.pop('uid')
    auth.logout(request)
    return redirect('index')


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
        elif i.tag == 'option3':
            model_dic['option'] = 3
        elif i.tag == 'option4':
            model_dic['option'] = 4
        elif i.tag == 'option5':
            model_dic['option'] = 5
        else:
            model_dic['option'] = 6
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


def load_model(model_name, task, content, input1):
    # save_directory = "deeplearningapp/models/" + model_name
    # dl_model = AutoModelForSeq2SeqLM.from_pretrained(save_directory)
    # tokenizer = AutoTokenizer.from_pretrained(save_directory)
    # pipe = pipeline("translation_en_to_ca", model=dl_model, tokenizer=tokenizer)
    # # pipeline = TextClassificationPipeline(model=dl_model, tokenizer=tokenizer)
    # # return pipeline(input1)[0]['label']
    task_dic = {"option1": "text-classification", "option2": "translation",
                "option3": "text-generation", "option4": "summarization",
                "option5": "question-answering", "option6": "fill-mask"}
    save_directory = "deeplearningapp/models/" + model_name
    # dl_model = AutoModelForSeq2SeqLM.from_pretrained(save_directory)
    # tokenizer = AutoTokenizer.from_pretrained(save_directory)
    pipe = pipeline(task_dic[task], model=save_directory)
    if task == "option1":
        return pipe(input1)[0]['label']
    elif task == 'option2':
        return pipe(input1)[0]['translation_text']
    elif task == 'option3':
        return pipe(input1)[0]['generated_text']
    elif task == 'option4':
        return pipe(input1)[0]['summary_text']
    elif task == 'option5':
        return pipe(question=input1, context=content)['answer']
    else:
        # return pipe(input1)
        return pipe(input1)[0]['token_str'] + " -> " + pipe(input1)[0]['sequence']
    # pipeline = TextClassificationPipeline(model=dl_model, tokenizer=tokenizer)
    # return pipeline(input1)[0]['label']


def model_detail(request):
    model_id = request.GET.get('param')
    model = Model.objects.get(model_id=model_id)
    ctx = {'tag': model.tag}
    if request.POST:
        input1 = request.POST.get("input")
        content = None
        task = model.tag
        if task == "option5":
            content = request.POST.get("content")
            future = executor.submit(load_model, model.model_name, task, content, input1)
        else:
            # 在线程池中异步运行预测函数
            future = executor.submit(load_model, model.model_name, task, None, input1)
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
        ctx['content'] = content
    return render(request, 'model-detail.html', context={"model": model, "ctx": ctx})


def profile(request):
    if 'uid' not in request.session.keys():
        return redirect(reverse('login'))
    user = User.objects.get(uid=request.session['uid'])
    my_model = Model.objects.filter(uid=request.session['uid']).all()
    # like_note = UserlikeNote.objects.filter(user_id=request.session['uid']).all()
    return render(request, 'profile.html', {'user': user, 'my_model': my_model})


def modify_profile(request):
    if 'uid' not in request.session.keys():
        return redirect(reverse('login'))
    user = User.objects.get(uid=request.session['uid'])
    if request.method == 'POST':
        username = request.POST.get('username')
        check_user = User.objects.filter(username=username).first()
        if check_user is None or user.uid == check_user.uid:
            username = request.POST.get('username')
            email = request.POST.get('email')
            user.username = username
            user.email = email
            user.save()
            print("user.save()")
            return HttpResponse(1)
    return HttpResponse(0)


def upload_model(request):
    if request.method == 'POST':
        files = request.FILES.getlist('files[]')
        model_name = request.POST.get('name')
        task = request.POST.get('option')
        background = request.POST.get('background')
        input_des = request.POST.get('input_des')
        output_des = request.POST.get('output_des')
        task_des = request.POST.get('task_des')
        new_model = Model(tag=task, upload_date=date.today(), background=background,
                          model_name=model_name, input_des=input_des, output_des=output_des, task_des=task_des)
        new_model.save()
        for file in files:
            fs = FileSystemStorage(location='deeplearningapp/models/'+model_name)
            fs.save(file.name, file)
        return render(request, 'header.html')


