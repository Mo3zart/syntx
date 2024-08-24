# Use the official PostgreSQL image as the base
FROM postgres:14

# Set the timezone to Europe/Berlin
ENV TZ=Europe/Berlin
RUN apt-get update && apt-get install -y tzdata && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Argument to pass environment variables from the build context
ARG POSTGRES_USER
ARG POSTGRES_PASSWORD
ARG POSTGRES_DB

# Set environment variables from .env file
ENV POSTGRES_USER=${POSTGRES_USER}
ENV POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
ENV POSTGRES_DB=${POSTGRES_DB}

# Install additional packages
RUN apt-get update && apt-get install -y \
    sudo \
    vim \
    less \
    curl \
    wget \
    net-tools \
    iputils-ping \
    git \
    htop \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy the SQL script into the container
COPY setup/tt_postgres_setup.sql /docker-entrypoint-initdb.d/tt_postgres_setup.sql

# Expose the default PostgreSQL port
EXPOSE 5432

# Start the PostgreSQL service
CMD ["postgres"]
