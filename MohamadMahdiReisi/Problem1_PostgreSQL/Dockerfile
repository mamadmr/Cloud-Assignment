FROM postgres:latest

ENV POSTGRES_USER=amir
ENV POSTGRES_PASSWORD=barari
ENV POSTGRES_DB=mydatabase
ENV POSTGRES_PORT=5432

RUN mkdir -p /docker-entrypoint-initdb.d

EXPOSE ${POSTGRES_PORT}

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}

VOLUME /var/lib/postgresql/data