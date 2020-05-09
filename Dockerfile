FROM evennia/evennia:latest

# install additional packages for SSL support
# TODO: freeze dependencies into a requirements.txt etc
#USER root
#RUN pip install pyopenssl pycrypto pyasn1 service_identity
#USER evennia

ENTRYPOINT evennia start -l