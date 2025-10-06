FROM python:3.12-slim
WORKDIR /user
COPY ./user.py user.py
COPY ./requirements.txt requirements.txt
COPY ./users.txt users.txt
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5050
CMD ["python3", "user.py"]