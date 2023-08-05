# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dash_down']

package_data = \
{'': ['*']}

install_requires = \
['dash-extensions==0.1.0rc5',
 'dash-iconify>=0.1.0,<0.2.0',
 'dash-labs>=1.0.3,<2.0.0',
 'dash-mantine-components>=0.7.0,<0.8.0',
 'dash==2.3.1',
 'mistune>=2.0.2,<3.0.0',
 'python-box>=6.0.1,<7.0.0']

setup_kwargs = {
    'name': 'dash-down',
    'version': '0.0.10',
    'description': '',
    'long_description': '[![Unit tests](https://github.com/emilhe/dash-down/actions/workflows/python-test.yml/badge.svg)](https://github.com/emilhe/dash-down/actions/workflows/python-test.yml)\n[![codecov](https://codecov.io/gh/emilhe/dash-down/branch/main/graph/badge.svg?token=kZXx2N1QGY)](https://codecov.io/gh/emilhe/dash-down)\n\nThe `dash-down` module provides tools to convert markdown files into Plotly Dash applications.\n\n## Getting started\n\nMake sure that you have setup [poetry](https://python-poetry.org/). Then run\n\n    poetry install\n\nto install dependencies.\n\n#### Running the example\n\n    poetry run python example.py\n\n#### Running the tests\n\n    poetry run pytest\n\n## Custom content\n\nCustom content is rendered the markdown [directive syntax extension](https://mistune.readthedocs.io/en/latest/directives.html). A directive has the following syntax,\n\n    .. directive-name:: directive value\n       :option-key: option value\n       :option-key: option value\n    \n       full featured markdown text here\n\nwhere the `directive-name` is mandatory, while the `value`, the `options` (specified as key value pairs), and the `text` are optional. \n\n#### What directives are bundled?\n\nCurrently, the bundled directives are\n\n* **api-doc** - a directive for rendering api documentation for a component\n* **dash-proxy** - a block for rendering dash apps (including interactivity)\n\n#### How to create custom directives?\n\nTo create a new directive, simply make a subclass of `DashDirective` and implement the `render_directive` function. Say you want to make a new directive that yields a plot of the `iris` dataset. The code would be along the lines of,\n\n```\nimport plotly.express as px\nfrom dash_down.directives import DashDirective\nfrom dash_extensions.enrich import dcc\n\nclass GraphDirective(DashDirective):\n    def render_directive(self, value, text, options, blueprint):\n        df = getattr(px.data, options.dataset)()\n        fig = px.scatter(df, x=options.x, y=options.y)\n        return dcc.Graph(figure=fig)\n```\n\nThe directive name is derived from the class name by dropping `Directive`, and converting to kebab-case (or you can override the `get_directive_name` function). With this directive defined, you can now create a graph similar to [the one in the Dash docs](https://dash.plotly.com/dash-core-components/graph) with the following syntax,\n\n    .. graph::\n       :dataset: iris\n       :x: sepal_width\n       :y: sepal_length\n\nTo render a markdown file using your new, shiny directive, the syntax would be,\n\n```\nfrom dash_extensions.enrich import DashProxy\nfrom dash_down.express import md_to_blueprint_dmc\n\npath_to_your_md_file = "..."\nblueprint = md_to_blueprint_dmc(path_to_your_md_file, plugins=[GraphDirective()])\n\nif __name__ == \'__main__\':\n    DashProxy(blueprint=blueprint).run_server()\n```\n\nA working example is bundled in the repo (see `example_custom_directive.py`).\n\n#### How to customize the layout of the rendered blueprint?\n\nThe layout of the blueprint returned by the renderer can be customized by passing a custom layout function to the `PluginBlueprint`. A working example is bundled in the repo (see `example_code_renderer.py`).\n\n#### How to customize the markdown rendering itself?\n\nMake a subclass of `DashMantineRenderer` (or `DashHtmlRenderer`, if you prefer to start from raw HTML) and override the render function(s) for any element that you want to change.\n\n#### How to customize the way code is rendered with the DashProxyDirective?\n\nThe `DashProxyDirective` takes optional arguments to customize code rendering. A working example is bundled in the repo (see `example_code_renderer.py`).\n',
    'author': 'emher',
    'author_email': 'emil.h.eriksen@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/emilhe/dash-down',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
