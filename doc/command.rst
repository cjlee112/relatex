
############################
ReLaTeX Command-line Options
############################



ReLaTeX requires two command-line arguments::

  relatex.py TEMPLATENAME INPUT-PATH [OPTIONS]

* **template name**: This should be the name of a directory
  inside the relatex/templates directory.

* **input latex file path**

Note: by default ReLaTeX writes its output latex file to 
the same directory as your input latex file, with the
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


