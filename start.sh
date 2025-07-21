#!/bin/bash
gunicorn --bind 0.0.0.0:10000 "app:create_app()"
