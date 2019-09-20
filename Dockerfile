FROM ciag/python:3.7
COPY . /opt/sendmail
WORKDIR /opt/sendmail
RUN pip install .
