#!/bin/bash
celery -A tasks worker --loglevel=info --pool=solo

