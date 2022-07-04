FROM python:3

RUN pip install flask pyyaml requests
COPY . .
ENV FLASK_APP=loadmanager.py
EXPOSE 5000
CMD ["python", "loadmanager.py"]