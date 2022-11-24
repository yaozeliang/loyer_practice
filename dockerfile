# FROM python:3.9.9-buster
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt
# Set timezone
RUN ln -snf /usr/share/zoneinfo/Europe/Paris /etc/localtime && echo Europe/Paris > /etc/timezone

# CMD [ "/bin/bash" ]
# CMD ["python","main.py"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
