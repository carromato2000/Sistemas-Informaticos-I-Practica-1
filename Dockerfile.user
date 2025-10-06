FROM python:3.11-slim
WORKDIR /user
COPY ./user.py ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5050
CMD ["python3", "user.py"]