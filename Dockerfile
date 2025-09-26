
FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
ENV MODEL_PATH=slot_recommender.pkl
EXPOSE 5001
CMD ["python","ai_service/app.py"]
