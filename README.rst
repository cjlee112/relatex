ReLaTeX
=======

ReLaTeX is a simple tool for 're-templating' LaTeX documents,
e.g. into the LaTeX template mandated by a specific journal.
It extracts sections, tables, figures, author and affiliation
info, and uses a powerful but simple template system to
make it easy to 'inject' whatever specific pieces needed into
the journal's template.  It gives you flexible control over
many aspects of the LaTeX output, such as the figure options,
renaming and reordering of sections, bibliography injection,
etc.  It also works well for converting Sphinx latex output
(from ReStructuredText input) to whatever journal LaTeX
template you wish.

Examples
--------

A Simple Document
.................

Directory example1 contains a very simple Latex document for 
testing different journal templates.  You can test it as follows::

  cd example1
  python ../relatex.py plos simple.tex --email yogi@cs.technion.ac.il

This inserts the document's contents into the PLoS template, and
outputs it as simple_plos.tex.  You can now generate a PDF in the
usual way, e.g.::

  pdflatex simple_plos.tex
  bibtex simple_plos
  pdflatex simple_plos.tex
  pdflatex simple_plos.tex


A Real Paper
............

Directory example 2 contains a full paper, generated from 
reStructured Text by the Python Sphinx package.  We can test
inserting it into the PNAS and PLoS templates as follows::

  cd example2
  python ../relatex.py pnas test.tex --bbl multihit.bbl

The --bbl option informs relatex of a .bbl bibliography file
that the PNAS template requires (PNAS requires that the bibliography
actually be inserted into the latex document itself; relatex
does this for you).

If you want to insert a different title or author list than
is present in the input file (or if ``relatex`` isn't successfully
finding your title or author list) you can specify them on the
command line using the ``--title`` or ``--authors`` options, e.g.::

  python ../relatex.py pnas test.tex --bbl multihit.bbl --title 'The Art of War: Beyond Memory-one Strategies in Population Games'

Here's another template example, for PLoS::

  python ../relatex.py plos test.tex --no-subsection-numbers --email leec@chem.ucla.edu

PLoS requires the removal of subsection numbering, and also
an email address for the corresponding author; the command-line options
above provide this information.

You then generate PDFs from the resulting test_pnas.tex and
test_plos.tex output files as usual.

