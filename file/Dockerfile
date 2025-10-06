FROM python:3.12-slim
WORKDIR .
COPY ./file.py file.py
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5051
CMD ["python3", "file.py"]