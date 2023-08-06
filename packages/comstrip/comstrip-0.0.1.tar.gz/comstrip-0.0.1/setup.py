# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['comstrip']

package_data = \
{'': ['*']}

install_requires = \
['python-Levenshtein>=0.12.2',
 'texttable>=1.6.3',
 'thefuzz>=0.19.0',
 'tiotrap>=0.3']

setup_kwargs = {
    'name': 'comstrip',
    'version': '0.0.1',
    'description': 'Universal Code Comment Stripper and Diff Analysis tools leveraging Emacs Language support',
    'long_description': '## ComStrip\n\nUniversal Code Comment Stripper and Diff Analysis tools leveraging Emacs Language support \n\n### Installation\n\n```\npython3 -m pip install commstrip\n```\n\n### Requirements\n* emacs 28.1+\n* language files for languages that need processing\n\nNote: This code is presently written for Linux and should work out of the box on MacOS and Cygwin but has not been tested there yet. Windows support is planned.\n\n### Create Alias\nAdd to `~/.bashrc`:\n```\nfunction __comstrip {\n\tpython3 /dpool/vcmain/dev/lisp/comstrip/src/comstrip/comstrip.py "$@"\n}\nalias comstrip=\'__comstrip\'\n```\n\n### CLI Usage:\n\n#### CLI - 3-way meld compare\nCompare /r1/src1.py to /r2/src2.py and /r2/src3.py, strip comments, blank lines and trailing spaces and launch in meld\n```\ncomstrip --basedir /dpool/vcmain/dev/lisp/comstrip/test/data --noblank --notrail --meld --file /r1/src1.py /r2/src2.py /r3/src3.py\n```\n\n#### CLI - Stats only\nCompare /r1/src1.py to /r3/src1.py, strip comments, blank lines and trailing spaces and show stats\n```\ncomstrip --basedir /dpool/vcmain/dev/lisp/comstrip/test/data --noblank --notrail --stats --file /r1/src1.py /r3/src2.py\n```\n\nOutput:\n```\nStats: /r1/src1.py <-> /r3/src1.py (/dpool/vcmain/dev/lisp/comstrip/test/data):\n  add_l | mod_l | rem_l | tot_l | tot_chars\n    161 |    25 |    28 |   109 |      7310\n\n  Orig Src    |                       Clean Src                        |  Ok  | Note\n/r1/vtscan.py | /tmp/cs_zz_cs_220420-211346.451785_vtscan_211347211.py | True |    -\n/r3/vtscan.py | /tmp/cs_zz_cs_220420-211346.452998_vtscan_211347429.py | True |    -\n```\n\n#### CLI - Use Meld to troubleshoot stripping of comments etc.\nCall with --meld option and pass only one file Meld will be launched showing the before and after of comment stripping\nThis can be used as you tweak your emacs packages to ensure that the Language processsing is working as expected\n```\ncomstrip --meld --noblank --notrail --file /dpool/vcmain/dev/lisp/comstrip/test/data/r3/src1.py\n```\n\n### Python API Usage:\n* ComStrip - Main API Object\n* DiffStats - Object containging diff information including stats\n* Diff - Representation of two files and contains a `stats:DiffStats` after processing\n* DiffSet - Collection of Diffs for batch processing\n* CSStat - Contains info about Comment Strip Processing: ok, file_in, file_out, message\n\nBecause of overhead of invoking sub-processes, it is best to use API that can process mulitple files in one batch, it is strongly recommended to use `<ComStrip>.process(diffset:DiffSet)` or `<ComStrip>.process(files:list)` to leverage the optimizations in those APIs.\n\nSee `test/hand_tests.py` for implementation of the four API call types: `diffset:DiffSet`, `diff:Diff`, `files:list` and `file:str`.\n\n\n### Debug using VSCode after git checkout\nIf you want to play around without having to install, just do a git checkout of the repo and add to your `.vscode/settings.json`:\n```\n{\n    "python.envFile": "${workspaceFolder}/dev.env"\n}\n```\n\n### TODO:\n[.] Make proper installer for system to get comstrip command working without alias\n[.] Port to Windows\n[.] Verify in Cygwin and MacOs\n[.] Build out proper testing\n[.] Implement leading tab handling',
    'author': 'Timothy C. Quinn',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/comstrip',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.9,<4.0.0',
}


setup(**setup_kwargs)
