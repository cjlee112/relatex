
######################
Basic ReLaTeX Tutorial
######################

ReLaTeX takes text from your input latex file and "injects"
it into a latex template e.g. a standard latex template for
submitting to a specific scientific journal.  

Examples
--------

A Simple Document
.................

Directory ``example1`` contains a very simple Latex document for 
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

Directory ``example2`` contains a full paper, generated from 
reStructured Text by the Python Sphinx package.  We can test
inserting it into the PNAS and PLoS templates as follows::

  cd example2
  python ../relatex.py pnas test.tex --bbl multihit.bbl

The --bbl option informs relatex of a .bbl bibliography file
that the PNAS template requires (PNAS requires that the bibliography
actually be inserted into the latex document itself; relatex
does this for you).

For PLoS::

  python ../relatex.py plos test.tex --no-subsection-numbers --email leec@chem.ucla.edu

PLoS requires the removal of subsection numbering, and also
an email address for the corresponding author; the command-line options
above provide this information.

You then generate PDFs from the resulting test_pnas.tex and
test_plos.tex output files as usual.

