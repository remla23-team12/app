# Dockerfile
FROM python:3.8.10-slim

WORKDIR /root/

COPY requirements.txt /root/

RUN python -m pip install --upgrade pip &&\
    pip install -r requirements.txt

COPY app.py /root/
COPY templates /root/templates/


ENTRYPOINT ["python"]
CMD ["app.py"]

# this is a model service container we need to expose the PORT which is used to access this service!!!!

EXPOSE 5000

# an image will be built using this dockerfile as a blueprint:
# when running the image to spawn a container we need to map this container's exposed port to 
# a localhost port: docker run -it --rm 1234:8080 <image tag name> <bash => runtime to start the container with>