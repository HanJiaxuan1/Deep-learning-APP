from transformers import pipeline


def load_model(model_name, task, content, input1):
    task_dic = {"option1": "text-classification", "option2": "translation_en_to_de",
                "option3": "text-generation", "option4": "summarization",
                "option5": "question-answering", "option6": "fill-mask"}
    save_directory = "deeplearningapp/models/" + model_name
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


