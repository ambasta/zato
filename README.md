
Zato /zɑːtəʊ/
-------------

_The next generation ESB and application server written in Python and 
released under a commercial-friendly LGPL license_. Think:

* Increased productivity
* Painless rollouts with less downtime
* Out-of-the-box support for HTTP, JSON, SOAP, Redis, AMQP, JMS WebSphere MQ, 
  ZeroMQ, FTP, SQL, hot-deployment, job scheduling, statistics, 
  high-availability load balancing and more
* Slick web admin GUI, CLI and API
* Awesome documentation
* 24x7 commercial support and training
* Growing community around the project

Visit the project's site at https://zato.io for more information. See you there!


About the fork
--------------


This fork of the original project aims to solve a few issues with the original, such as:

* Cross distribution support via pip
    Zato upstream currently comes with its own bundled installer which is supported across limited platforms/distributions. Zato as a python package simplifies installation on any distribution.
* Ability to run zato in its own environment
    The bundled installer with Zato upstream also builds its own environment. Consequently, it becomes considerably hard to deploy multiple instances of zato each in its own environment.
* Up to date with the latest stable versions of its dependencies
    Finally, upstream currently uses severely outdated versions for various dependencies/libraries. The fork aims to support the latest and greatest software out there.


How do install
--------------

* This project still has a single external dependency against haproxy. Ensure that haproxy is installed on the environment.
* A simple installer which builds the zato python packages and installs them is bundled with the fork, one can simply run this installer in the environment or,
* Build each `zato-*` package individually. For example, one can build `zato-client` by moving to the zato-client directory and running `python setup.py sdist`. The following command set exemplify the same:
    `cd <repo>/code/zato-common && python setup.py sdist && pip install dist/*.tar.gz`
