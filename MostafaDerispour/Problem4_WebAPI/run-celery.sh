sudo usermod -aG docker $(whoami)

echo ">>> Activating virtual environment..."
source env/bin/activate

echo ">>> Setting Python path..."
export PYTHONPATH=$(pwd)

echo ">>> Starting Celery Worker..."
celery -A my_celery_app.tasks worker --loglevel=info > celery.log 2>&1 &
CELERY_PID=$!

sleep 5