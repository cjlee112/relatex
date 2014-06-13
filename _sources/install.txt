##################
Installing ReLaTeX
##################

Obtaining ReLaTeX
-----------------

* You can either download the latest release of ReLaTeX from its
  GitHub `downloads <https://github.com/cjlee112/relatex/tags>`_ page;

* or you can get the very latest code commits using Git, directly
  from the ReLaTeX's `GitHub <https://github.com/cjlee112/relatex>`_ page.
  (This requires using `Git <http://git-scm.com>`_).

Installation
------------

ReLaTeX is a pure Python package; you need 
`Python <http://python.org>`_ to run it.
You can either just run the downloaded ``relatex.py`` script
directly (no install step required), or you can run its
``setup.py`` script to install it on your system.  Both options
have advantages and disadvantages:

Option 1: Running relatex.py directly (no install step required)
................................................................

You can just run ``relatex.py`` directly like this::

  python /path/to/relatex.py plos my.tex

* advantage: this way, it knows where its templates directory
  is (in the same place where ``relatex.py`` is), so you can
  specify a standard template just by giving its name, e.g. ``plos``.

* disadvantage: ReLaTeX requires the Python
  `Jinja2 <http://jinja.pocoo.org>`_ package.  You either have to
  have Jinja2 already installed, or install it yourself via your system's
  software installer, or Python's mechanisms such as ``easy_install``
  and ``pip``, e.g.::

    sudo pip install Jinja2

(leave out ``sudo`` if you are installing to a location you have
write privileges for).

Option 2: Installing relatex.py into your system libraries
..........................................................

In the downloaded ``relatex`` directory run::

  sudo python setup.py install

(leave out ``sudo`` if you are installing to a location you have
write privileges for).

* advantage: assuming your Python has
  `setuptools <http://pypi.python.org/pypi/setuptools>`_,
  this will attempt to automatically install
  `Jinja2 <http://jinja.pocoo.org>`_
  for you, if it is not already installed.

* disadvantage: you will have to specify the path to your desired
  template file, e.g.::

    relatex.py /path/to/relatex/templates/plos my.tex

