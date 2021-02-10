FROM alpine

RUN set -ex && \
    apk add --no-cache gcc musl-dev
RUN ["mkdir", "code"]
RUN ["mkdir", "script"]
RUN /bin/sh -c 'echo "echo | \$1 \$2 -o \${3:-a.out}" > /script/build.sh'
RUN /bin/sh -c 'echo "cat inp.txt  | ./\${1:-a.out}" > /script/run.sh'

WORKDIR /code

CMD ["sleep","60s"]