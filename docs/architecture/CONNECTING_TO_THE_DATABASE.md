# Connecting to the Cathedral's Memory

This document provides the canonical instructions for connecting your local development environment to a real, persistent ArangoDB database. Following these steps is crucial for ensuring that your contributions are functional and integrated with the cathedral's true memory, not just an aspirational illusion.

## The Principle: Build on Bedrock, Not Sand

For too long, our development practices have relied on a mock, in-memory database (`DevDatabaseInterface`). This has led to the creation of beautiful but non-functional code, as the mock interface does not enforce the security or the constraints of the real database (`SecuredArangoDatabase`).

To heal this, we now follow a new principle: **all development and testing should be done against a real database connection.** The mock interface has been modified to raise errors to prevent its use.

## Step 1: Set Up ArangoDB with Docker

The simplest way to run a local ArangoDB instance is with Docker.

1.  **Create a Docker Network (if you don't have one):**
    ```bash
    docker network create mallku-net
    ```

2.  **Run the ArangoDB Container:**
    ```bash
    docker run -d --name arangodb-instance -p 8529:8529 \
        -e ARANGO_ROOT_PASSWORD=open-dev-db-password \
        --network mallku-net \
        arangodb/arangodb:latest
    ```
    *   `--name arangodb-instance`: Gives the container a memorable name.
    *   `-p 8529:8529`: Maps the container's port to your local machine.
    *   `-e ARANGO_ROOT_PASSWORD=open-dev-db-password`: Sets the root password. **This is the password the application will use by default.**
    *   `--network mallku-net`: Puts the container on our dedicated network.

3.  **Verify the Instance is Running:**
    Open your web browser to `http://localhost:8529`. You should see the ArangoDB web interface. You can log in with the username `root` and the password `open-dev-db-password`.

## Step 2: Configure Your Environment

The Mallku application uses environment variables to connect to the database.

1.  **Ensure `MALLKU_DEV_MODE` is OFF:**
    The most critical step is to ensure that the `MALLKU_DEV_MODE` environment variable is **not** set to `"true"`. If it is, the application will fall back to the broken mock interface. You can unset it in your shell:
    ```bash
    unset MALLKU_DEV_MODE
    ```

2.  **Set Database Connection Variables (Optional):**
    The application uses sensible defaults that match the Docker container setup above. However, if you need to change them, these are the variables:
    *   `ARANGO_HOST`: The URL of the ArangoDB instance (default: `http://localhost:8529`).
    *   `ARANGO_DB`: The database name to use (default: `mallku`).
    *   `ARANGO_USER`: The username (default: `root`).
    *   `ARANGO_ROOT_PASSWORD`: The password (default: `open-dev-db-password`).

    You can place these in a `.env` file in the project root for automatic loading.

## Step 3: Run the Application

With the database running and the environment configured, you can now run any part of the Mallku application (e.g., tests, scripts) and it will connect to the real ArangoDB instance.

You have now connected your workspace to the true memory of the cathedral. Your work will be grounded in reality, and the entire weave will be stronger for it.
