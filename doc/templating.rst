
###########################
Adding Templates to ReLaTeX
###########################

Overview
--------

You can easily add new templates for ReLaTeX to use.  The basic process is:

* You take an existing latex file you want to use as a template.
  For example, this might be the official latex template provided
  by a scientific journal that you want to submit a paper to.
  You add this to ReLaTeX by simply copying it to
  ``relatex/templates/TEMPLATENAME/template.tex``,
  where ``TEMPLATENAME`` is the name you wish to assign to this
  template.  You should also copy any additional files required
  for this template to work (such as ``.sty`` or ``.cls`` files),
  to that directory.

* You add `Jinja2 <http://jinja.pocoo.org/>`_
  code to the ``template.tex`` template file, telling ReLaTeX
  what content to insert in different parts of the template.

Examples
--------

See the example templates in ``templates/pnas``, ``templates/plos``,
and ``templates/generic``.
You can see them in action in :doc:`tutorial`.
Note that Jinja2 variables are inserted using ``{{ }}`` markers,
and control structures are inserted using ``{% %}`` markers.


ReLaTeX Content Variables
-------------------------

ReLaTeX provides the following variables for insertion anywhere within
your template:

Content variables
.................

* any keyword parameter(s) passed by the ``--param`` command line 
  option.

* **title**: inserts the document title

* **section**: is a dictionary of the named sections in the paper,
  whose keys are section names, and whose associated values
  are the latex content of that section.  It also provides the
  following attribute:

  * **order**: a list of section names, in the order they appeared
    in the input latex file.

  Note that if your input latex file uses the
  ``\begin{abstract}...\end{abstract}``
  construct, its content will be added to this dictionary as
  the section named ``Abstract``.

* **figures**: if ``--extract-figures`` was specified,
  a list of figure objects, each with the following
  attributes.  Otherwise it's an empty list.

  * **imagefile**: file name of the image file.

  * **caption**: the figure caption

  * **options**: the latex ``\begin{figure}`` options provided
    in the input latex file for this figure, if any.

  * **legend**: the text legend associated with this figure.

* **tables**: if ``--extract-figures`` was specified,
  a list of table objects, each with the following
  attributes.  Otherwise it's an empty list.

  * **tabular**: the content of the table itself (i.e. the content
    of its ``tabular`` environment.

  * **columnFormats**: the list of format specification for the set of
    columns, provided in the input latex file for this figure.

  * **legend**: the text legend associated with this table.

Author and Affiliation variables
................................

* **authors**: a list of author objects, each with the following
  attributes:

  * **name**: the Author Name as provided in the input latex file's
    ``\author{}`` list.

  * **get_affiliations(fmt=None, key=None, linker=',')**: returns a 
    string providing a formatted list of affiliations for this author.

    *fmt*, if provided, will be used as a Python format string which
    can contain any of the following fields:
    ``%(id)s``: inserts the number of the affiliation (starting from 1);
    ``%(key)s``: inserts the key character of the affiliation,
    obtained from the optional key character string ``key`` argument.
    ``%(label)s``: inserts the affiliation string from the 
    ``affiliations.txt`` file for this affiliation.
    ``%(labelOnce)s``: same as ``%(label)s``, except that it will
    insert an empty string on subsequent re-usages of the same
    affiliation (required by some journal formats).

    *key*, if provided is a string of characters to use for
    each affiliation (i.e. the first character is used for the
    first affiliation, etc.).

    *linker* is the string used for joining the list of affiliations.

  * **get_marker(role, label)**: returns the string specified by
    **label** if the author has the specified **role**, otherwise
    an empty string.

* **emailAddress**: inserts the corresponding author's email address,
  provided by the ``--email`` option.

* **affiliations**: a list of affiliation objects, each with the
  following attributes:

  * **id**: the number of the affiliation (starting at 1).

  * **label**: the affiliation string from the 
    ``affiliations.txt`` file for this affiliation.

Bibliography variables
......................

* **bibname**: name of the bibliography file (i.e. ``.bib`` file
  name without the ``.bib`` suffix).

* **bibCount**: inserts the largest bibliography number from
  the ``.bbl`` file supplied via the ``--bbl`` option.

* **thebibliography**: inserts the bibliography obtained from
  a ``.bbl`` file supplied via the ``--bbl`` option.


