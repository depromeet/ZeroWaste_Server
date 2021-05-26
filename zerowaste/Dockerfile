FROM python:3.8.6-buster

RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && apt-get install -y --no-install-recommends ssh \
    && apt-get install -y gcc \
    && apt-get clean \
    && apt-get upgrade -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/

RUN python -m pip install --upgrade pip
COPY ./requirements.txt .

RUN pip3 install -r requirements.txt

RUN mkdir /zerowaste
COPY . /zerowaste/
RUN cd zerowaste

EXPOSE 8000

# running server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
