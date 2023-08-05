# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vcspull', 'vcspull.cli']

package_data = \
{'': ['*']}

install_requires = \
['click>=7', 'colorama>=0.3.9', 'kaptan', 'libvcs>=0.12.0b31,<0.13.0']

entry_points = \
{'console_scripts': ['vcspull = vcspull:cli.cli']}

setup_kwargs = {
    'name': 'vcspull',
    'version': '1.12.0b19',
    'description': 'synchronize your projects via yaml / json files',
    'long_description': '# $ vcspull &middot; [![Python Package](https://img.shields.io/pypi/v/vcspull.svg)](https://pypi.org/project/vcspull/) [![License](https://img.shields.io/github/license/vcs-python/vcspull.svg)](https://github.com/vcs-python/vcspull/blob/master/LICENSE) [![Code Coverage](https://codecov.io/gh/vcs-python/vcspull/branch/master/graph/badge.svg)](https://codecov.io/gh/vcs-python/vcspull)\n\nSynchronize repos in bulk from JSON or YAML file. Compare to\n[myrepos](http://myrepos.branchable.com/). Built on [libvcs](https://github.com/vcs-python/libvcs)\n\nGreat if you use the same repos at the same locations across multiple\nmachines or want to clone / update a pattern of repos without having to\n`cd` into each one.\n\n- clone /update to the latest repos with `$ vcspull`\n- use filters to specify a location, repo url or pattern in the\n  manifest to clone / update\n- supports svn, git, hg version control systems\n- automatically checkout fresh repositories\n- supports [pip](https://pip.pypa.io/)-style URL\'s\n  ([RFC3986](https://datatracker.ietf.org/doc/html/rfc3986)-based [url\n  scheme](https://pip.pypa.io/en/latest/topics/vcs-support/))\n\nSee the [documentation](https://vcspull.git-pull.com/), [configuration](https://vcspull.git-pull.com/configuration/) examples, and [config generators](https://vcspull.git-pull.com/configuration/generation.html).\n\n# how to\n\n## install\n\n```console\n$ pip install --user vcspull\n```\n\n### Developmental releases\n\nYou can test the unpublished version of vcspull before its released.\n\n- [pip](https://pip.pypa.io/en/stable/):\n\n  ```console\n  $ pip install --user --upgrade --pre vcspull\n  ```\n\n- [pipx](https://pypa.github.io/pipx/docs/):\n\n  ```console\n  $ pipx install --suffix=@next \'vcspull\' --pip-args \'\\--pre\' --force\n  ```\n\n  Then use `vcspull@next sync [config]...`.\n\n## configure\n\nadd repos you want vcspull to manage to `~/.vcspull.yaml`.\n\n_vcspull does not currently scan for repos on your system, but it may in\nthe future_\n\n```yaml\n~/code/:\n  flask: "git+https://github.com/mitsuhiko/flask.git"\n~/study/c:\n  awesome: "git+git://git.naquadah.org/awesome.git"\n~/study/data-structures-algorithms/c:\n  libds: "git+https://github.com/zhemao/libds.git"\n  algoxy:\n    repo: "git+https://github.com/liuxinyu95/AlgoXY.git"\n    remotes:\n      tony: "git+ssh://git@github.com/tony/AlgoXY.git"\n```\n\n(see the author\'s\n[.vcspull.yaml](https://github.com/tony/.dot-config/blob/master/.vcspull.yaml),\nmore [configuration](https://vcspull.git-pull.com/configuration.html))\n\n`$HOME/.vcspull.yaml` and `$XDG_CONFIG_HOME/vcspull/` (`~/.config/vcspull`) can\nbe used as a declarative manifest to clone you repos consistently across\nmachines. Subsequent syncs of nitialized repos will fetch the latest commits.\n\n## clone / update your repos\n\n```console\n$ vcspull\n```\n\nKeep nested VCS repositories updated too, lets say you have a mercurial\nor svn project with a git dependency:\n\n`external_deps.yaml` in your project root, (can be anything):\n\n```yaml\n./vendor/:\n  sdl2pp: "git+https://github.com/libSDL2pp/libSDL2pp.git"\n```\n\nclone / update repos:\n\n```console\n$ vcspull sync -c external_deps.yaml\n```\n\nSee the [Quickstart](https://vcspull.git-pull.com/quickstart.html) for\nmore.\n\n## pulling specific repos\n\nhave a lot of repos?\n\nyou can choose to update only select repos through\n[fnmatch](http://pubs.opengroup.org/onlinepubs/009695399/functions/fnmatch.html)\npatterns. remember to add the repos to your `~/.vcspull.{json,yaml}`\nfirst.\n\nThe patterns can be filtered by by directory, repo name or vcs url.\n\n```console\n// any repo starting with "fla"\n$ vcspull sync "fla*"\n// any repo with django in the name\n$ vcspull sync "*django*"\n\n// search by vcs + url\n// since urls are in this format <vcs>+<protocol>://<url>\n$ vcspull sync "git+*"\n\n// any git repo with python in the vcspull\n$ vcspull sync "git+*python*\n\n// any git repo with django in the vcs url\n$ vcspull sync "git+*django*"\n\n// all repositories in your ~/code directory\n$ vcspull sync "$HOME/code/*"\n```\n\n<img src="https://raw.githubusercontent.com/vcs-python/vcspull/master/docs/_static/vcspull-demo.gif" class="align-center" style="width:45.0%" alt="image" />\n\n# Donations\n\nYour donations fund development of new features, testing and support.\nYour money will go directly to maintenance and development of the\nproject. If you are an individual, feel free to give whatever feels\nright for the value you get out of the project.\n\nSee donation options at <https://git-pull.com/support.html>.\n\n# More information\n\n- Python support: >= 3.9, pypy\n- VCS supported: git(1), svn(1), hg(1)\n- Source: <https://github.com/vcs-python/vcspull>\n- Docs: <https://vcspull.git-pull.com>\n- Changelog: <https://vcspull.git-pull.com/history.html>\n- API: <https://vcspull.git-pull.com/api.html>\n- Issues: <https://github.com/vcs-python/vcspull/issues>\n- Test Coverage: <https://codecov.io/gh/vcs-python/vcspull>\n- pypi: <https://pypi.python.org/pypi/vcspull>\n- Open Hub: <https://www.openhub.net/p/vcspull>\n- License: [MIT](https://opensource.org/licenses/MIT).\n\n[![Docs](https://github.com/vcs-python/vcspull/workflows/docs/badge.svg)](https://vcspull.git-pull.com) [![Build Status](https://github.com/vcs-python/vcspull/workflows/tests/badge.svg)](https://github.com/vcs-python/vcspull/actions?query=workflow%3A%22tests%22)\n',
    'author': 'Tony Narlock',
    'author_email': 'tony@git-pull.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://vcspull.git-pull.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
