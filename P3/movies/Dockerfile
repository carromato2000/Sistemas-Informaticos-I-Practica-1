FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --root-user-action=ignore --upgrade pip
RUN pip install --root-user-action=ignore -r requirements.txt
COPY . .
EXPOSE 5051
CMD ["python3", "movies.py"]