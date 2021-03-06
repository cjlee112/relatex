
######################
Basic ReLaTeX Tutorial
######################

A Gallery of Examples of Re-Templating a Paper
----------------------------------------------

ReLaTeX takes text from your input latex file and "injects"
it into a latex template e.g. a standard latex template for
submitting to a specific scientific journal.  To illustrate,
here's one paper that I've injected into a series of different
templates using ReLaTeX,
going all the way from reStructured Text to latex
templates for different journals:

* I actually wrote the paper in
  `reStructured Text <http://sphinx.pocoo.org/rest.html>`_,
  which can be cross-compiled to latex, HTML, or other formats
  using `Sphinx <http://sphinx.pocoo.org>`_ / Docutils.  Here's the
  `original file <http://people.mbi.ucla.edu/leec/pubs/multihit.txt>`_.

* I stored my references in a BibTex bibliography file
  `multihit.bib <http://people.mbi.ucla.edu/leec/pubs/multihit.bib>`_
  (this file is a generic database, so it
  contains a lot more references than just the ones for this
  paper).

* minor note: Sphinx can produce an
  `HTML version <http://people.mbi.ucla.edu/leec/pubs/multihit_sphinx/multihit.html>`_
  of the paper, including
  equations (thanks to
  `jsMath <http://www.math.union.edu/~dpvc/jsMath/>`_),
  figures, and references (thanks to Marc Harper's
  `citation server <http://citation.marcallenharper.com>`_).
  This is not really relevant to ReLaTeX, but it has its uses
  (e.g. I run Sphinx on my iPad in order to edit / view papers
  directly on the iPad using its built-in web browser).

* Sphinx can also compile this to a latex file.  Here is the
  `latex file <http://people.mbi.ucla.edu/leec/pubs/multihit.tex.txt>`_
  that Sphinx generated, and the resulting
  `PDF output <http://people.mbi.ucla.edu/leec/pubs/multihit.pdf>`_.
  As you can see, this is useful, but it produces latex code that
  is a bit non-standard (e.g. its use of the **gather** and **split**
  environments for equations).  This wouldn't be suitable for
  submission to a journal, since they usually require you
  to submit latex that follows their template exactly.

* I then used ReLaTeX to inject this latex content into the
  PLoS latex template.  PLoS requires the use of this template
  for submitting a paper for production by their journals. Here is
  `the resulting latex <http://people.mbi.ucla.edu/leec/pubs/test_plos.tex.txt>`_
  and the `PDF <http://people.mbi.ucla.edu/leec/pubs/test_plos.pdf>`_
  it produces. Note that this pushes the tables and figures to 
  the end of the output, as required by PLoS' template.

* Here is the
  `production PDF <http://people.mbi.ucla.edu/leec/pubs/Harper2011.pdf>`_
  that PLoS generated from ReLaTeX's output tex file.

* To show that it's easy to inject the paper into another template,
  here is example output using the PNAS production template
  (note that this doesn't include figures, since they are submitted
  as separate files for production):
  `the latex file <http://people.mbi.ucla.edu/leec/pubs/test_pnas.tex.txt>`_
  and the `PDF <http://people.mbi.ucla.edu/leec/pubs/test_pnas.pdf>`_.

Of course, this is more complicated than the typical case
where you just have a latex file and want to inject it into a single
template.  Here are a couple examples showing how easy it is to
do that with ReLaTeX.

A Simple Document
-----------------

Directory ``example1`` contains a very simple Latex document for 
testing different journal templates.  You can test it as follows
on the PLoS template
(the ``--email`` option gives the corresponding author's
email address, required by PLoS)::

  cd example1
  python ../relatex.py plos simple.tex --email yogi@cs.technion.ac.il --extract-figures

This inserts the document's contents into the PLoS template, and
outputs it as ``simple_plos.tex``.  You can now generate a PDF in the
usual way, e.g.::

  pdflatex simple_plos.tex
  bibtex simple_plos
  pdflatex simple_plos.tex
  pdflatex simple_plos.tex


A Real Paper
------------

Directory ``example2`` contains a full paper, generated from 
reStructured Text by the Python Sphinx package.  We can test
inserting it into the PNAS and PLoS templates as follows::

  cd example2
  python ../relatex.py pnas test.tex --bbl multihit.bbl --extract-figures --extract-tables

The ``--bbl`` option informs relatex of a ``.bbl`` bibliography file
that the PNAS template requires (PNAS requires that the bibliography
actually be inserted into the latex document itself; relatex
does this for you).

An example of using the 2015 PLoS template::

  python ~/projects/relatex/relatex.py plos ip_pg.tex --no-subsection-numbers --email leec@chem.ucla.edu --bbl ip_pg.bbl --extract-tables --table-insertions table_insertions.txt --use-packages xspace

* ``--use-packages`` specifies packages that need to be added to the PLOS
  template for your paper to compile.
* ``--table-insertions`` specifies a text file that indicates where each
  table should be re-inserted in the final manuscript.  Each line in
  the file gives a text string in the paper where you want each of
  the figures to be inserted (the figure is inserted immediately before
  the location where the text string is found).

For 2009 PLoS template::

  python ../relatex.py plos test.tex --no-subsection-numbers --email leec@chem.ucla.edu --extract-figures --extract-tables

PLoS requires the removal of subsection numbering, and also
an email address for the corresponding author; the command-line options
above provide this information.

You then generate PDFs from the resulting ``test_pnas.tex`` and
``test_plos.tex`` output files as usual.

Using ReLaTeX with Sphinx
-------------------------

Sphinx configuration: to handle ``cite`` and ``bibliography``
reStructured text commands properly
(generating latex ``\cite`` and ``\bibliography`` output),
you must use the ``bibcite`` Sphinx extension, which you can
obtain from https://bitbucket.org/foobaron/bibcite.

* install (or link) ``bibcite.py`` in your ``sphinx-ext`` directory.
* edit your Sphinx ``conf.py`` config file to
  ensure that ``sphinx-ext`` is added to the Python path,
  and that ``bibcite`` is added to Sphinx's imports, e.g.::

    # If extensions (or modules to document with autodoc) are in another directory,
    # add these directories to sys.path here. If the directory is relative to the
    # documentation root, use os.path.abspath to make it absolute, like shown here.
    sys.path.append(os.path.abspath('sphinx-ext'))

    # -- General configuration -----------------------------------------------------

    # Add any Sphinx extension module names here, as strings. They can be extensions
    # coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
    extensions = ['sphinx.ext.jsmath', 'bibcite']




We recommend you use the ``howto`` Sphinx document style 
(instead of the ``manual`` style, which is more appropriate
for a book format rather than an article format).  

If you don't specify an input file path,
ReLaTeX will look automatically in your ``_build/latex``
directory (where Sphinx writes its latex file).  So you 
can run ReLaTeX by just specifying the template name::

  make latex
  relatex.py pnas --bbl my.bbl --extract-figures --extract-tables

ReLaTeX will write its output in the same directory as the input.

ReLaTeXing a paper for arXiv
----------------------------

arXiv requires that papers written in LaTeX be submitted as
tex files rather than as PDF.  Unfortunately, if your tex file
doesn't fit arXiv's expectations, it will be rejected.
For example, tex files generated by Sphinx require special
packages provided by Sphinx, so arXiv will not accept them,
because arXiv's automatic PDF creation process will fail.
You can solve this problem by ReLaTeXing your tex file to a
generic tex format (with no odd package requirements) that
arXiv will accept::

  python /path/to/relatex.py generic paper.tex --email you@biguniversity.edu 

This produces ``paper_generic.tex``, which you can upload to arXiv.
(You can also ``pdflatex`` and ``bibtex`` it in the usual way).



