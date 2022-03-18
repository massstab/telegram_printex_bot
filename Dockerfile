# set base image (host OS)
FROM --platform=linux/arm/v7 arm32v7/python:3.8.10

# set the working directory in the container
WORKDIR /code

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN python -m pip install -r requirements.txt

# update
RUN apt-get update

# install latex
RUN apt-get -y install texlive-latex-base texlive-latex-extra

# ghostscript is needed cor imagemagick (convert pdf to jpg)
RUN apt-get -y install ghostscript

# delete some line in imagemagick policy or convert will not work
RUN sed -i '/<policy domain="coder" rights="none" pattern="PDF"/d' /etc/ImageMagick-6/policy.xml

# copy the content of the local src directory to the working directory
COPY src/ /code

RUN mkdir -p /code/tex

# command to run on container start
CMD [ "python", "./run_bot.py" ] 
# CMD ["sleep", "3600"]
