
    FROM python:3.9

    RUN pip install torch==2.0.1 transformers==4.18.0
    
    WORKDIR /app

    ADD deeplearningapp/load.py /app
    ADD deeplearningapp/models/bert-base-multilingual-uncased-sentiment /app/deeplearningapp/models/bert-base-multilingual-uncased-sentiment
    
    EXPOSE 8000
    CMD ["python", "load.py"]
    