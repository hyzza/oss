FROM debian:bullseye

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install --no-install-recommends --yes \
    python3-pip \
    python3-setuptools \
    python3-wheel \
    python3-dev \
    && apt-get clean -y

RUN adduser --system --disabled-password spacy

COPY displacy /usr/lib/python3/dist-packages/spacy-services/displacy

# install dependencies like SpaCy and language specific models
RUN pip3 install --no-cache-dir -r /usr/lib/python3/dist-packages/spacy-services/displacy/requirements.txt

RUN apt-get clean -y && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

USER spacy

ENTRYPOINT ["/usr/bin/python3", "/usr/lib/python3/dist-packages/spacy-services/displacy/app.py"]
