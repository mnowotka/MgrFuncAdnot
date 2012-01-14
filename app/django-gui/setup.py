from setuptools import setup, find_packages

setup(
    name = "django-gui",
    version = "0.1",
    url = 'https://github.com/mnowotka/MgrFuncAdnot',
    license = '',
    description = "Praca magisterska z bioinformatyki - inteligentna adnotacja funkcjonalna, czesc GUI.",
    author = 'Michal Maciej Nowotka',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    install_requires = ['setuptools'],
)
