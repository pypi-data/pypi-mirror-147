# Stenciler

stenciler is a CLI tool for building plaintext artifacts by populating Jinja
templates from YAML files. You can use it in any case where you need to create
one or more different plaintext formats with the same data, e.g. a resume in
`.txt` and `.tex` formats.

## Installation

```shell
pipx install stenciler
```

## Example Usage

Here is an example use case. These files can also be found in the `sample`
directory.

Say you need to build a sample resume in `.txt` and `.tex` formats. First, set up
your data:

```yaml
# resume.yaml
name: Marie Curie
summary: |
    Physicist, chemist, two-time Nobel Prize winner, enjoys long bicycle trips.
awards:
- name: Nobel Prize in Chemistry
  year: 1911
- name: Albert Medal
  year: 1910
- name: Davy Medal
  year: 1903
- name: Nobel Prize in Physics
  year: 1903
```

Now, set up your stencil. This yaml file should have a simple dictionary structure
where the keys are file extensions (e.g. `txt`, `tex`) and the values are Jinja
templates.

```yaml
# stencil.yaml
txt: |
  Name:       {{ name }}

  SUMMARY
  ----------------------------------------------------------------------------------
  {{ summary | replace('\n', ' ') | wordwrap(80) }}

  AWARDS
  ----------------------------------------------------------------------------------
  {% for award in awards %}{{ award.name }}{{ " " * (78 - award.name.__len__()) }}{{ award.year}}
  {% endfor %}
tex: |
  \documentclass{article}
  \begin{document}
  {\huge\centering {{ name }}\\[-0.7\baselineskip]\hrulefill\par}

  \subsection*{Summary}
  {{ summary | replace('\n', ' ') | wordwrap(80) }}

  \subsection*{Education}
  {% for award in awards %}
  \noindent {{ award.name }} \hfill {{ award.year }}
  {% endfor %}

  \end{document}
```

Last, run `stenciler` to generate the output files:

```shell
stenciler --stencil stencil.yaml --data resume.yaml
```

Results:

```
# outputs/resume.txt
Name:       Marie Curie

SUMMARY
----------------------------------------------------------------------------------
Physicist, chemist, two-time Nobel Prize winner, enjoys long bicycle trips.

AWARDS
----------------------------------------------------------------------------------
Nobel Prize in Chemistry                                                      1911
Albert Medal                                                                  1910
Davy Medal                                                                    1903
Nobel Prize in Physics                                                        1903
```

```tex
# outputs/resume.tex
\documentclass{article}
\begin{document}
{\huge\centering Marie Curie\\[-0.7\baselineskip]\hrulefill\par}

\subsection*{Summary}
Physicist, chemist, two-time Nobel Prize winner, enjoys long bicycle trips.

\subsection*{Education}

\noindent Nobel Prize in Chemistry \hfill 1911

\noindent Albert Medal \hfill 1910

\noindent Davy Medal \hfill 1903

\noindent Nobel Prize in Physics \hfill 1903


\end{document}
```

![Screenshot of compiled resume.pdf](sample/outputs/resume_pdf.png "Screenshot")

## Developer Setup

Set up your virtual environment:

```shell
python3 -m venv .venv
```

Assuming `direnv`, set up your `.envrc`:

```shell
# .envrc
PATH_add .venv/bin
PATH_add bin

chmod -R +x bin
```

Allow your env file and install requirements:

```shell
direnv allow
pip install -r dev-requirements.txt
```

Run the test script:

```shell
checks
```
