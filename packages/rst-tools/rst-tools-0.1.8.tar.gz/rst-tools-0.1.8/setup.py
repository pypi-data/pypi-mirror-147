# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rst_tools', 'rst_tools.models']

package_data = \
{'': ['*']}

install_requires = \
['pandas']

setup_kwargs = {
    'name': 'rst-tools',
    'version': '0.1.8',
    'description': 'Rough sets implementation in Python',
    'long_description': '# Guidelines \n\n## Instalation\nTo install this package use pip as following \n\n`pip install rst-tools`\n\n## Usage \n\n### Rough Set (Pawlak\'s Model)\n\n```python\nimport pandas as pd\nfrom rst_tools.models.roughsets import RoughSets as RST\nfrom rst_tools.models.roughsets import QuickReduct as QR\n\ndf = pd.read_csv("YOUR/FILE.csv")\nconditional_attributes = list(df.column.values)\ndecision_attribute = conditional_attributes[-1]\ndel conditional_attributes[-1]\n\nroughsets = RST(df)\nkonsistensi_data = roughsets.konsistensi_tabel(conditional_attributes, decision_attribute)\n\nprint("Konsistensi Data %f" % (konsistensi_data))\n\nqr = QR(roughsets)\nreducts = qr.reduct(decision_attributes, decision_attribute) \n\nprint("Hasil reduksi atribut %s" % (reducts))\n\n\'\'\'....\'\'\'\n```\n\n### Maximum Dependency Attribute (MDA) (Herawan\'s Model)\n\n```python\nimport pandas as pd\nfrom rst_tools.models.maximum_dependency_attributes import MDA\n\n\ndf = pd.read_csv("YOUR/FILE.csv")\nconditional_attributes = list(df.column.values)\ndecision_attribute = conditional_attributes[-1]\ndel conditional_attributes[-1]\n\nmda = MDA(df, attrs=attributes)\nattributes, table = mda.run()\n\nprint(attributes) \n\n\'\'\'....\'\'\'\n```\n\n### Variable Precision Rough Sets (Ziarko\'s Model)\n\n```python\nimport pandas as pd\nfrom rst_tools.models.vprs import VariablePrecisionRoughSet\nfrom rst_tools.models.reduct import reduct\n\n\ndf = pd.read_csv("YOUR/FILE.csv")\nconditional_attributes = list(df.column.values)\ndecision_attribute = conditional_attributes[-1]\ndel conditional_attributes[-1]\n\nrs = vprs(df, b) \nreducts, k, sup_attrs = reduct(rs, attributes, decision)\n\nprint("Konsistensi Data %f" % (k))\nprint("Atribut reduksi %s" % (reducts))\n\n\'\'\'....\'\'\'\n```\n\n### Similarity Rough Sets\n\n```python\nfrom rst_tools.models.similarity import SimilarityRoughSets as SRS \nfrom rst_tools.models.reduct import reduct\nimport pandas as pd \n\ndataset = pd.read_csv("YOUR/FILE.csv")\nattributes = list(dataset.columns.values)\ncond_attrs = attributes\ndec_attr = cond_attrs[-1]\ndel cond_attrs[-1]\n\nprint("alpha ", end="")\nalpha = float(input())\nsrs = SRS(dataset, alpha)\n\nud, R = srs.ind(cond_attrs)\n\n\nsub = srs.subsetU(dec_attr)\n\nk= srs.gamma(cond_attrs, dec_attr)\nalpha= srs.alph(cond_attrs, dec_attr)\nprint(k)\nprint(alpha)\n\n\'\'\'....\'\'\'\n```',
    'author': 'Rofilde Hasudungan',
    'author_email': 'rofilde@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rhsitorus/rst-tools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
