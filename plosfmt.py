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

class Figure(object):
    def __init__(self, imagefile, caption, legend, options=''):
        self.imagefile = imagefile
        self.caption = caption
        self.legend = legend
        self.options = options

def save_figure(t, imageOnly=False):
    m = re.search(r'\\includegraphics([^{]*){([^}]+)', t)
    options = m.group(1)
    imagefile = m.group(2)
    if imageOnly:
        return Figure(imagefile, '', '', options)
    tag = r'\caption{'
    i = t.index(tag) + len(tag)
    tag = r'}{\small'
    j = t.index(tag)
    caption = t[i:j]
    k = t.index(r'}\end{figure}')
    legend = re.sub('\n\n', '\n', t[j + len(tag):k]) # caption cannot contain multiple paragraphs
    return Figure(imagefile, caption, legend, options)

def extract_figures(t, legendsOnly=True):
    'remove figures from text; PLoS wants them inserted at the end'
    t = re.sub(r'\\hypertarget{([^}]+)}{}', '', t)
    #t = re.sub(r'\\includegraphics', r'\\includegraphics[width=5in]', t)
    # remove hard-coded Figure labels required by Sphinx
    t = re.sub(r'\\caption{\\textbf{(Figure[^}]+)}: ', r'\\caption{', t)
    figures = []
    while True:
        i = t.find(r'\begin{figure}[htbp]') # which tag occurs first?
        start = t.find(r'\includegraphics')
        if i < 0:
            if start < 0:
                return t, figures # end of figures!!
        elif start < 0 or i < start: # extract normal figure block
            j = t[i:].index(r'\end{figure}') + 12
            figures.append(save_figure(t[i:i + j]))
            t = t[:i] + t[i + j:]
            continue
        j = t[start:].index('}') + 1 # extract bare includegraphics
        figures.append(save_figure(t[start:start + j], True))
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

class Table(object):
    def __init__(self, tabular, columnFormats, caption, legend=''):
        self.tabular = tabular
        self.columnFormats = columnFormats
        self.caption = caption
        self.legend = legend

def extract_tables(t):
    'extract tables from main text, return text and tables separately'
    lastpos = 0
    endTag = r'\end{table}'
    tabularTag = r'\begin{tabular}{'
    s = ''
    tables = []
    while True:
        try:
            i = t[lastpos:].index(r'\begin{table}')
        except ValueError:
            break
        s += t[lastpos:lastpos + i]
        j = t[lastpos + i:].index(endTag) + len(endTag)
        tableStr = t[lastpos + i:lastpos + i + j]
        caption = re.search(r'\\caption\{([^}]+)', tableStr).group(1)
        k = tableStr.index(tabularTag) + len(tabularTag)
        l = tableStr[k:].index('}')
        columnFormats = tableStr[k:k + l]
        m = tableStr[k:].index(r'\end{tabular}')
        tables.append(Table(tableStr[k + l + 1:k + m], columnFormats,
                            caption))
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
