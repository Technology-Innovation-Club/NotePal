# Set the default PostgreSQL major version to 15
ARG PG_MAJOR=15

# Use the official PostgreSQL image for the specified major version
FROM postgres:$PG_MAJOR

# Set the PostgreSQL major version as a build argument
ARG PG_MAJOR

#Install apt-transport-https, ca-certificates, curl, and lsb-release to access Debian repositories
RUN apt-get update && \
    apt-get install -y --no-install-recommends apt-transport-https ca-certificates curl gnupg lsb-release

# Install git to clone the repository and other build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends git build-essential postgresql-server-dev-$PG_MAJOR

# Disable SSL verification for git clone
ENV GIT_SSL_NO_VERIFY=1

# Clone the pgvector repository from GitHub
RUN git clone https://github.com/pgvector/pgvector.git /tmp/pgvector

# Build and install the pgvector extension
RUN cd /tmp/pgvector && \
    make clean && \
    make OPTFLAGS="" && \
    make install && \
    mkdir /usr/share/doc/pgvector && \
    cp LICENSE README.md /usr/share/doc/pgvector

# Clean up unnecessary build dependencies and files
RUN rm -rf /tmp/pgvector && \
    apt-get remove -y git build-essential postgresql-server-dev-$PG_MAJOR && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*