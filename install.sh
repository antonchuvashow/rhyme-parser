#!/bin/bash

INCLUDE_ADMINER=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --with-adminer)
            INCLUDE_ADMINER=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

git clone https://github.com/your-username/rhymezone-website.git
cd rhymezone-website

if [ "$INCLUDE_ADMINER" = true ]; then
    docker-compose up --build -d
else
    docker-compose up --build -d db web
fi

echo "Rhymezone Website has been successfully set up."
echo "Access the website at http://localhost"

if [ "$INCLUDE_ADMINER" = true ]; then
    echo "Adminer (Database Management) is available at http://localhost:8080"
    echo "  - System: PostgreSQL"
    echo "  - Server: db"
    echo "  - Username: test"
    echo "  - Password: test123"
    echo "  - Database: test"
fi
