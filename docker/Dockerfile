FROM python:3.6

RUN pip install click itk
COPY ./test.mp4 /test.mp4
COPY ./test.gif /test.gif
COPY ./run.py /run.py
ENTRYPOINT ["python", "/run.py"]
