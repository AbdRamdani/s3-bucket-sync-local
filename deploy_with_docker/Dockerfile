FROM python:3.9-slim

WORKDIR /app

# copy the script and necessary files into the container
COPY final.py /app/synchronisation_s3.py

# install dependencies
RUN pip install boto3

# set the default command to run when the container starts
ENTRYPOINT ["python3", "/app/synchronisation_s3.py"]

# pass arguments to execute the script
CMD ["<folder_path>", "<bucket_name>"]

# instructions for building the Docker image and running the container
# build the image using:
# docker build -t syns3_image .

# run the container with:
# docker run -v /home/abd/Desktop/<folder>:/app/local syns3_image /app/local test_s3synch_container
