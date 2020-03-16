FROM python:3.7

# create application folder
RUN mkdir /app
WORKDIR /app

# copy dependencies
COPY src/requirements.txt /app/

# install dependencies
RUN pip install -r requirements.txt

COPY . /app/
# start app
EXPOSE 3000
CMD python app.py --port=3000