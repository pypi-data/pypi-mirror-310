# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.16.4
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# # Simple Notebook Visualiser
#
# __USE `active_ipynb` tag for cells viewed in Jupytext notebook that are not meant for py file__
#
# Simple notebook visualiser for one or more Jupyter notebooks.
#
# Visualises markdown and code cells, with block size determined by code cell line count and estimated screen line count for markdown cells.

# +
import math
import matplotlib.pyplot as plt
import list_imports
from io import  BytesIO
import base64  
import jupytext
from .text_quality import md_readtime
from pathlib import Path
from .notebook_profiler import process_notebook_file
from pandas import concat, DataFrame

def nb_vis(cell_map, img_file='', linewidth = 5, w=20, gap=None,
           gap_boost=1, gap_colour='lightgrey', retval='',
           wordless=False, minimal=False, header_gap=0.2, dpi=80, **kwargs):
    """Visualise notebook gross cell structure."""

    def get_gap(cell_map):
        """Automatically set the gap value based on overall length"""
        
        def get_overall_length(cell_map):
            """Get overall line length of a notebook."""
            overall_len = 0
            gap = 0
            for i ,(l,t) in enumerate(cell_map):
                #i is number of cells if that's useful too?
                overall_len = overall_len + l
            return overall_len

        max_overall_len = 0
        
        #If we are generating a plot for multiple notebooks, get the largest overall length
        if isinstance(cell_map,dict):
            for k in cell_map:
                _overall_len = get_overall_length(cell_map[k])
                max_overall_len = _overall_len if _overall_len > max_overall_len else max_overall_len
        else:
            max_overall_len = get_overall_length(cell_map)

        #Set the gap at 0.5% of the overall length
        return math.ceil(max_overall_len * 0.01)
        
        
    def plotter(cell_map, x, y, label='', header_gap = 0.2):
        """Plot visualisation of gross cell structure for a single notebook."""

        for _cell_map in cell_map:

            #Add a coloured bar between cells
            if y > 0:
                if gap_colour:
                    plt.plot([y,y+gap],[x,x], gap_colour, linewidth=linewidth)

                y = y + gap
            
            _y = y + _cell_map[0] + 1 #Make tiny cells slightly bigger
            plt.plot([y,_y],[x,x], _cell_map[1], linewidth=linewidth)

            y = _y
    
    x = 1
    y = 0
    
    gap = gap if gap is not None else get_gap(cell_map) * gap_boost
    h = 1+len(cell_map) if not minimal else len(cell_map)*linewidth/dpi
    fig, ax = plt.subplots(figsize=(1200/dpi, h))
    
    if not wordless and not minimal:
        plt.text(0, 0, "\nNotebook quality report")
        
    #Add a registration point to the plot
    plt.plot([0,0],[0,0])
    for k in cell_map:
        if not wordless and not minimal:
            #Plot notebook path
            plt.text(y, x, k)
            x = x + header_gap
        plotter(cell_map[k], x, y, k, header_gap=header_gap)
        x = x + 1

    plt.ioff()
    ax.axis('off')
    plt.gca().invert_yaxis()
    
    if img_file:
        plt.savefig(img_file)
        print(f"Notebook cell type quality chart saved to: {img_file}")
    
    if retval=='fig':
        return fig, ax
    elif retval=='img':
        output = BytesIO()
        plt.savefig(output, format="png")
        plt.close(fig)
        # <img src="data:image/png;base64,{}"/>
        return base64.encodebytes(output.getvalue()).decode()
# -

# Define the colour map for different cell types:

VIS_COLOUR_MAP  = {'markdown':'cornflowerblue', 'code':'pink', 'raw':'orange'}
LINE_WIDTH = 160

# The following function will find one or more notebooks on a path and generate cell maps for each of them. All the cell maps are then passed for visualisation on the same canvas.

# +
import nbformat
import os
import textwrap
from glob import glob

from .notebook_profiler import safe_concat
def nb_big_parse_nb(path='', text_formats=True, raw='', path_filter=None, **kwargs):
    """Parse one or more notebooks on a path."""

    def _count_screen_lines(txt, width=LINE_WIDTH):
        """Count the number of screen lines that an overflowing text line takes up."""
        ll = txt.split('\n')
        _ll = []
        for l in ll:
            # Model screen flow: split a line if it is more than `width` characters long
            _ll=_ll+textwrap.wrap(l, width)
        n_screen_lines = len(_ll)
        return n_screen_lines

    def _nb_big_parse_nb(fn=None, text_formats=True, raw='', **kwargs):
        """Parse a notebook and generate the nb_vis cell map for it."""

        cell_map = []
        imports = []
        text_report = {'reading_time':0}

        if raw:
            nb = raw
        elif fn:
            fmts = ['.ipynb']
            if text_formats:
                fmts = fmts + ['.md', '.Rmd', '.py']
            _fn, fn_ext = os.path.splitext(fn)

            if fn_ext not in fmts or not os.path.isfile(fn):
                # Better to return this as empty and check downstream?
                print(f"fn {fn} is not an readable as a notebook file.")
                return { 'cell_map':{}, 'imports':{}, 'text_report':{}}

            if fn_ext=='.ipynb':
                with open(fn,'r') as f:
                    nb = nbformat.reads(f.read(), as_version=4)
            else:
                nb = jupytext.read(fn)
        else:
            print(f"No raw text or filename?")
            return { 'cell_map':{}, 'imports':{}, 'text_report':{}}

        for cell in nb.cells:
            if cell['cell_type'] not in VIS_COLOUR_MAP:
                continue
            cell_map.append((_count_screen_lines(cell['source']), VIS_COLOUR_MAP[cell['cell_type']]))
            if cell['cell_type']=='code':
                # AST parser breaks on ipython magic, etc
                clean_code = [c for c in cell['source'].split('\n') if not c.startswith(('!','%'))]
                for code in clean_code:
                    try:
                        imports = imports + list_imports.parse(code)
                    except:
                        pass
            elif cell['cell_type']=='markdown':
                text_report['reading_time'] += md_readtime(cell['source'], rounding_override=True, **kwargs)
        if 'rounded_minutes' in kwargs and kwargs['rounded_minutes']:
            if 'reading_time' in text_report:
                text_report['reading_time'] =  math.ceil(text_report['reading_time']/60)
        big_report = process_notebook_file(fn)
        return { 'cell_map':cell_map, 'imports':list(set(imports)),
                 'text_report':text_report, "big_report":big_report }

    def _dir_walker(path='.', exclude = 'default', text_formats=True):
        """Profile all the notebooks in a specific directory, list of directories, or individual files."""

        if exclude == 'default':
            exclude_paths = ['.ipynb_checkpoints', '.git', '__MACOSX']
            exclude_dir = ['.ipynb']  # .ipynb is only excluded if it's a directory
        else:
            exclude_paths = exclude
            exclude_dir = []

        nb_multidir_cell_map = {}
        nb_multidir_imports = {}
        nb_multidir_text_report = {}
        nb_multidir_big_report = {}
        very_big_report_df = DataFrame()

        # Ensure path is a list to handle single paths and lists uniformly
        if isinstance(path, str):
            paths = [Path(p) for p in glob(path)]
        elif isinstance(path, list):
            paths = [Path(p) for p in path]
        else:
            paths = [Path(path)]

        files_to_process = []

        # Separate directories and files
        for p in paths:
            if p.is_dir():
                for fn in sorted(p.rglob("*")):
                    if fn.is_file() and fn.suffix == '.ipynb':
                        if not any(ex in str(fn.parent) for ex in exclude_paths + exclude_dir):
                            files_to_process.append(fn)
            elif p.is_file() and p.suffix == '.ipynb':
                if not any(ex in str(p.parent) for ex in exclude_paths):
                    files_to_process.append(p)

        # Now `files_to_process` contains all relevant files to process
        for fn in files_to_process:
            # Start walking...
            if not set(exclude_paths).intersection(set(fn.parts)):
                # Profile that directory...
                reports = _nb_big_parse_nb(fn, text_formats, **kwargs )
                cell_map = reports['cell_map']
                imports = reports['imports']
                text_report = reports['text_report']
                big_report_df = reports["big_report"]
                big_report=big_report_df.to_dict('records')
                big_report_df["path"] = str(Path(fn).parent)
                big_report_df["name"] = Path(fn).name
                if cell_map:
                    nb_multidir_cell_map = {**nb_multidir_cell_map, fn: cell_map}
                if imports:
                    nb_multidir_imports = {**nb_multidir_imports, fn: imports}
                if text_report:
                    nb_multidir_text_report = {**nb_multidir_text_report, fn: text_report}
                if big_report:
                    nb_multidir_big_report = {**nb_multidir_big_report,  fn: big_report}
                very_big_report_df = safe_concat(
                        [very_big_report_df, big_report_df]
                    )
        return {
            "cell_map": nb_multidir_cell_map,
            "imports": nb_multidir_imports,
            "text_report": nb_multidir_text_report,
            "big_report": nb_multidir_big_report,
            "big_report_df": very_big_report_df,
        }

    # Also: we need to be able to switch on and off which reports are run
    # Need to think about handling this properly e.g. in context of plugins
    if not raw and glob(path):
        reports = _dir_walker(path, text_formats=text_formats)
        cell_map = reports['cell_map']
        imports = reports['imports']
        text_report = reports['text_report']
        big_report = reports["big_report"]
        big_report_df = reports["big_report_df"]
    else:
        reports =  _nb_big_parse_nb(path, text_formats, raw=raw, **kwargs)

        cell_map = {path: reports['cell_map']}
        imports = {path: reports['imports']}
        text_report = {path: reports['text_report']}
        big_report = reports["big_report"]
        big_report_df = reports["big_report_df"]
    return {"cell_map": cell_map,
            "imports": imports,
            "text_report": text_report,
            "big_report": big_report,
            "big_report_df": big_report_df}


def nb_vis_parse_nb(path='.', img_file='', linewidth = 5, w=20, text_formats=True, retval='', raw='', path_filter=None, **kwargs):
    """Do a big parse and then chart the result."""
    reports = nb_big_parse_nb(
        path, text_formats, raw=raw, path_filter=path_filter, **kwargs
    )
    cell_map = reports["cell_map"]
    response = nb_vis(cell_map, img_file, linewidth, w, retval=retval, **kwargs)
    if retval:
        return response

def nb_imports_parse_nb(path='.', text_formats=True,
                        raw='', installed=True, verbose=True):
    """Do a big parse and then print the result."""
    from isort import place_module
    import pkg_resources

    # Returns: STDLIB, THIRDPARTY
    # For python 3.10, we could use: sys.stdlib_module_names

    reports = nb_big_parse_nb(path, text_formats, raw=raw)
    imports = reports["imports"]
    all_packages = []
    third_party = []
    std_lib = []

    x = []
    y = []
    for i in imports:
        packages = [p.split('.')[0] for p in imports[i]]
        all_packages = all_packages + packages

        if verbose:
            print(f"Imports in {i}: {', '.join(packages)}")

        # Scatterplot
        for p in imports[i]:
            # x.append("\n".join(str(i).split("/")))
            # Limit length of filename displayed
            x.append(str(i).split("/")[-1].replace(".ipynb", "")[:40])
            y.append(p)

    fig, ax = plt.subplots(figsize=(20, 10))
    ax.scatter(x = x, y = y)
    plt.xticks(rotation=30, ha='right')
    # Accommodate long filenames
    plt.subplots_adjust(bottom=0.2)
    plt.title('Packages used across notebooks')
    plt.savefig('packages.png')

    all_packages = set(all_packages)

    # stdlib packages
    std_lib = {p for p in all_packages if place_module(p) == "STDLIB"}
    # Project names are defined by a project’s setup script,
    # and they are used to identify projects on PyPI.
    third_party = {p for p in all_packages if place_module(p) == "THIRDPARTY"}
    third_party_packages_required = {pkg_resources.Requirement(p).project_name for p in all_packages if place_module(p) == "THIRDPARTY"}
    if verbose:
        print(f"All imports: {', '.join(all_packages)}")
        print(f"std_lib imports: {', '.join(std_lib)}")
        print(f"Third party imports: {', '.join(third_party)}")
        print(f"Third party projects required: {', '.join(third_party_packages_required)}")
    fails = None
    if installed:
        import importlib

        fails = [p for p in all_packages if p and not importlib.util.find_spec(p)]
        # TO DO  - what was the following supposed to check?
        # maybe dependencies?
        # fails_required = {pkg_resources.Requirement(p).project_name for p in fails}
        if verbose:
            if fails:
                print(f"The following packages cannot be imported: {', '.join(fails)}")
                # print(f"Install the following packages to fix broken imports: {', '.join(fails_required)}")
            else:
                print("All packages can be imported.")

    return (imports, all_packages, std_lib, third_party, fails)

    # For package details:
    # import pkg_resources
    # https://setuptools.pypa.io/en/latest/pkg_resources.html
    # print([p.project_name for p in pkg_resources.working_set])
    # We can also pull out things like package requirements, etc.
    # pkg_resources.working_set.require('pandas')
    # pkg_resources.Requirement('pandas').project_name

from .notebook_profiler import (
    report_template_dir,
    report_template_nb,
    multi_level_reporter,
)

def nb_text_parse_nb(path='.', text_formats=True, reading_rate=100, rounded_minutes=False, raw=''):
    """Parse markdown text in notebook(s)."""
    reports = nb_big_parse_nb(path, text_formats, reading_rate=reading_rate, rounded_minutes=rounded_minutes, raw=raw)
    # print("\nTEXT REPORT\n",reports['text_report'])
    print("\n\nIMPORTS REPORT\n",reports["imports"])
    # print("\n\BIG REPORT\n", reports["big_report"], "\n\n")

    # print(reporter(reports["big_report_df"], report_template_full))
    print(
        multi_level_reporter(
            reports["big_report_df"],
            report_template_dir,
            report_template_nb,
            dir_separator="\n\n---------\n\n"
        )
    )
    # print(reports)


# + tags=["active-ipynb"]
# Test a single notebook mapper:

# + tags=["active-ipynb"]
# TEST_NOTEBOOK = '../Notebook_profile_test.ipynb'

# + tags=["active-ipynb"]
# nb_vis_parse_nb(TEST_NOTEBOOK)

# + tags=["active-ipynb"]
# Test a plot of multiple notebooks down a path:

# + tags=["active-ipynb"]
# TEST_DIR = '../../tm351/Part 02 Notebooks'
# nb_vis_parse_nb('../../tm351/Part 02 Notebooks',
#                 linewidth=10, gap_colour='white', gap=1, img_file='test-nbvis.png')

# + tags=["active-ipynb"]
# nb_vis_parse_nb('../Documents/GitHub/tm351-undercertainty/notebooks/tm351/Part 02 Notebooks',
#                 linewidth=10, gap=0, img_file='test-nbvis.png')

# + tags=["active-ipynb"]
# Can we see the saved test file?
#
# ![](test-nbvis.png)
