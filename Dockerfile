FROM python:latest

WORKDIR /app

COPY ./MTech .

RUN pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["streamlit", "run"]

CMD ["dashboard.py"]