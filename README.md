# MuN
## MUsic Notifier
MUsic Notifier is an application that sends you notifications about new releases from your favorite artists.
## Features
Releases can be taken from:
- Spotify
- Deezer

Notifications can be sent via:
- Email
- Telegram

## Launching the development environment
You need to have Python and PostgreSQL installed
``` bash
git clone https://github.com/hmlON/mun.git
cd mun

pip install -r requirements.txt

createuser -s postgres
createuser -s mun
createdb -U postgres mun

python manage.py runserver
```

## How you can contribute
- support for more integrations with music services (e.g. Apple Music)
- support for more notifications (e.g. Facebook Bot)
- forwarding from HTTP to HTTPS
- fetching checker
- add ability to have an account without an integration
- improve design
- add tests
- refactoring
