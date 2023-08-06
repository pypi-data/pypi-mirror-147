"""This module defines the CLI."""
import argparse
from pathlib import Path

import jinja2
import yaml

from stenciler import __desc__


def cli():
    """Main function."""
    # Inputs
    parser = argparse.ArgumentParser(__desc__)
    parser.add_argument(
        "-s", "--stencil", help="Path to stencil YAML file.", action="store"
    )
    parser.add_argument("-d", "--data", help="Path to data YAML file.", action="store")
    parser.add_argument(
        "-o",
        "--outdir",
        help="Output directory.",
        action="store",
        default=str(Path.cwd() / "outputs"),
    )
    args = parser.parse_args()
    outdir = Path(args.outdir)
    outdir.mkdir(exist_ok=True, parents=True)

    # Run
    with open(args.data, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    with open(args.stencil, encoding="utf-8") as f:
        template_data = yaml.safe_load(f)
    for fmt, template_str in template_data.items():
        template = jinja2.Template(template_str)
        outpath = outdir / f"{Path(args.data).stem}.{fmt}"
        content = template.render(data)
        with open(outpath, "w", encoding="utf-8") as f:
            f.write(content)
