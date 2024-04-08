# Use the official PostgreSQL image with tag 16
FROM postgres:16

# Set environment variables
ENV POSTGRES_PASSWORD postgres

# Set the working directory inside the container
WORKDIR /docker-entrypoint-initdb.d

# Add the initialization script to the container
# COPY . /docker-entrypoint-initdb.d

# Expose the PostgreSQL port
EXPOSE 5432

# Command to run when the container starts
CMD ["postgres"]
