FROM python:alpine

RUN apk -U upgrade && apk add git
RUN apk add chromium chromium-chromedriver
RUN pip install -U pip && pip install opensearch-py timesketch timesketch_api_client timesketch_import_client pyyaml google-api-python-client -U

WORKDIR /data

ENTRYPOINT ["python3", "gwforensic.py"]
CMD ["-h"]
