# Custom Dockerfile
FROM apache/airflow:1.10.10

ARG AIRFLOW_USER_HOME=/opt/airflow
ARG PYTHON_DEPS=""
ENV AIRFLOW__CORE__AIRFLOW_HOME=${AIRFLOW_USER_HOME}
# Install mssql support & dag dependencies
USER root
RUN apt-get update -yqq \
    && apt-get install -y gcc freetds-dev \
    && apt-get install -y git procps \
    && apt-get install -y vim
RUN pip install apache-airflow[crypto,celery,gcp_api,mssql,postgres,s3]
RUN pip install apache-airflow[ssh]==1.10.10 \
        --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-1.10.10/constraints-3.6.txt"
RUN pip install sshtunnel google-api-python-client oauth2client \
    && pip install git+https://github.com/infusionsoft/Official-API-Python-Library.git \
    && pip install apache-airflow-backport-providers-google
RUN if [ -n "${PYTHON_DEPS}" ]; then pip install ${PYTHON_DEPS}; fi

# This fixes permission issues on linux.
# The airflow user should have the same UID as the user running docker on the host system.
# make build is adjust this value automatically
ARG DOCKER_UID
RUN \
    : "${DOCKER_UID:?Build argument DOCKER_UID needs to be set and non-empty. Use 'make build' to set it automatically.}" \
    && usermod -u ${DOCKER_UID} airflow \
    && find / -path /proc -prune -o -user 50000 -exec chown -h airflow {} \; \
    && echo "Set airflow's uid to ${DOCKER_UID}"

RUN chown -R airflow: ${AIRFLOW_USER_HOME}

EXPOSE 8080 5555 8793

USER airflow
WORKDIR ${AIRFLOW_USER_HOME}
