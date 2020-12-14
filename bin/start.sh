#!/bin/bash

export FLASK_APP=app.py
export FLASK_ENV=development

# PARA POWERSHELL EN WINDOWS:
#$env:FLASK_APP = "app.py"
#$env:FLASK_ENV = "development"
flask run --port 5000