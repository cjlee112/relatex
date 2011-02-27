from jinja2 import Template
import re
import os
import glob
import sys
import optparse
import shutil

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
    'remove figures from text; many journals want them inserted at the end'
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

def denumber_subsections(t):
    'use if subsections should not be numbered'
    t = re.sub(r'\\subsection{', r'\\subsection*{', t)
    t = re.sub(r'\\subsubsection{', r'\\subsubsection*{', t)
    return t

def cleanup_text(t, denumberSubsections=False):
    t = fmt_equations(t)
    t = cleanup_tables(t)
    t = rm_hrefs(t)
    if denumberSubsections:
        t = denumber_subsections(t)
    return t

class SectionDict(dict):
    def __init__(self, t, tag=r'\section'):
        'return dict of document sections with section names as keys'
        dict.__init__(self)
        i = 0
        l = []
        name = None
        while True:
            try:
                j = t[i:].index(tag)
                if name: # save previous section
                    self[name] = t[i:i + j]
                    l.append(name)
                i += j
            except ValueError:
                if name: # save terminal section
                    self[name] = t[i:]
                    l.append(name)
                break
            i += t[i:].index('{') + 1 # find start & end of section name
            j = t[i:].index('}')
            name = t[i:i + j]
            i += j + 2 # skip past } and newline
        self.order = l # record the original order of the sections

        

def get_title(t):
    return re.search(r'\\title\{([^}]+)', t).group(1)

def get_authors(t):
    names = re.search(r'\\author\{([^}]+)', t).group(1).split(',')
    l = []
    for name in names:
        name = name.strip()
        if name.startswith('and '):
            name = name[4:]
        l.append(Author(name))
    return l

def get_bibname(t):
    return re.search(r'\\bibliography\{([^}]+)', t).group(1)

def read_bbl(bblpath):
    ifile = open(bblpath)
    inBib = False
    bbl = ''
    try:
        for line in ifile:
            if line.startswith(r'\begin{thebibliography}'):
                bibCount = line.split('}')[1][1:]
                inBib = True
            elif line.startswith(r'\end{thebibliography}'):
                inBib = False
            elif inBib:
                bbl += line
    finally:
        ifile.close()
    return bbl, bibCount

def get_text(t, denumberSubsections=False):
    i = t.index(r'\section')
    j = t.index(r'\bibliography')
    return cleanup_text(t[i:j], denumberSubsections)

def append_after_tag(tag, t, rep, nskip=0):
    i = t.index(tag) + len(tag)
    return t[:i - nskip] + rep + t[i:]

class Author(object):
    def __init__(self, name):
        self.name = name
        self.affiliations = []

    def add_affiliation(self, aff):
        self.affiliations.append(aff)

    def get_affiliations(self, fmt=None, key=None, linker=','):
        if fmt: # user-provided format string
            l = []
            for aff in self.affiliations:
                d = dict(id=str(aff.id), label=aff.label, labelOnce=aff.label)
                if aff.alreadyPrinted:
                    d['labelOnce'] = ''
                if key:
                    d['key'] = key[aff.id - 1]
                l.append(fmt % d)
                aff.alreadyPrinted = True
        elif key is None:
            l = [str(aff.id) for aff in self.affiliations]
        else:
            l = [key[aff.id - 1] for aff in self.affiliations]
        return linker.join(l)
            
class Affiliation(object):
    def __init__(self, id, label):
        self.id = id
        self.label = label
        self.alreadyPrinted = False

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
                 bibname, text, tables, figures, **kwargs):
    'insert our paper sections into the latex template'
    section = SectionDict(text) # extract individual sections
    return template.render(title=title, authors=authors,
                           affiliations=affiliations, section=section,
                           bibname=bibname, figures=figures, tables=tables,
                           **kwargs)

def copy_template_files(templatepath, outpath):
    'copy additional template files to same directory as the output'
    templatedir = os.path.dirname(templatepath)
    files = glob.glob(os.path.join(templatedir, '*'))
    outdir = os.path.dirname(outpath)
    if not outdir:
        outdir = os.getcwd()
    for path in files:
        if path != templatepath:
            shutil.copy(path, outdir)

def reformat_file(paperpath, outpath='out.tex',
                  templatepath='template.tex',
                  affiliations='affiliations.txt',
                  copyExtraFiles=True, denumberSubsections=False, **kwargs):
    'do everything to reformat an input tex file into latex template'
    ifile = open(paperpath) # read source latex from sphinx
    latex = ifile.read()
    ifile.close()
    ifile = open(templatepath) # read latex template
    template = Template(ifile.read())
    ifile.close()

    title = get_title(latex) # extract relevant sections from sphinx
    text = get_text(latex, denumberSubsections)
    text, tables = extract_tables(text)
    text, figures = extract_figures(text)
    bibname = get_bibname(latex)
    authors = get_authors(latex)
    affiliations = read_affiliations(affiliations, authors)

    ifile = open(outpath, 'w') # output text inserted into template
    ifile.write(template_fmt(template, title, authors, affiliations,
                             bibname, text, tables, figures, **kwargs))
    ifile.close()
    if copyExtraFiles: # copy extra template files to output directory
        copy_template_files(templatepath, outpath)


def default_outfile(paperpath, templateName):
    return '%s_%s.tex' % (os.path.basename(paperpath).split('.')[0],
                          templateName)

def default_infile(dirs=('_build/latex', 'build/latex')):
    'search for a sphinx-generated latex file'
    for dirpath in dirs:
        if os.path.isdir(dirpath):
            l = glob.glob(os.path.join(dirpath, '*.tex'))
            break
    if len(l) != 1:
        raise ValueError('did not find unique latex source file: ' + str(l))
    return l[0]

def default_template(templateName, filename='template.tex'):
    return os.path.join(sys.path[0], 'templates', templateName, filename)


def get_options():
    parser = optparse.OptionParser()
    parser.add_option(
        '--bbl', action="store", type="string",
        dest="bbl", 
        help="path to .bbl bibliography file")
    parser.add_option(
        '--no-extra-files', action="store_false", dest="copyExtraFiles",
        default=True,
        help='do not copy extra template files to output directory')
    parser.add_option(
        '--no-subsection-numbers', action="store_true",
        dest="denumberSubsections", default=False,
        help='prevent numbering of subsections')
    return parser.parse_args()

if __name__ == '__main__':
    options, args = get_options()
    templateName = args[0]
    args = args[1:]
    templatePath = default_template(templateName)
    try:
        paperpath = args[0]
        args = args[1:]
    except IndexError:
        paperpath = default_infile()
    if options.bbl:
        bbl,bibCount = read_bbl(options.bbl)
    else:
        bbl = bibCount = None
    outpath = default_outfile(paperpath, templateName)
    print 'writing output to', outpath
    reformat_file(paperpath, outpath, templatePath,
                  thebibliography=bbl, bibCount=bibCount,
                  copyExtraFiles=options.copyExtraFiles,
                  denumberSubsections=options.denumberSubsections, *args)
