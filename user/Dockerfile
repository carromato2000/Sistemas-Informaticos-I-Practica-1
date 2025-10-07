FROM python:3.12-slim
WORKDIR .
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5050
CMD ["python3", "user.py"]