#!/usr/bin/env bash

flask db upgrade
flask run --debug -h 0.0.0.0