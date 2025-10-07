FROM python:3.13-slim
WORKDIR .
COPY . .
RUN pip install --no-cache-dir --root-user-action=ignore -r requirements.txt
EXPOSE 5051
CMD ["python3", "file.py"]