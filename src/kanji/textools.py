header = r"""\documentclass[a4paper,12pt]{extarticle}
\input{preamble.tex}
\usepackage{CJKutf8}
\usepackage{array}% http://ctan.org/pkg/array
\usepackage{makecell}
\usepackage{longtable}
\begin{document}
"""
ltblend = r"\end{longtable}"
end = r"\end{document}\n"

rowsep = "% Row END\n\\\\ \n%" + "=" * 45 + "\n"

ltbl3 = (
    r"""\begin{longtable}{|lp{6cm}p{4cm}|}
        \multicolumn{1}{c}{\textbf{Kanji}} & \multicolumn{1}{c}{\textbf{Reading}} & \multicolumn{1}{c}{\textbf{Meaning}} \\ \hline
        \endfirsthead

        \multicolumn{1}{c}{\textbf{Kanji}} & \multicolumn{1}{c}{\textbf{Reading}} & \multicolumn{1}{c}{\textbf{Meaning}} \\ \hline
        \endhead

        \hline
        \endfoot

        \hline \hline
        \endlastfoot
"""
    + "\n%"
    + "=" * 45
    + "\n"
)

ltbl6 = (
    r"""\begin{longtable}{|lll|lll|}
        \multicolumn{1}{c}{\textbf{Kanji}} & \multicolumn{1}{c}{\textbf{Reading}} & \multicolumn{1}{c}{\textbf{Meaning}} 
        & \multicolumn{1}{c}{\textbf{Kanji}} & \multicolumn{1}{c}{\textbf{Reading}} & \multicolumn{1}{c}{\textbf{Meaning}} 
        \\ \hline
        \endfirsthead

        \multicolumn{1}{c}{\textbf{Kanji}} & \multicolumn{1}{c}{\textbf{Reading}} & \multicolumn{1}{c}{\textbf{Meaning}}
        & \multicolumn{1}{c}{\textbf{Kanji}} & \multicolumn{1}{c}{\textbf{Reading}} & \multicolumn{1}{c}{\textbf{Meaning}}
        \\ \hline
        \endhead

        \hline
        \endfoot

        \hline \hline
        \endlastfoot
"""
    + "\n%"
    + "=" * 45
    + "\n"
)

ltblhiragana = (
    r"""\begin{longtable}{|lll|lll|}
        \multicolumn{1}{c}{\textbf{Hiragana}} & \multicolumn{1}{c}{\textbf{Reading}} & \multicolumn{1}{c}{\textbf{Hiragana}} 
        & \multicolumn{1}{c}{\textbf{Reading}} & \multicolumn{1}{c}{\textbf{Hiragana}} & \multicolumn{1}{c}{\textbf{Reading}} 
        \\ \hline
        \endfirsthead

        \multicolumn{1}{c}{\textbf{Hiragana}} & \multicolumn{1}{c}{\textbf{Reading}} & \multicolumn{1}{c}{\textbf{Hiragana}} 
        & \multicolumn{1}{c}{\textbf{Reading}} & \multicolumn{1}{c}{\textbf{Hiragana}} & \multicolumn{1}{c}{\textbf{Reading}} 
        \\ \hline
        \endhead

        \hline
        \endfoot

        \hline \hline
        \endlastfoot
"""
    + "\n%"
    + "=" * 45
    + "\n"
)


def entry(fignames, reading, meaning, **kwg):
    """ One table entry for a one column dict
    fignames: figure file names separated by space
    reading: str with hiragana reading
    meaning: str with meaning
    """
    s = "%" + "-" * 20 + "\n"
    s += "% dictionary entry START\n"
    mpgwidth = kwg.get("mpgwidth", 0.3)
    s += f"\\begin{{minipage}}{{{mpgwidth}\\textwidth}}\n"

    fignames = fignames.split(" ")

    s += "\centerline{\n"
    if len(fignames[0]):
        for figname in fignames:
            s += f"\t\includegraphics[width=0.4\\linewidth,]{{{figname}}}\n"
    s += "}\n"

    s += "\\end{minipage}\n&\n"
    s += f"\\begin{{CJK}}{{UTF8}}{{min}}{reading}\\end{{CJK}}"
    skipmeaning = kwg.get("skipmeaning", False)
    if not skipmeaning:
        s += f"\n&\n{meaning}\n"
    s += "% dictionary entry END\n"
    return s


def row(entries):
    """
  entries: list of entries to be joined
  """
    rowstart = "% Row START\n"
    if type(entries) != list:
        raise TypeError(f"entries must bie a list, but are {type(entries)}")
    if len(entries) == 1:
        return rowstart + entries[0] + rowsep

    return rowstart + "\n&\n".join(entries) + rowsep


def generatetex(dictfile, **kws):
    """ generate tex from dictionary csv file """
    import pandas as pd, os

    mydi = pd.read_csv(dictfile)
    rows = [row([entry(*r)]) for i, r in mydi.iterrows()]
    tex = header + ltbl3 + "".join(rows) + ltblend + end
    savepath = kws.get("savepath", os.path.basename(dictfile).split(".")[0] + ".tex")
    with open(savepath, "wb") as f:
        f.write(tex.encode("utf8"))


def generatetex2c(dictfile, **kws):
    """ Generate two-column dict """
    import pandas as pd, numpy as np, os

    mydi = pd.read_csv(dictfile)
    if mydi.shape[0] % 2:
        mydi = pd.concat(
            [mydi, pd.DataFrame([["", "", ""]], columns=["fig", "mean", "read"])],
            ignore_index=True,
        )
    a, _ = mydi.shape
    c = np.arange(a).reshape([2, a // 2]).T

    rows = [
        row(
            [
                (entry(*r, mpgwidth=0.2))
                for r in [mydi.iloc[i].values, mydi.iloc[j].values]
            ]
        )
        for i, j in c
    ]
    tex = header + ltbl6 + "".join(rows) + ltblend + end

    savepath = kws.get("savepath", os.path.basename(dictfile).split(".")[0] + ".tex")
    with open(savepath, "wb") as f:
        f.write(tex.encode("utf8"))
