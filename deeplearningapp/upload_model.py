from django.http import HttpResponse
from app.models import Model
from transformers import AutoModelForSequenceClassification, AutoTokenizer, TextClassificationPipeline
import pickle


# 数据库操作
def upload_model(request):
    test1 = Model(tag="Text Classification",
                  upload_date='2023-06-20',
                  background='go_emotions is based on Reddit data and has 28 labels. It is a multi-label dataset where one or multiple labels may apply for any given input text, hence this model is a multi-label classification model with 28 \'probability\' float outputs for any given input text. Typically a threshold of 0.5 is applied to the probabilities for the prediction for each label.',
                  model_name='roberta-base-go_emotions',
                  input_des='A sentence (eg: I am not having a great day)',
                  output_des='one of labels (eg: disappointment)',
                  task_des='Text classification'
                  )
    test1.save()
    return HttpResponse("<p>数据添加成功！</p>")


def add_model(request):
    save_directory = "deeplearningapp/models/parrot_adequacy_model"  # 要保存模型的目录路径
    dl_model = AutoModelForSequenceClassification.from_pretrained(save_directory)
    tokenizer = AutoTokenizer.from_pretrained(save_directory)
    model_data = Model.objects.get(model_id=6)
    print(1)
    serialized_model = pickle.dumps(dl_model)
    print(2)
    serialized_tokenizer = pickle.dumps(tokenizer)
    print(3)
    model_data.model_data = serialized_model
    print(4)
    model_data.tokenizer_data = serialized_tokenizer
    print(5)
    model_data.save()
    print(6)
    return HttpResponse("<p>模型添加成功！</p>")


def test_model(request):
    model_data = Model.objects.get(model_id=5)
    serialized_model = model_data.model_data
    model = pickle.loads(serialized_model)
    serialized_token = model_data.tokenizer_data
    tokenizer = pickle.loads(serialized_token)
    pipeline = TextClassificationPipeline(model=model, tokenizer=tokenizer)
    print(pipeline("I love you")[0]['label'])
    return HttpResponse("<p>123</p>")
