#FROM rabbitmq:latest
FROM rabbitmq:3.13-management

################################################################################
#### Set SHELL, ENTRYPOINT and CMD.
################################################################################

# Interaction between ENTRYPOINT and CMD: https://docs.docker.com/reference/dockerfile/#understand-how-cmd-and-entrypoint-interact

# It is used when we write commands RUN, ENTRYPOINT or CMD in shell form.
# By default it is "/bin/sh -c" that doesn't support several commands
# (e.g. source)
SHELL ["/bin/bash", "-c"]

# Command that runs each time container is started (exec form doesn't use SHELL).
#ENTRYPOINT ["python3", "echo.py"]

# Command that is added to exec form of ENTRYPOINT. See more on reference above.
#CMD ["python3", "echo.py"]

################################################################################

# TODO: make profiles
#ADD definitions.json /etc/rabbitmq/
