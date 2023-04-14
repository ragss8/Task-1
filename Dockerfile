FROM python:3.9.7
WORKDIR /usr/src
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "index:app", "--host", "0.0.0.0", "--port", "8008"]


