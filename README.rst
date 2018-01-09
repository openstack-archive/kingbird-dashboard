===============================
Kingbird Dashboard
===============================

User Interface for Kingbird

* Free software: Apache license
* Source: http://git.openstack.org/cgit/openstack/kingbird-dashboard
* Bugs: http://bugs.launchpad.net/kingbird-dashboard

Features
--------

* TODO

Enabling in DevStack
--------------------

Add this repo as an external repository into your ``local.conf`` file::

    [[local|localrc]]
    enable_plugin kingbird_dashboard https://github.com/openstack/kingbird-dashboard

Manual Installation
-------------------

Begin by cloning the Horizon and Kingbird Dashboard repositories::

    git clone https://github.com/openstack/horizon
    git clone https://github.com/openstack/kingbird-dashboard

Create a virtual environment and install Horizon dependencies::

    cd horizon
    python tools/install_venv.py

Set up your ``local_settings.py`` file::

    cp openstack_dashboard/local/local_settings.py.example openstack_dashboard/local/local_settings.py

Open up the copied ``local_settings.py`` file in your preferred text
editor. You will want to customize several settings:

-  ``OPENSTACK_HOST`` should be configured with the hostname of your
   OpenStack server. Verify that the ``OPENSTACK_KEYSTONE_URL`` and
   ``OPENSTACK_KEYSTONE_DEFAULT_ROLE`` settings are correct for your
   environment. (They should be correct unless you modified your
   OpenStack server to change them.)

Install Kingbird Dashboard with all dependencies in your virtual environment::

    tools/with_venv.sh pip install -e ../kingbird-dashboard/

And enable it in Horizon::

    ln -s ../kingbird-dashboard/kingbird_dashboard/enabled/_90_project_kingbird_panelgroup.py openstack_dashboard/local/enabled
    ln -s ../kingbird-dashboard/kingbird_dashboard/enabled/_91_project_kingbird_kingbirds_panel.py openstack_dashboard/local/enabled

To run horizon with the newly enabled Kingbird Dashboard plugin run::

    ./run_tests.sh --runserver 0.0.0.0:8080

to have the application start on port 8080 and the horizon dashboard will be
available in your browser at http://localhost:8080/
