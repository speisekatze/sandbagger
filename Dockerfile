FROM python:3.8.2
ADD . /sandbagger
WORKDIR /sandbagger
EXPOSE 8080
CMD [ "python", "main.py" ]
