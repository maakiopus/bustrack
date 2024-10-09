#!/usr/bin/env bash
poetry run gunicorn -c gunicornconfig.py main:app

