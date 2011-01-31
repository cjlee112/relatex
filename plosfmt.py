from jinja2 import Template
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

def extract_legend(t):
    'extract caption following PLOS production figure legend standard'
    t = re.sub(r'\[htbp\]', '[!ht]', t)
    t = re.sub(r'\\centering', '', t)
    t = re.sub(r'\\includegraphics([^{]*){([^}]+)}', '', t) # rm image
    t = re.sub(r'{\\small', '', t)
    t = re.sub(r'}\\end', '}\n' + r'\\end', t)
    t = re.sub('\n\n', '\n', t) # caption cannot contain multiple paragraphs
    first = True
    while True: # get rid of emphasis
        i = t.find(r'\emph{')
        if i < 0: # done
            break
        j = t.index('}', i)
        if first: # PLOS wants first sentence in bold
            t = t[:i] + r'{\bf ' + t[i + 6:j] + '.' + t[j + 1:]
            first = False
        else:
            t = t[:i] + t[i + 6:j] + t[j + 1:]
    return t + '\n\n'

def extract_figures(t, legendsOnly=True):
    'remove figures from text; PLoS wants them inserted at the end'
    t = re.sub(r'\\hypertarget{([^}]+)}{}', '', t)
    #t = re.sub(r'\\includegraphics', r'\\includegraphics[width=5in]', t)
    t = re.sub(r'\\caption{\\textbf{([^}]+)}: ', r'\\caption{', t)
    figures = ''
    while True:
        i = t.find(r'\begin{figure}[htbp]') # which tag occurs first?
        start = t.find(r'\includegraphics')
        if i < 0:
            if start < 0:
                return t, figures # end of figures!!
        elif start < 0 or i < start: # extract normal figure block
            j = t[i:].index(r'\end{figure}') + 12
            if legendsOnly:
                figures += extract_legend(t[i:i + j])
            else:
                figures += t[i:i + 14] + '[H]' + t[i + 20:i + j] + '\n'
            t = t[:i] + t[i + j:]
            continue
        j = t[start:].index('}') + 1 # extract bare includegraphics
        figures += t[start:start + j] + '\n'
        t = t[:start] + t[start + j:]
    

def cleanup_tables(t):
    t = re.sub('threeparttable', 'table', t) # replace with standard table
    t = re.sub(r'\\begin{table}', r'\\begin{table}[!ht]', t)
    lastpos = 0
    s = '' # replace non-standard tabulary env with standard tabular env
    for m in re.finditer(r'\\begin{tabulary}{\\textwidth}{([^}]+)', t):
        s += t[lastpos:m.start()] + r'\begin{tabular}{' + m.group(1).lower()
        lastpos = m.end()
    t = s + t[lastpos:]
    t = re.sub(r'{tabulary}', r'{tabular}', t) #fix end mark as well
    return t

def extract_tables(t):
    'extract tables from main text, return text and tables separately'
    lastpos = 0
    endTag = r'\end{table}'
    s = tables = ''
    while True:
        try:
            i = t[lastpos:].index(r'\begin{table}')
        except ValueError:
            break
        s += t[lastpos:lastpos + i]
        j = t[lastpos + i:].index(endTag) + len(endTag)
        tables += t[lastpos + i:lastpos + i + j] + '\n'
        lastpos += i + j
    s += t[lastpos:]
    return s, tables
        

def rm_hrefs(t):
    return re.sub(r'\\href{([^}]+)}', '', t)

def cleanup_subsections(t):
    'PLoS subsections should not be numbered'
    t = re.sub(r'\\subsection{', r'\\subsection*{', t)
    t = re.sub(r'\\subsubsection{', r'\\subsubsection*{', t)
    return t

def cleanup_text(t):
    t = fmt_equations(t)
    t = cleanup_tables(t)
    t = rm_hrefs(t)
    t = cleanup_subsections(t)
    return t

def get_section(t, tag):
    i = t.index(tag) + len(tag)
    try:
        j = t[i:].index(r'\section')
    except ValueError:
        return t[i:]
    return t[i:i + j]

def get_title(t):
    return re.search(r'\\title\{([^}]+)', t).group(1)

def get_authors(t):
    names = re.search(r'\\author\{([^}]+)', t).group(1).split(',')
    l = []
    for name in names:
        l.append(Author(name.strip()))
    return l

def get_bibname(t):
    return re.search(r'\\bibliography\{([^}]+)', t).group(1)

def get_text(t):
    i = t.index(r'\section')
    j = t.index(r'\bibliography')
    return cleanup_text(t[i:j])

def append_after_tag(tag, t, rep, nskip=0):
    i = t.index(tag) + len(tag)
    return t[:i - nskip] + rep + t[i:]

class Author(object):
    def __init__(self, name):
        self.name = name
        self.affiliations = []

    def add_affiliation(self, aff):
        self.affiliations.append(aff)

    def get_affiliations(self, key=None, linker=','):
        if key is None:
            return linker.join([str(aff.id) for aff in self.affiliations])
        else:
            return linker.join([key[aff.id - 1] for aff in self.affiliations])
            
class Affiliation(object):
    def __init__(self, id, label):
        self.id = id
        self.label = label

def read_affiliations(filename, authors):
    ifile = open(filename)
    l = []
    try:
        for i,line in enumerate(ifile):
            t = line.strip().split('\t')
            aff = Affiliation(i + 1, t[0])
            for au in t[1:]:
                for author in authors:
                    if au in author.name:
                        author.add_affiliation(aff)
            l.append(aff)
    finally:
        ifile.close()
    return l

def template_fmt(template, title, authors, affiliations,
                 bibname, text, tables, figures,
                 sections=('Abstract', 'Introduction', 'Results',
                           'Discussion', 'Materials and Methods',
                           'Acknowledgments')):
    'insert our paper sections into the PLoS latex template'
    section = {}
    for tag in sections:
        section[tag] = get_section(text, '{' + tag + '}')
    return template.render(title=title, authors=authors,
                           affiliations=affiliations, section=section,
                           bibname=bibname, figures=figures, tables=tables)

def reformat_file(paperpath, outpath='plosout.tex',
                  templatepath='plos_template_cjl.tex',
                  affiliations='affiliations.txt'):
    'do everything to reformat an input tex file to tex output file for PLoS'
    ifile = open(paperpath) # read source latex from sphinx
    latex = ifile.read()
    ifile.close()
    ifile = open(templatepath) # read latex template from PLoS
    template = Template(ifile.read())
    ifile.close()

    title = get_title(latex) # extract relevant sections from sphinx
    text = get_text(latex)
    text, tables = extract_tables(text)
    text, figures = extract_figures(text)
    bibname = get_bibname(latex)
    authors = get_authors(latex)
    affiliations = read_affiliations(affiliations, authors)

    ifile = open(outpath, 'w') # output text inserted into template
    ifile.write(template_fmt(template, title, authors, affiliations,
                             bibname, text, tables, figures))
    ifile.close()


if __name__ == '__main__':
    import sys
    reformat_file(*sys.argv[1:])
