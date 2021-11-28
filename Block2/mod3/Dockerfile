FROM python:3.10
WORKDIR /assistant_m
RUN pip install pipenv

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

RUN pipenv install --system --deploy

CMD python app.py

COPY . .