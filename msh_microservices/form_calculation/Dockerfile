FROM python:3.8-alpine

COPY ./requirements.txt /form_calculation/requirements.txt

WORKDIR /form_calculation

RUN pip install -r requirements.txt

COPY . /form_calculation

EXPOSE 8084

# CMD ["gunicorn", "-b", "0.0.0.0:8084", "app:app"] 
# CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8084", "app:app"] 
CMD ["python", "wsgi.py"]