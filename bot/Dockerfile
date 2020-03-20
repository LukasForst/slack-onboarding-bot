FROM python:3.7

# create application folder
RUN mkdir /app
WORKDIR /app

# copy dependencies
COPY requirements.txt /app/

# install dependencies
RUN pip install -r requirements.txt

# copy code
COPY . /app/

# start app
EXPOSE 3000
ENV FLAS_APP=app
ENV FLAS_ENV=production
CMD flask run --port=3000 --host=0.0.0.0