# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sdd_segmentation']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.0,<2.0.0', 'scipy>=1.7.0,<2.0.0']

setup_kwargs = {
    'name': 'sdd-segmentation',
    'version': '0.1.0a2',
    'description': "The python implementation of algorithm proposed by Z. Wang, 'A New Approach for Segmentation and Quantification of Cells or Nanoparticles,' in IEEE Transactions on Industrial Informatics, vol. 12, no. 3, pp. 962-971, June 2016, DOI: 10.1109/TII.2016.",
    'long_description': '# Slope Difference Distribution Segmentation\n\nThe python implementation of algorithm proposed by Z. Wang, "A New Approach for Segmentation and Quantification of Cells or Nanoparticles," in IEEE Transactions on Industrial Informatics, vol. 12, no. 3, pp. 962-971, June 2016, DOI: 10.1109/TII.2016.\n\n## Description\n\n## Badges\n\nTODO: Add bagdes https://shields.io/\n## Installation\n\nYou can install ``sdd-segmentation`` directly from PyPi via ``pip``:\n\n```bash\n    pip install sdd-segmentation\n```\n\n## Usage\n\n```python\nimport cv2\nfrom sdd_segmentation.sdd import sdd_threshold_selection\n\nimg_np = cv2.imread("image.png")\nT = sdd_threshold_selection(img_np.astype(float), 15)\nprint(T)\nth_image_np = img_np > T[-1]\n```\n\n## License\n\nThis software is licensed under the BSD 3-Clause License.\n\nIf you use this software in your scientific research, please cite our paper:\n\n```bibtex\n\n```\n\nAND original [work](https://doi.org/10.1109/TII.2016.2542043):\n```bibtex\n@ARTICLE{Wang2016,\n    author={Wang, ZhenZhou},\n    journal={IEEE Transactions on Industrial Informatics}, \n    title={A New Approach for Segmentation and Quantification of Cells or Nanoparticles}, \n    year={2016},\n    volume={12},\n    number={3},\n    pages={962-971},\n    doi={10.1109/TII.2016.2542043}\n}\n```\n',
    'author': 'Aleksandr Sinitca',
    'author_email': 'siniza.s.94@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/digiratory/sdd-segmentation',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
