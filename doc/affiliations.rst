
#####################################
Specifying Institutional Affiliations
#####################################

Since different journals may require affiliations to
be formatted somewhat differently, ReLaTeX does not attempt
some kind of universal affiliation transformation method
from your input latex file.
Instead, you give it a separate ``affiliations.txt`` file
that tells it the precise formatted affiliations text
you want to use.  The format is very simple:

* Each line gives a single institutional affiliation.

* You simply type on that line the exact latex string you want
  to appear for that affiliation, followed by a tab-separated
  list of authors that have that affiliation.  Note that
  you can specify an author by giving any unique substring
  of their full name as it appears in the input latex \author{}
  list.  We recommend that you simply give the last name
  of each author (assuming it is unique).

* Affiliations should be given in the order you want them to
  appear in the output.  For example, if the output template
  numbers the affiliation list, the first line in ``affiliations.txt``
  will appear as affiliation 1, etc.

Here is a simple example::

  Institute for Genomics and Proteomics, University of California, Los Angeles, CA, USA	Harper	Machado	Liao	Lee
  Dept. of Human Genetics, University of California, Los Angeles, CA, USA	Chen	Toy	Nelson
  Dept. of Chemical Engineering,  University of California, Los Angeles, CA, USA	Machado	Liao
  Dept. of Chemistry \& Biochemistry,  University of California, Los Angeles, CA, USA	Lee
  Dept. of Computer Science,  University of California, Los Angeles, CA, USA	Lee
  Molecular Biology Institute,  University of California, Los Angeles, CA, USA	Lee

