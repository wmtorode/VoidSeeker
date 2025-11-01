#!/bin/sh

alembic-db upgrade
exec python3 /opt/roguestudio/voidseekerbot/voidseeker.py