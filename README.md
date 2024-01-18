# wala
Web interface to execute scripts and get status feedback.

## Development

Clone the project

    gh repo clone Adnn/wala
    pushd wala

Create and use a virtual env

    python3 -m venv .venv
    source .venv/bin/activate

Install the project and its dependencies

    pip3 install -e .

Run the development server, then point your web browser to http://localhost:5000

    flask --app wala run --debug

## Vagrant deployment

`vagrant/` provides a vagrant environment where the `wala` web application is deployed
in a way amenable to production.

It is using `gunicorn` WSGI server, automatically monitored via `systemd`.
It also setup `nginx` as a reverse proxy.
(See `vagrant/deploy.sh` for the actual steps.)

* Up the machine, the deployment will setup the environment:

      pushd vagrant
      vagrant up

* Once deployment is complete, point your browser to http://localhost:8080
