
    FROM python:3.9

    RUN pip install torch==1.9.0 transformers==4.17.0
    
    WORKDIR /app

    ADD deeplearningapp/load.py /app
    ADD deeplearningapp/models/roberta-large /app/deeplearningapp/models/roberta-large
    
    EXPOSE 8000
    CMD ["python", "load.py"]
    