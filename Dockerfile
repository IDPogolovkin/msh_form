FROM python:3.8-alpine

COPY ./requirements.txt /msh_form_prod/requirements.txt

WORKDIR /msh_form_prod

RUN pip install -r requirements.txt

COPY . /msh_form_prod

EXPOSE 5088

# CMD ["gunicorn",  "app:app", "-w", "2", "-b", "0.0.0.0:5088"] 
CMD ["python", "wsgi.py"]