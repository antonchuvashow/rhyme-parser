# Rhyme Parser

https://github.com/antonchuvashow/rhyme-parser/assets/54022438/e5beb18f-686a-4d55-8669-cdba48941320

## Project Overview

This project is a web application built with Flask and using PostgreSQL as the database. It allows users to search for
rhymes. Please note that this is a **learning project**, and the rhymes are parsed from **Rhymezone**, so be mindful of
their license.

## Prerequisites

Before you begin, ensure that you have Docker installed on your machine.

- [Docker Installation Guide](https://docs.docker.com/get-docker/)

## Quick Start with `install.sh`

1. **Clone the repository**:

    ```bash
    git clone https://github.com/antonchuvashow/rhyme-parser
    cd rhyme-parser
    ```

2. **Run the install.sh script**:
    - With this script, you can run the project without Adminer by default.
    ```bash
    ./install.sh
    ```
   However, if you want to include Adminer, you can use the `--with-adminer` option:

    ```bash
    sudo chmod +x ./install.sh
    ./install.sh --with-adminer
    ```
   This will build and start only the web container with Adminer.

3. **Access the website**:

   Open your web browser and go to [http://localhost](http://localhost)
4. **Accessing Adminer (Database Management)**:
    - Adminer is available at [http://localhost:8080](http://localhost:8080)
        - **System**: PostgreSQL
        - **Server**: localhost
        - **Username**: test
        - **Password**: test123
        - **Database**: (Leave empty)

## Manual Setup

If you prefer a more flexible setup without Docker Compose, you can manually build and start the containers:

1. Clone the repository:

    ```bash
    git clone https://github.com/antonchuvashow/rhyme-parser
    cd rhyme-parser
    ```

2. Build the Docker containers:

    ```bash
    docker build -t rhyme-parser-web .
    ```

3. Start the PostgreSQL container:

    ```bash
    docker run -d --name rhyme-parser-db -e POSTGRES_USER=test -e POSTGRES_PASSWORD=test123 -p 5432:5432 postgres
    ```

4. Start the Flask web application container:

    ```bash
    docker run -d --name rhyme-parser-web -e FLASK_SECRET=really_secret_key_close_your_eyes -e DB_USERNAME=test -e DB_PASSWORD=test123 -e DB_HOST=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' rhyme-parser-db) -e DB_PORT=5432 -p 80:3000 rhyme-parser-web
    ```

5. Access the website:

   Open your web browser and go to [http://localhost](http://localhost)

## License

This project is a learning experiment, and the rhymes are sourced from Rhymezone. Be sure to review and comply with
Rhymezone's licensing terms.

---

**Note:** The provided information is for educational purposes only, and usage compliance with Rhymezone's license is
the responsibility of the user.
