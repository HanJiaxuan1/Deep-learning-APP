
    FROM python:3.9

    RUN pip install torch==2.0.1 transformers==4.18.0
    
    WORKDIR /app

    ADD deeplearningapp/load.py /app
    ADD deeplearningapp/models/123 /app/deeplearningapp/models/123
    
    EXPOSE 8000
    CMD ["python", "load.py"]
    