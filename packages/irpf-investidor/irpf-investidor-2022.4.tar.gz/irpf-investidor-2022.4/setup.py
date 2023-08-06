# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['irpf_investidor']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1', 'pandas>=1.3.5', 'prompt-toolkit>=3.0.24', 'xlrd>=2.0.1']

entry_points = \
{'console_scripts': ['irpf-investidor = irpf_investidor.__main__:main']}

setup_kwargs = {
    'name': 'irpf-investidor',
    'version': '2022.4',
    'description': 'IRPF Investidor',
    'long_description': 'IRPF Investidor\n===============\n\n|PyPI| |Status| |Python Version| |License|\n\n|Read the Docs| |Tests| |Codecov|\n\n|pre-commit| |Black|\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/irpf-investidor.svg\n   :target: https://pypi.org/project/irpf-investidor/\n   :alt: PyPI\n.. |Status| image:: https://img.shields.io/pypi/status/irpf-investidor.svg\n   :target: https://pypi.org/project/irpf-investidor/\n   :alt: Status\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/irpf-investidor\n   :target: https://pypi.org/project/irpf-investidor\n   :alt: Python Version\n.. |License| image:: https://img.shields.io/pypi/l/irpf-investidor\n   :target: https://opensource.org/licenses/MIT\n   :alt: License\n.. |Read the Docs| image:: https://img.shields.io/readthedocs/irpf-investidor/latest.svg?label=Read%20the%20Docs\n   :target: https://irpf-investidor.readthedocs.io/\n   :alt: Read the documentation at https://irpf-investidor.readthedocs.io/\n.. |Tests| image:: https://github.com/staticdev/irpf-investidor/workflows/Tests/badge.svg\n   :target: https://github.com/staticdev/irpf-investidor/actions?workflow=Tests\n   :alt: Tests\n.. |Codecov| image:: https://codecov.io/gh/staticdev/irpf-investidor/branch/main/graph/badge.svg\n   :target: https://codecov.io/gh/staticdev/irpf-investidor\n   :alt: Codecov\n.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n\n\nPrograma auxiliar para calcular custos de ações, ETFs e FIIs. Este programa foi feito para calcular emolumentos, taxa de liquidação e custo total para a declaração de Bens e Direitos do Imposto de Renda Pessoa Física.\n\n**Essa aplicação foi testada e configurada para calcular tarifas referentes aos anos de 2019 a 2021 (IRPF 2020/2022) e não faz cálculos para compra e venda no mesmo dia (Day Trade), contratos futuros e Índice Brasil 50.**\n\n\nRequisitos\n----------\n\n1. Python\n\nInstale na sua máquina o Python 3.8.0 ou superior (versão 3.10 recomendada) para o seu sistema operacional em python.org_.\n\nUsuários do Windows devem baixar a versão `Windows x86-64 executable installer` e na tela de instalação marcar a opção `Add Python 3.8 to PATH`:\n\n.. image:: docs/images/winpath.png\n  :width: 400\n  :alt: Checkbox PATH na instalação Windows\n\n2. Suporte a língua Português (Brasil) no seu sistema operacional.\n\nPode ser instalado no Linux (Debian/Ubuntu) pelo comando:\n\n.. code:: console\n\n   $ apt-get install language-pack-pt-base\n\n\nInstalação\n----------\n\nYou can install *IRPF Investidor* via pip_ from PyPI_:\n\n.. code:: console\n\n   $ pip install irpf-investidor\n\n\nUso\n---\n\n1. Entre na `Área do Investidor`_ da B3, faça login e entre no menu Extratos e Informativos → Negociação de Ativos → Escolha uma corretora e as datas 1 de Janeiro e 31 de Dezembro do ano em que deseja declarar. Em seguida clique no botão “Exportar para EXCEL”. Ele irá baixar o arquivo “InfoCEI.xls”.\n\n**Ainda não é possível rodar o programa usando os novos arquivos XLSX, gerar no formato antigo.**\n\nVocê pode combinar lançamentos de anos diferentes em um mesmo documento colando as linhas de um relatório em outro, mas mantenha a ordem cronológica.\n\n2. Execute o programa através do comando:\n\n.. code:: console\n\n   $ irpf-investidor\n\n\nO programa irá procurar o arquivo "InfoCEI.xls" na pasta atual (digite `pwd` no terminal para sabe qual é) ou na pasta downloads e exibirá na tela os resultados.\n\nAo executar, o programa pede para selecionar operações realizadas em leilão. Essa informação não pode ser obtida nos relatórios da `Área do Investidor` da B3 e precisam ser buscadas diretamente com a sua corretora de valores. Isso afeta o cálculo dos emolumentos e do custo médio.\n\n\nAviso legal (disclaimer)\n------------------------\n\nEsta é uma ferramenta com código aberto e gratuita, com licença MIT. Você pode alterar o código e distribuir, usar comercialmente como bem entender. Contribuições são muito bem vindas. Toda a responsabilidade de conferência dos valores e do envio dessas informações à Receita Federal é do usuário. Os desenvolvedores e colaboradores desse programa não se responsabilizam por quaisquer incorreções nos cálculos e lançamentos gerados.\n\n\nCréditos\n--------\n\nEsse projeto foi gerado pelo template `@cjolowicz`_\'s `Hypermodern Python Cookiecutter`_.\n\n.. _@cjolowicz: https://github.com/cjolowicz\n.. _python.org: https://www.python.org/downloads/\n.. _Área do Investidor: https://www.investidor.b3.com.br/area-do-investidor\n.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n.. _PyPI: https://pypi.org/\n.. _pip: https://pip.pypa.io/\n.. github-only\n.. _Contributor Guide: CONTRIBUTING.rst\n.. _Uso: https://irpf-investidor.readthedocs.io/en/latest/usage.html\n',
    'author': 'staticdev',
    'author_email': 'staticdev-support@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/staticdev/irpf-investidor',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
