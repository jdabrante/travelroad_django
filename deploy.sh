#!/bin/bash
cd /home/pc17-dpl/travelroad_django
   git add .
   git commit -m "Changes"
   git push

ssh dimas@dimas.arkania.es "
  cd /home/dimas/travelroad_django
  git pull

  source .venv/bin/activate
  pip install -r requirements.txt

  # python manage.py migrate
  # python manage.py collectstatic --no-input

  supervisorctl restart travelroad
"
