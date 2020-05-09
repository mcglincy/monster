FROM evennia/evennia:latest

USER root
# install additional packages for SSL support
# TODO: freeze dependencies into a requirements.txt etc
RUN pip install pyopenssl pycrypto pyasn1 service_identity

USER evennia
ENTRYPOINT evennia start -l