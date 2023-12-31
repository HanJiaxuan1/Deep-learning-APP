import pandas as pd
from django.shortcuts import render, HttpResponse, redirect
import pickle
from transformers import AutoModelForSequenceClassification, AutoTokenizer, \
    TextClassificationPipeline, AutoModelForMaskedLM, AutoModelForSeq2SeqLM, AutoModelForCausalLM
from transformers import pipeline, \
    TextClassificationPipeline, AutoModelForMaskedLM, AutoModelForSeq2SeqLM, AutoModelWithLMHead
from app.models import Model, User
from concurrent.futures import ThreadPoolExecutor
from django.contrib import auth
from werkzeug.security import generate_password_hash
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.contrib import messages
from datetime import date
from . import load
import docker
import os
from django.conf import settings
import subprocess
from django.contrib.sessions.models import Session
from django.http import HttpResponseForbidden
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
import shutil
import zipfile


# Create your views here.
def hello(request):
    return render(request, 'index.html')


def home(request):
    print(request.user)
    print(request.user.is_authenticated)
    return render(request, 'header.html')


def document(request):
    return render(request, 'document.html')


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
    User = get_user_model()
    find_user = User.objects.filter(email=email).first()
    if find_user is None:
        return HttpResponse("0")
    if find_user.verify_password(password) is False:
        return HttpResponse("2")
    request.session["uid"] = find_user.uid   # 获取用户的uid
    auth.login(request, find_user)  # Django自带的系统来身份验证系统来看是否登录了 因为继承了AbstractUser 所以可以使用自带的系统
    print("1")
    return HttpResponse("1")


def RegisterCheck(request):
    email = request.POST.get('email')
    username = request.POST.get('username')
    password = request.POST.get('password')
    User = get_user_model()
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
    token, created = Token.objects.get_or_create(user=new_user)
    print(token)
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


def load_model(model_name, task, content, input1):
    task_dic = {"option1": "text-classification", "option2": "translation_en_to_de",
                "option3": "text-generation", "option4": "summarization",
                "option5": "question-answering", "option6": "fill-mask"}
    save_directory = "deeplearningapp/models_all/" + model_name
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
        return pipe(input1)[0]['token_str'] + " -> " + pipe(input1)[0]['sequence']


def create_container(model_name, task, content, input1):
    # client = docker.from_env()
    image = model_name + ":1.0"
    environment = {
        "MODEL_NAME": model_name,
        "TASK": task,
        "CONTENT": content,
        "INPUT1": input1
    }
    cmd = "python -c 'import os; import load; " \
          "result = load.load_model(os.environ[\"MODEL_NAME\"], os.environ[\"TASK\"], " \
          "os.environ[\"CONTENT\"], os.environ[\"INPUT1\"]); print(result)'"

    # container = client.containers.run(image, detach=True, command=cmd, environment=environment)
    # container.wait()
    # result = container.logs().decode('utf-8').strip()
    # container.remove()

    docker_run_cmd = ["docker", "run", "--rm"]
    for key, value in environment.items():
        docker_run_cmd.extend(["-e", f"{key}={value}"])
    docker_run_cmd.extend([image, "bash", "-c", cmd])
    exec_result = subprocess.run(docker_run_cmd, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, text=True)
    output = exec_result.stdout.strip()
    print(exec_result)
    return output


def model_detail(request):
    user = request.user
    token_value = None
    if user.is_authenticated:
        try:
            token = Token.objects.get(user=user)
            token_value = token
        except Token.DoesNotExist:
            print('Do not find token')
    model_id = request.GET.get('param')
    model = Model.objects.get(model_id=model_id)
    ctx = {'tag': model.tag, 'token': token_value}
    if request.POST:
        input1 = request.POST.get("input")
        content = "a content"
        task = model.tag
        if task == "option5":
            content = request.POST.get("content")
            future = executor.submit(create_container, model.model_name, task, content, input1)
        else:
            # 在线程池中异步运行预测函数
            future = executor.submit(create_container, model.model_name, task, content, input1)
        # 你可以获取任务的结果（这会阻塞线程，直到结果可用）
        ctx['outcome'] = future.result()
        ctx['input'] = input1
        ctx['content'] = content
    return render(request, 'model-detail.html', context={"model": model, "ctx": ctx})


def api_model_detail(request):
    user = request.user
    token_value = None
    if user.is_authenticated:
        try:
            token = Token.objects.get(user=user)
            token_value = token
        except Token.DoesNotExist:
            print('Do not find token')
    model_id = request.GET.get('param')
    model = Model.objects.get(model_id=model_id)
    ctx = {'tag': model.tag, 'token': token_value}
    if request.POST:
        all_tokens = Token.objects.all()
        token_values = [token.key for token in all_tokens]
        authorization_header = request.META.get('HTTP_AUTHORIZATION', None)
        if authorization_header not in token_values:
            return HttpResponseForbidden("Access denied")
        input1 = request.POST.get("input")
        content = "a content"
        task = model.tag
        if task == "option5":
            content = request.POST.get("content")
            future = executor.submit(create_container, model.model_name, task, content, input1)
        else:
            # 在线程池中异步运行预测函数
            future = executor.submit(create_container, model.model_name, task, content, input1)
        # 你可以获取任务的结果（这会阻塞线程，直到结果可用）
        ctx['outcome'] = future.result()
        ctx['input'] = input1
        ctx['content'] = content
    return render(request, 'model-detail.html', context={"model": model, "ctx": ctx})


def profile(request):
    User = get_user_model()
    if 'uid' not in request.session.keys():
        return redirect(reverse('login'))
    user = User.objects.get(uid=request.session['uid'])
    my_model = Model.objects.filter(uid=request.session['uid']).all()
    return render(request, 'profile.html', {'user': user, 'my_model': my_model})


def modify_profile(request):
    User = get_user_model()
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


# RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
def create_dockerfile(model, torch_ver, transformers_ver):
    dockerfile_content = f"""
    FROM python:3.9

    RUN pip install torch=={torch_ver} transformers=={transformers_ver}
    
    WORKDIR /app

    ADD deeplearningapp/load.py /app
    ADD deeplearningapp/models/{model} /app/deeplearningapp/models/{model}
    
    EXPOSE 8000
    CMD ["python", "load.py"]
    """
    with open("dockerfile", "w") as f:
        f.write(dockerfile_content)


def build_docker_image(model_name):
    current_dir = settings.BASE_DIR
    dockerfile_path = os.path.join(current_dir, "")
    client = docker.from_env()
    image_name = model_name
    image_tag = "1.0"
    client.images.build(path=dockerfile_path, tag=f"{image_name}:{image_tag}")


def upload_model(request):
    User = get_user_model()
    if request.method == 'POST':
        print("调用")
        user = User.objects.get(uid=request.session['uid'])
        task_dic = {"option1": "text-classification", "option2": "translation",
                    "option3": "text-generation", "option4": "summarization",
                    "option5": "question-answering", "option6": "fill-mask"}
        files = request.FILES.getlist('files[]')
        print("获取")
        model_name = request.POST.get('name')
        task = request.POST.get('option')
        background = request.POST.get('background')
        input_des = request.POST.get('input_des')
        output_des = request.POST.get('output_des')
        # 检查 model_name 是否已经存在
        if Model.objects.filter(model_name=model_name).exists():
            return HttpResponse(0)
        task_des = task_dic[task]
        new_model = Model(tag=task, upload_date=date.today(), background=background,
                          model_name=model_name, uid=user, input_des=input_des, output_des=output_des, task_des=task_des)
        new_model.save()
        print("存入数据库")
        parent_model = request.POST.get('tokenizer')
        if parent_model != "":
            tokenizer = AutoTokenizer.from_pretrained(parent_model)
            tokenizer.save_pretrained('deeplearningapp/models/' + model_name)
        for file in files:
            print('test')
            fs = FileSystemStorage(location='deeplearningapp/models/' + model_name)
            fs.save(file.name, file)
        print("存入本地")
        pytorch_version = request.POST.get('pytorch')
        print(pytorch_version)
        transformer_version = request.POST.get('transformers')
        print(transformer_version)
        create_dockerfile(model_name, pytorch_version, transformer_version)
        build_docker_image(model_name)
        print("docker")
        # return render(request, 'index.html')
        return HttpResponse(1)


def download_model(request):
    all_tokens = Token.objects.all()
    token_values = [token.key for token in all_tokens]
    authorization_header = request.META.get('HTTP_AUTHORIZATION', None)
    if authorization_header not in token_values:
        return HttpResponseForbidden("Access denied")

    model_id = request.GET.get('param')
    model = Model.objects.get(model_id=model_id)
    model_name = model.model_name
    save_directory = 'deeplearningapp/models/' + model_name
    temp_folder = 'temp_folder'
    os.makedirs(temp_folder, exist_ok=True)

    for item in os.listdir(save_directory):
        item_path = os.path.join(save_directory, item)
        if os.path.isfile(item_path):
            shutil.copy2(item_path, temp_folder)

    zip_filename = model_name + '.zip'
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(temp_folder):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, temp_folder)
                zipf.write(file_path, arcname)

    with open(zip_filename, 'rb') as zip_file:
        zip_content = zip_file.read()

    response = HttpResponse(zip_content, content_type="application/zip")
    response['Content-Disposition'] = f'attachment; filename="{zip_filename}"'
    shutil.rmtree(temp_folder)
    os.remove(zip_filename)
    return response

