FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /tf
WORKDIR /tf
ADD requirements.txt /tf/
RUN pip install -r requirements.txt
ADD . /tf
CMD python app.py