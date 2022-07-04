FROM python:3

RUN pip install flask apscheduler
COPY ./app.py /app/app.py
ENV FLASK_APP=/app/app.py
EXPOSE 5000
CMD ["python", "/app/app.py"]