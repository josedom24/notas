FROM python:3
RUN apt-get update -y && apt-get install -y \
        libsasl2-dev python-dev libldap2-dev libssl-dev \
        && apt-get clean && rm -rf /var/lib/apt/lists/*
WORKDIR /usr/src/app
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY  ./notas .
RUN python3 manage.py migrate
CMD [ "python3", "./manage.py","runserver","0.0.0.0:8000" ]
EXPOSE 8000
