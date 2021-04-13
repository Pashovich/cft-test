FROM python:3.7
ENV PYTHONUNBUFFERED=1
WORKDIR /cft-test


RUN apt-get update && apt-get -y dist-upgrade
RUN apt-get -y install build-essential libssl-dev libffi-dev libblas3 libc6 liblapack3 gcc python3-dev python3-pip cython3
RUN apt-get -y install python3-numpy python3-scipy 
RUN apt install -y netcat
RUN rm -rf /var/lib/apt/lists/*


copy requirements.txt requirements.txt
run pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

COPY ./entrypoint.sh .
COPY . .

run chmod +x ./entrypoint.sh

ENTRYPOINT [ "./entrypoint.sh" ]