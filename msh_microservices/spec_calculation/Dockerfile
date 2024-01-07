FROM python:3.8-alpine

COPY ./requirements.txt /spec_calculation/requirements.txt

WORKDIR /spec_calculation

RUN pip install -r requirements.txt

COPY . /spec_calculation

EXPOSE 8083

# CMD ["gunicorn", "-b", "0.0.0.0:8083", "app:app"] 
# CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8083", "app:app"] 
CMD ["python", "wsgi.py"]


