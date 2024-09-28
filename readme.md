# Flask Hello World App with Docker, Gunicorn, and Nginx

This project demonstrates how to set up a simple "Hello World" Flask application using Docker, with Gunicorn as the WSGI server and Nginx as the web server. The setup includes persistent storage for an SQLite database and log files.

Flask and Gunicorn are run in one container, while Nginx is run in another container to serve as a reverse proxy. The Flask app is accessible through Nginx on port 80.

Both containers are using same volumes to store persistent app files, data and logs. The Flask app logs are stored in /logs/app.log, while the Nginx access and error logs are stored in /logs/nginx.log. The SQLite database is stored in /data/requests.sqlite.

## Explanation

Flask Application (app.py): A simple Flask app that writes the time of each GET request to an SQLite database, includes the time of the previous request, and the total number of requests in the response. It also ensures the database is created if it doesn’t exist and handles the case when there is no data in the database.

Dockerfile for Flask and Gunicorn: Builds a Docker image for the Flask app, installs dependencies, and runs the app using Gunicorn.

Requirements File (requirements.txt): Lists the dependencies for the Flask app.

Dockerfile for Nginx: Builds a Docker image for Nginx and copies the custom configuration file.

Nginx Configuration (nginx.conf): Configures Nginx to proxy requests to the Flask app and logs access and error logs to the /logs directory.

Docker Compose File (docker-compose.yml): Defines the services for the Flask app and Nginx, mounts volumes for persistent storage, and sets environment variables.

## FLASK_ENV

The FLASK_ENV environment variable is used to set the environment in which your Flask application runs. It can have different values, but the most common ones are:

- development: When FLASK_ENV is set to development, Flask runs in development mode. This mode is useful for development and debugging because it:
    - Enables the interactive debugger.
    - Enables the reloader, which automatically restarts the server when code changes are detected.
    - Provides detailed error messages.
 - production: When FLASK_ENV is set to production, Flask runs in production mode. This mode is optimized for running the application in a production environment. It:
    - Disables the interactive debugger and reloader.
    - Provides less detailed error messages to avoid exposing sensitive information.

## App Volume

The app volume in the docker-compose.yml file is used to mount the application code from your host machine to the container. This setup has several benefits:

 - Development Convenience: By mounting the app directory from your host to the container, you can edit your code on your host machine, and the changes will be reflected in the container immediately. This is especially useful during development.
 - Persistence: It ensures that your application code is persistent and not lost when the container is stopped or removed.
 - Consistency: It keeps your development environment consistent with your production environment, reducing the chances of encountering environment-specific bugs.

In this setup:

 - ./app:/app mounts the app directory from your host machine to the /app directory in the container.
 - ./logs:/logs mounts the logs directory from your host machine to the /logs directory in the container.
 - ./data:/data mounts the data directory from your host machine to the /data directory in the container.

## Project Structure

/path/to/your/project/
├── app/
│   ├── app.py
│   ├── requirements.txt
├── logs/
│   ├── app.log
│   ├── flask.log
│   ├── nginx.log
├── data/
│   ├── requests.sqlite
├── Dockerfile
├── Dockerfile.nginx
├── docker-compose.yml
├── nginx.conf

The project structure consists of the following directories and files:

 - app/: Contains the Flask application code and requirements.txt file.
 - logs/: Contains the log files for the Flask app and Nginx.
 - data/: Contains the SQLite database file.
 - Dockerfile: Builds the Docker image for the Flask app.
 - Dockerfile.nginx: Builds the Docker image for Nginx.
 - docker-compose.yml: Defines the services for the Flask app and Nginx.
 - nginx.conf: Contains the Nginx configuration.

# Development and deployment

## Development on Laptop
 - Develop the Application: You can develop and test your Flask application on your laptop using the provided Docker setup.
 - Build the Docker Images: Build the Docker images on your laptop to ensure everything works as expected.
 - Test the Application: Run the containers on your laptop and test the application to ensure it works correctly.
 - Debugging: If you encounter any issues, you can debug the application on your laptop before deploying it to the server.

## Deployment on Server
 - Transfer Files: Once you have everything working on your laptop, transfer the necessary files to your server. You can use tools like scp (secure copy) or a USB drive to transfer the files.
 - Build Docker Images on the server: If the server has a different architecture ( for example ARM, Raspberry Pi), you will need to build the Docker images on the Server itself.

## How to build and run the containers

Navigate to Project Directory:

    ```bash
    cd /path/to/your/project/
    ```

Build and run the containers:
    
    ```bash
    docker-compose up --build
    ```

This setup will create a Flask app served by Gunicorn, with Nginx as a reverse proxy in a separate container. The SQLite database and log files will be stored persistently in the data and logs directories, respectively.

Access the Flask app:

    Open a web browser and go to http://localhost

You should see the "Hello World" message along with the time of the previous request and the total number of requests.

## How to stop the containers

To stop the containers, press `Ctrl+C` in the terminal where you ran `docker-compose up`. This will stop the containers and clean up the resources.

Alternatively, you can run the following command in a new terminal window:

    ```bash
    docker-compose down
    ```

This will stop and remove the containers, networks, and volumes created by `docker-compose up`.

## How to access the logs

The logs for the Flask app and Nginx are stored in the logs directory on your host machine. You can access them by navigating to the logs directory in your project directory.

For example, to view the Flask app logs:

    ```bash
    cat logs/app.log
    ```

To view the Nginx access and error logs:

    ```bash
    cat logs/nginx.log
    ```

## How to access the SQLite database

The SQLite database file is stored in the data directory on your host machine. You can access it using an SQLite client or by running SQLite commands in the terminal.

For example, to open the SQLite database using the SQLite command-line client:

    ```bash
    sqlite3 data/requests.sqlite
    ```

## How to access the Flask app container

If you need to access the Flask app container for debugging or other purposes, you can do so using the following command:

    ```bash
    docker exec -it flaskapp /bin/bash
    ```

This will open a bash shell in the Flask app container, allowing you to run commands and inspect the container.

