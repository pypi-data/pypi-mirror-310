from setuptools import setup, find_packages

setup(
   name='meu_investimento_mn',
   version='0.1',
   packages=find_packages(),
   install_requires=[],
   author='Marina N M',
   author_email='mah.novelli@hotmail.com',
   description='Uma biblioteca para cálculos de investimentos.',
   url='https://github.com/m-novelli/projeto_fiap',
   classifiers=[
       'Programming Language :: Python :: 3',
       'License :: OSI Approved :: MIT License',
       'Operating System :: OS Independent',
   ],
   python_requires='>=3.6',
)