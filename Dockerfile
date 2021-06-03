FROM python:slim
ADD . /sandbagger
WORKDIR /sandbagger
EXPOSE 8080
CMD [ "python", "main.py" ]
