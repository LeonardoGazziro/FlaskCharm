import os
from subprocess import check_call

from charmhelpers.core.templating import render
from charmhelpers.core.host import service, service_running, service_available
from charmhelpers.core.hookenv import open_port, config
from charmhelpers.core.hookenv import status_set
from charmhelpers.core.hookenv import application_name
from charms.reactive import when, when_not, set_flag, set_state, endpoint_from_flag, when_file_changed
from charms.reactive.flags import register_trigger

def port():
    return int(config('port'))

@when_not('charm_simple_flask.installed')
def install_hello_juju():
    # If your charm has other dependencies before it can install,
    # add those as @when() clauses above., or as additional @when()
    # decorated handlers below
    #
    # See the following for information about reactive charms:
    #
    #  * https://jujucharms.com/docs/devel/developer-getting-started
    #  * https://github.com/juju-solutions/layer-basic#overview
    #

    # further links
    # - https://ubuntu.com/blog/charming-discourse-with-the-reactive-framework

    app = application_name()
    # venv_root = "/srv/charm-simple-flask/venv"
    status_set("maintenance", "Creating Python virtualenv")
    # check_call(['/usr/bin/python3', '-m', 'venv', venv_root])
    status_set("maintenance", "Installing Python requirements")
    check_call(['pip3', 'install', 'gunicorn'])
    check_call(['pip3', 'install', '-r', '/srv/charm-simple-flask/current/requirements.txt'])
    # create_database_tables() # hello-juju can operate without a relation via SQLite via its default settings
    set_state('charm_simple_flask.installed')


@when('charm_simple_flask.installed')
@when_not('charm_simple_flask.gunicorn_configured')
def configure_gunicorn():
    status_set("maintenance", "Configuring gunicorn service")
    render(
        'charm-simple-flask.service.j2',
        '/etc/systemd/system/charm-simple-flaskservice',
        perms=0o755,
        context={
            'port': port(),
            'project_root': '/srv/charm-simple-flask/current',
            'user': 'www-data',
            'group': 'www-data',
        }
    )
    service("enable", "charm_simple_flask")
    status_set("active", "Serving HTTP from gunicorn")

