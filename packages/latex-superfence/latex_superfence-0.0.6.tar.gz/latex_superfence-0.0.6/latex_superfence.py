import re
import subprocess
import os
import shutil
from functools import partial


def tex_to_svg(source, options):
    dirPath = ".latexTmp"
    os.makedirs(f"{dirPath}", exist_ok=True)
    with open(f"{dirPath}/latex.tex", "w", encoding="utf-8") as f:
        f.write(source)
    try:
        result = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
                "-output-directory", dirPath, f"{dirPath}/latex.tex"],
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(e.output)
        shutil.rmtree(dirPath)
        return f"<pre>{e.output}</pre><pre>{source}</pre>"

    subprocess.run(
        ["pdfcrop", f"{dirPath}/latex.pdf", f"{dirPath}/latex_crop.pdf"],
        capture_output=True,
        text=True,
        check=True
    )
    subprocess.run(
        ["pdf2svg", f"{dirPath}/latex_crop.pdf", f"{dirPath}/latex.svg"],
        capture_output=True,
        text=True,
        check=True
    )
    with open(f"{dirPath}/latex.svg", "rb") as f:
        svg = f.read().decode("UTF8")
    fill = options.get('fill')
    if fill:
        svg = svg.replace("fill:rgb(0%,0%,0%)", f"fill:{fill}")
    stroke = options.get('stroke')
    if stroke:
        svg = svg.replace("stroke:rgb(0%,0%,0%)", f"stroke:{stroke}")
    shutil.rmtree(dirPath)
    return svg


def formatter(**kwargs):
    fill = kwargs.get('fill')
    stroke = kwargs.get('stroke')
    return partial(_fence_latex_format, fill=fill, stroke=stroke)


def _fence_latex_format(
    source, language='latex', class_name='latex', options={}, md=None, preview=False, fill=None, stroke=None, **kwargs
):
    options['fill'] = options.get('fill', fill)
    options['stroke'] = options.get('stroke', stroke)
    pattern = r'^\s*:\w+:\s*\w+.*$'
    source = re.sub(pattern, '', source, flags=re.MULTILINE)
    svg = tex_to_svg(source, options)
    template = f"<p align=center>{svg}</p>"
    return template


def validator(language, inputs, options, attrs, md):
    okay = True
    print(inputs)
    for k, v in inputs.items():
        options[k] = v
    return okay
