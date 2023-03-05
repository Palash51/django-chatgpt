#!/bin/sh

until cd /app/chatgpt
do
    echo "Waiting for server volume..."
done

# run a worker :)
celery -A chatgpt worker --loglevel=info --concurrency 1 -E
