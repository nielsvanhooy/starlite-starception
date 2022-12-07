##############

# NOTE: this is a fork of https://github.com/alex-oleshkevich/starception

All rights to him and the contributors for that repo.

This fork exists to implement starception for starlite: https://github.com/starlite-api/starlite.

Starlite left starlette since version [1.39.0] for there own implementations. 

Therefore the orginal repo doens't work
anymore

Seeing starception was originally built for starlette backed frameworks.
So a fork was needed to make this work with
starlite

Note2 : I will keep the fork in sync with the main repo except for the starlette stuff.

##############

# Starception-starlite

Beautiful exception page for Starlette and FastAPI apps.

![PyPI](https://img.shields.io/pypi/v/starception)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/alex-oleshkevich/starception/Lint%20and%20test)
![GitHub](https://img.shields.io/github/license/alex-oleshkevich/starception)
![Libraries.io dependency status for latest release](https://img.shields.io/librariesio/release/pypi/starception)
![PyPI - Downloads](https://img.shields.io/pypi/dm/starception)
![GitHub Release Date](https://img.shields.io/github/release-date/alex-oleshkevich/starception)

## Installation

Install `starlite-starception` using PIP or poetry:

```bash
pip install starlite_starception
# or
poetry add starlite_starception
```

### With syntax highlight support

If you want to colorize code snippets, install `pygments` library.

```bash
pip install starlite_starception[pygments]
# or
poetry add starlite_starception -E pygments
```

## Screenshot

![image](screenshot.png)

<details>
<summary>Dark theme</summary>
<div>
    <img src="./dark.png">
</div>
</details>

## Features

* secrets masking
* solution hints
* code snippets
* display request info: query, body, headers, cookies
* session contents
* request and app state
* platform information
* environment variables
* syntax highlight
* open paths in editor (vscode only)
* exception chains
* dark theme

The middleware will automatically mask any value which key contains `key`, `secret`, `token`, `password`.

## Quick start

See example application in [examples/](examples/) directory of this repository.

## Usage

Starception will work only in debug mode so don't forget to set `debug=True` for local development.

### Monkey patching Starlette

To replace built-in debug exception handler call `install_error_handler` before you create Starlette instance.
> Currently, this is a recommended approach.

```python
from starlite_starception import install_error_handler
from starlite import Starlite, get


@get("/")
def view() -> None:
    raise TypeError('Oops')


install_error_handler()
app = Starlite(route_handlers=[view])
```

### Using middleware

To render a beautiful exception page you need to install a `StarceptionMiddleware` middleware to your application.


> Note, to catch as many exceptions as possible the middleware has to be the first one in the stack.

```python
import typing

from starlite import Starlite

from starlite_starception import StarceptionMiddleware


async def index_view() -> None:
    raise Exception('Oops, something really went wrong...')


app = Starlite(
    debug=True,
    route_handlers=[index_view],
    middleware=[
        StarceptionMiddleware,
        # other middleware go here
    ]
)
```

## Solution hints

If exception class has `solution` attribute then its content will be used as a solution hint.

```python
class WithHintError(Exception):
    solution = (
        'The connection to the database cannot be established. '
        'Either the database server is down or connection credentials are invalid.'
    )
```

![image](hints.png)

## Opening files in editor

Set your current editor to open paths in your editor/IDE.

```python
from starlite_starception import set_editor

set_editor('vscode')
```

![image](link.png)


> Note, currently only VSCode supported. If you know how to integrate other editors - please PR

### Registering link templates

If your editor is not supported, you can add it by calling `add_link_template` and then selecting it with `set_editor`.

```python
from starlite_starception import set_editor, add_link_template

add_link_template('vscode', 'vscode://file/{path}:{lineno}')
set_editor('vscode')
```

## Credentials

* Look and feel inspired by [Phoenix Framework](https://www.phoenixframework.org/).
* Icons by [Tabler Icons](https://tabler-icons.io/).
