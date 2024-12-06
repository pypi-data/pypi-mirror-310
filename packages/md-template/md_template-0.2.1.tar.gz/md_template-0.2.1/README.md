# Markdown Template

[![Project version](https://img.shields.io/pypi/v/md-template?style=flat-square)](https://pypi.python.org/pypi/md-template)
[![Supported python versions](https://img.shields.io/pypi/pyversions/md-template?style=flat-square)](https://pypi.python.org/pypi/md-template)
[![License](https://img.shields.io/github/license/jcwillox/md-template?style=flat-square)](https://github.com/jcwillox/md-template/blob/main/LICENSE)
[![CodeFactor Grade](https://img.shields.io/codefactor/grade/github/jcwillox/md-template?style=flat-square)](https://www.codefactor.io/repository/github/jcwillox/md-template)
[![Code style](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)

A tool to help primarily with generating Markdown tables based on a set of files. This is particularly useful to repositories that contain several subprojects, such as userscript repos.

## Installation

This will install `md-template` and `natsort` as well as `pyyaml` for the userscript preset.

```bash
pip install md-template[full]
```

For the most minimal installation.

```bash
pip install md-template
# or with natsort (recommended)
pip install md-template[natsort]
```

## Usage

**Command-line**

The easiest but most restricted method.

```bash
# md-template --help
md-template table --preset scoop --dry-run
```

**Class-based**

See [table.presets](https://github.com/jcwillox/md-template/blob/main/mdtemplate/table/presets) for more detailed examples.

```python
from pathlib import Path
from typing import Iterable

from mdtemplate.table import TableTemplate


class MyTemplate(TableTemplate):
    files = "bucket/*.json"
    columns = ("Name", "Branch")
    source = "README.md"  # default

    def handle_path(self, path: Path) -> Iterable[Iterable[str]]:
        # create a row
        yield [
            # include information using the current filepath
            f"Column 1: **{path.name}**",
            # use information from the git repository
            f"Column 2: {self.repository.branch}",
        ]


if __name__ == "__main__":
    MyTemplate().parse_args().render()
```

**Function-based**

```python
from pathlib import Path
from typing import Iterable

from mdtemplate.table import TableTemplate


def handle_path(self: TableTemplate, path: Path) -> Iterable[Iterable[str]]:
    # create a row
    yield [
        # include information using the current filepath
        f"Column 1: **{path.name}**",
        # use information from the git repository
        f"Column 2: {self.repository.branch}",
    ]


if __name__ == "__main__":
    TableTemplate(
        files="bucket/*.json",
        columns=("Name", "Branch"),
        source="README.md",  # default
        handle_path=handle_path,
    ).parse_args().render()
```

## Output

Both the class-based and function-based examples above generate the same table.

**Input**

```md
# My Repository

<!-- table -->
| Manifests |
| --------- |

<!-- table-end -->
```
