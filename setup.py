
"""
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
"""

import warnings

try:
    from setuptools import setup
    # setuptools can automatically install dependencies for you
    install_requires = ['Jinja2']
    has_setuptools = True
except ImportError:
    warnings.warn('Setuptools not found, falling back to distutils')
    from distutils.core import setup
    has_setuptools = False

CLASSIFIERS = """
Development Status :: 3 - Alpha
Operating System :: MacOS :: MacOS X
Operating System :: Microsoft :: Windows :: Windows NT/2000
Operating System :: OS Independent
Operating System :: POSIX
Operating System :: POSIX :: Linux
Operating System :: Unix
Programming Language :: Python
Topic :: Scientific/Engineering
Topic :: Scientific/Engineering :: Bio-Informatics
"""

# split into lines and filter empty ones
CLASSIFIERS = filter(None, CLASSIFIERS.splitlines())

entry_points = {
    'console_scripts': [
        'relatex = relatex.relatex:main',
        ],
    }

def try_install(**kwargs):
    'try to install relatex using setup()'
    setup(
        name = 'relatex',
        version= '0.3',
        description = 'a simple tool for extracting LaTeX content and re-injecting it into a different LaTeX format template',
        long_description = __doc__,
        author = "Christopher Lee",
        author_email='leec@chem.ucla.edu',
        url = 'https://github.com/cjlee112/relatex',
        license = 'New BSD License',
        classifiers = CLASSIFIERS,

        scripts = ['relatex.py'],
        **kwargs
     )

def main():
    if has_setuptools:
        try_install(install_requires=install_requires)
    else:
        try_install()

if __name__ == '__main__':
    main()
