FROM python:3.11-slim
WORKDIR /file
COPY ./file.py ./requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5051
CMD ["python3", "file.py"]