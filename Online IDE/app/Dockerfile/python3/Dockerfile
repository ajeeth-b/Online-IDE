FROM alpine

RUN ["apk", "add", "python3"]
RUN ["apk", "add", "py-pip"]
RUN ["mkdir", "code"]
RUN ["mkdir", "script"]
RUN /bin/sh -c 'echo "echo | \$1 \$2" > /script/build.sh'
RUN /bin/sh -c 'echo "cat inp.txt  | \$1 \$2" > /script/run.sh'

WORKDIR /code

CMD ["sleep","60s"]