#!/usr/bin/env bash
# shellcheck disable=SC2164
cd /home/dmitriy/Projects/car_price_cheker
source venv/bin/activate
python manage.py check_many
