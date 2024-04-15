FROM python:3.12-bookworm

WORKDIR /hiredict-python

COPY . . 

EXPOSE 6379

CMD [ "python", "src/tests.py"]