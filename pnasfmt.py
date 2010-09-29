
import re

def fmt_equations(t):
    'replace wierd Sphinx equation fmt with standard displaymath'
    t = re.sub(r'\\end{split}\\notag\\\\\\begin{split}', '', t)
    t = re.sub(r'\\begin{split}', '', t)
    t = re.sub(r'\\end{split}', '', t)
    t = re.sub(r'\\notag', '', t)
    t = re.sub(r'\\begin{gather}', r'\\[', t)
    t = re.sub(r'\\end{gather}', r'\\]', t)
    return t

def rm_figures(t):
    'remove figures from text; PNAS wants them inserted at the end'
    while True:
        i = t.find(r'\hypertarget')
        if i < 0:
            return t
        j = t[i:].find(r'\end{figure}')
        t = t[:i] + t[i + j + 12:]
    return t

def cleanup_text(t):
    t = fmt_equations(t)
    t = rm_figures(t)
    return t

def get_abstract(t):
    tag = '{Abstract}'
    i = t.index(tag) + len(tag)
    j = t[i:].index(r'\section')
    return t[i:i + j]

def get_title(t):
    return re.search(r'\\title\{([^}]+)', t).group(1)

def get_authors(t):
    l = re.search(r'\\author\{([^}]+)', t).group(1).split(',')
    return [s.strip() for s in l]
    
def get_text(t):
    i = t.index(r'\section')
    j = t.index(r'\bibliography')
    return cleanup_text(t[i:j])

def get_bibliography(path):
    ifile = open(path.split('.')[0] + '.bbl')
    t = ifile.read()
    ifile.close()
    i = t.index(r'\begin{thebibliography}')
    endtag = r'\end{thebibliography}'
    j = t.index(endtag)
    return t[i:j + len(endtag)]

def replace_tag(tag, t, rep):
    i = t.index(tag)
    return t[:i] + rep + t[i + len(tag):]

def insert_bibliography(t, bib):
    i = t.index(r'\begin{thebibliography}{}')
    endtag = r'\end{thebibliography}'
    j = t.index(endtag)
    return t[:i] + bib + t[j + len(endtag):]

def template_fmt(template, authors, title, abstract, text, bib=None,
                 affil='UCLA'):
    'insert our paper sections into the PNAS latex template'
    t = re.sub('insert title here', title, template)
    authorship = []
    for author in authors:
        authorship.append(r'%s\affil{1}{%s}' % (author, affil))
    t = replace_tag(r'\author{}', t, r'\author{' + ',\n'.join(authorship) + '}')
    t = replace_tag('-- enter abstract text here --', t, abstract)
    t = replace_tag('-- text of paper here --', t, text)
    if bib:
        t = insert_bibliography(t, bib)
    # t = re.sub(r'\-\- enter abstract text here \-\-', abstract, t)
    # t = re.sub(r'\-\- text of paper here \-\-', text, t)
    return t

def reformat_file(paperpath, outpath='pnasout.tex',
                  templatepath='pnastmpl.tex', affil='UCLA'):
    'do everything to reformat an input tex file to tex output file for PNAS'
    ifile = open(paperpath)
    latex = ifile.read()
    ifile.close()
    ifile = open(templatepath)
    template = ifile.read()
    ifile.close()
    abstract = get_abstract(latex)
    title = get_title(latex)
    authors = get_authors(latex)
    text = get_text(latex)
    bib = get_bibliography(paperpath)
    ifile = open(outpath, 'w')
    ifile.write(template_fmt(template, authors, title, abstract, text, bib,
                             affil))
    ifile.close()


if __name__ == '__main__':
    import sys
    reformat_file(*sys.argv[1:])
