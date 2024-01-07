FROM python:3.8-alpine

COPY ./requirements.txt /msh_form/requirements.txt

WORKDIR /msh_form

RUN pip install -r requirements.txt

COPY . /msh_form

EXPOSE 5088

# CMD ["gunicorn", "-b", "0.0.0.0:5088", "app:app"] 
CMD ["python", "wsgi.py"]