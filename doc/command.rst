
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


