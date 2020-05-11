# # name of my chosen image is python
# # official Docker image for Python
# # 3.6-alpine tag selects a Python 3.6 interpreter installed on Alpine Linux
#
# FROM python:3.6-alpine3.6
#
# RUN apt-get update -y && \
#     apt-get install -y python3-pip python3-dev
#
#
# WORKDIR /
#
# COPY requirements.txt requirements.txt
# COPY com_ai_ineuron_utils com_ai_ineuron_utils
# COPY com_ineuron_ai_ml_forKids_model_training com_ineuron_ai_ml_forKids_model_training
# COPY com_ineuron_ai_ml_kids_model_predict com_ineuron_ai_ml_kids_model_predict
# COPY data data
# COPY models models
# COPY main.py main.py
#
# RUN pip3 install -r requirements.txt
#
# ENTRYPOINT [ "python3" ]
#
# CMD [ "main.py" ]


FROM python:3.7.5-slim
# FROM python:3.7-alpine as base

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev && \
    apt-get install -y build-essential cmake && \
    apt-get install -y libopenblas-dev liblapack-dev && \
    apt-get install -y libx11-dev libgtk-3-dev



COPY ./requirements.txt /requirements.txt

WORKDIR /

RUN pip3 install -r requirements.txt

COPY . /

ENTRYPOINT [ "python3" ]

CMD [ "main.py" ]
