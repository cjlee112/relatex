
############################
ReLaTeX Command-line Options
############################



ReLaTeX requires two command-line arguments::

  relatex.py TEMPLATE INPUT-PATH [OPTIONS]

* **template**: This should be either

  * the name of a directory inside the ``relatex/templates``
    directory, e.g. ``plos``.  This only works if you
    are running ``relatex.py`` directly from the ``relatex``
    source directory.
  * the path to your desired template file,
    e.g. ``/path/to/templates/plos/template.tex``.
    In this case, the name of the directory in which the
    file is located (``plos``) will be taken as the 
    template name.
  * the path to your desired template directory, e.g.
    ``/path/to/templates/plos``, which must contain
    a ``templates.tex`` template file.

* **input latex file path**: path to the LaTeX file to read.

Note: by default ReLaTeX writes its output latex file to 
the current directory, with the
template name appended to its file prefix, i.e. running
the ``pnas`` template on a ``test.tex``
input file will generate a ``test_pnas.tex`` output file.

Note that ReLaTeX also looks for an ``affiliations.txt``
*affiliations* file in the current directory.  For more 
info see :doc:`affiliations`.

In addition, it accepts the following options:

* ``--extract-tables``: some templates (e.g. PLOS) require
  moving all the tables to the end of the paper.  Using
  this option extract all tables from the main text,
  and allows the template to insert them at the end of the paper.
* ``--extract-figures``: some templates (e.g. PLOS) require
  moving all the figures to the end of the paper.  Using
  this option extract all figures from the main text,
  and allows the template to insert them at the end of the paper.
* ``--bbl BBL-PATH``: some templates (e.g. PNAS) require 
  directly inserting the bibliography into the latex file
  (rather than providing a separate ``.bib`` bibliography database).
  ReLaTeX will do this automatically for you if you provide
  the path to a ``.bbl`` file for your input paper (this is
  generated automatically when you run ``bibtex`` on your input paper).

* ``--email ADDRESS``: provide an email address for the corresponding
  author, used by some templates.

* ``--no-extra-files``: by default, ReLaTeX copies additional
  files required by your template (e.g. ``.cls`` and ``.sty`` files)
  into the directory containing your output file, since
  running latex on the output latex file will require these
  files.  You can turn off this behavior with this flag.

* ``--no-subsection-numbers``: some templates (e.g. PLoS)
  require that section numbering be turned off for subsections.
  You can do so using this flag.

* ``--rename OLDNAME:NEWNAME``: you can rename one or more
  sections in your original
  document to the names expected by the journal, by specifying a 
  current section name as OLDNAME, and the name expected by the
  journal as NEWNAME.

* ``--imageoptions IMAGEOPTIONS``: forces ``\includegraphics``
  to use IMAGEOPTIONS as its optional arguments, i.e. in the
  form ``\includegraphics[IMAGEOPTIONS]``.

* ``--merge-citations TAG``: merges any string of
  ``\cite{CITE1} \cite{CITE2}...``
  to be combined in a single expression of the form
  ``TAG{CITE1,CITE2...}``.

* ``--keep-hrefs``: forces relatex to preserve ``\href{}``
  links; by default it strips them, since many journal templates
  do not allow them.

* ``--replace :PATTERN:SUB``: perform global substitution of
  the regular expression ``PATTERN`` to replace it with the
  regular expression ``SUB``; you can use subgroup values in 
  ``SUB`` such as ``\1,\2`` etc.  Note that you can specify any
  separator character you want as the first character of the
  argument string; in the example above it is given as :
  (i.e. a colon).

* ``--param KEY=VALUE``: pass the specified keyword arguments
  to the Jinja2 template, to use as it desires.

An example::

  python /path/to/relatex.py bioinformatics mypaper.tex --email leec@chem.ucla.edu --merge-citations '\citep' --keep-hrefs --imgoptions 'width=9cm' --replace ':\\cite\{:\citep{' --replace ':\\code\{([^}]+)\}:\1' --param shortTitle=Phenoseq --param fundingText='DOE grant DE-FC02-02ER63421' --param shortAuthors='Lee \& Harper'
