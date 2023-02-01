# Developing an invoicing app with Flask and Vue.js

## Local Run

1. Clone this repo
2. Copy and update .env files in each folder by running:
    ``` 
    $ cp .env.dev .env 
    ```

1. Spin up both containers using docker-compose:

    ```
    $ docker compose up
    ```

    Navigate to [http://localhost:5000](http://localhost:5000) to access the api docs/admin

    Navigate to [http://localhost:8080](http://localhost:8080) to access the vue app

4. A test Postgres db has already been setup, so zero work is required ther.

## Production Deployment

1. Github actions is setup to:
    - Build from the master branch
    - Fetch environment variables from AWS secrets keys (can be swapped out for any secrets manager)
    - Build and push individual containers of both api and frontend folders to ECR(or docker hub)
    - Finally deploy to an ec2 instance(or droplet)
