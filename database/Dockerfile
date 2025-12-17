# Database Dockerfile - MongoDB with initialization
FROM mongo:7.0

# Set environment variables
ENV MONGO_INITDB_ROOT_USERNAME=admin
ENV MONGO_INITDB_ROOT_PASSWORD=password123
ENV MONGO_INITDB_DATABASE=inventory

# Create directory for initialization scripts
RUN mkdir -p /docker-entrypoint-initdb.d

# Copy initialization script
COPY init-mongo.js /docker-entrypoint-initdb.d/

# Copy MongoDB configuration
COPY mongod.conf /etc/mongod.conf

# Create data directory
RUN mkdir -p /data/db && \
    chown -R mongodb:mongodb /data/db

# Expose MongoDB port
EXPOSE 27017

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD mongosh --eval "db.adminCommand('ping')" --quiet || exit 1

# Start MongoDB with custom config
CMD ["mongod", "--config", "/etc/mongod.conf"]
