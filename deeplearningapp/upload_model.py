from django.http import HttpResponse
from app.models import Model


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
