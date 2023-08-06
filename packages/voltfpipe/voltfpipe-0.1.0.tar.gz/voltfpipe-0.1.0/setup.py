# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['voltfpipe']

package_data = \
{'': ['*']}

install_requires = \
['dataclasses-json>=0.5.7,<0.6.0',
 'opencv-python>=4.5.5,<5.0.0',
 'pypsxlib>=0.2.0,<0.3.0',
 'ruamel.yaml>=0.17.21,<0.18.0',
 'simple-term-menu>=1.4.1,<2.0.0',
 'slug>=2.0,<3.0',
 'typer>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['voltfpipe = voltfpipe.cli:app']}

setup_kwargs = {
    'name': 'voltfpipe',
    'version': '0.1.0',
    'description': 'A pipeline manager for a voltf project (photogrammetry and videogrammetry)',
    'long_description': '# voltfpipe\n\nA pipeline manager for a voltf project (photogrammetry and videogrammetry).\n\n# Description\nInitially, can manage raw videos (breaking them up)\n\n# Requirements\n\n`ffmpeg` available on the command line\n\n# Quickstart\n\n## Install\npip install voltfpipe\n\n## How do I ... ?\n\n### Init a project\n\n`voltfpipe init`\n\n### Add a video\n\n`voltfpipe video add path/to/video --project my-project --video my-video-slug` \n\n### Add all  videos in a directory\n\n`voltfpipe videos add path/to/videos/ --project my-project` \n\n### Prepare a video for import \n\n`voltfpipe video configure --project my-project --video my-video-slug`\n\n### Batch Prepare all videos for import \n\n`voltfpipe videos configure --project my-project`\n\nThis will guestimate a lot of settings for each video.\n\n### Create images for a project\n\n`voltfpip images create --project my-project`\n\nImages will be in `my-project/images/`\n\n',
    'author': 'Luke Miller',
    'author_email': 'dodgyville@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/dodgyville/voltfpipe',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
