md2html.py
==========

Renders Github Flavored Markdown files to HTML, optionally wrapped in a custom
Jinja2 template.

Has a watch option to watch for filesystem changes. This was the main point of
writing this, and can be used to give near instant previews in combination with
some live reload mechanism, for example _Auto Reload_ in Firefox
(https://addons.mozilla.org/en-US/firefox/addon/auto-reload/).

Written while learning Python, so use at own risk.

Requirements
------------

* watchdog 0.6.0
* Jinja2 2.6
* The _marked_ Markdown parser: https://github.com/chjj/marked.

See _requirements.txt_.

Usage
-----

Minimal usage:

```bash
$ md2html.py hello.md > hello.html
```

Using the `--watch` option to watch given path for changes (only renders files
matching `*.md` and `*.markdown`).

```bash
$ md2html.py --watch .
```

With optional `--output-dir`:

```bash
$ md2html.py --watch --output-dir /tmp .
```

With a custom template file:

```bash
$ md2html.py --template template.html hello.md > hello.html
```

Options
-------

### `--watch`

Watches filesystem for changes, `infile` is treated as a path using this option.

### `--template TEMPLATE`

Wrap rendered HTML in given template. Can be either filesystem path or URL.
Defaults to hotlinking to
https://raw.github.com/dfh/md2html.py/master/templates/default.html

### `--output-dir DIR`

Write output to `DIR`, defaults to `.`.

License
-------

Copyright (c) 2013, David Högberg. (MIT License)

See LICENSE for more information.
