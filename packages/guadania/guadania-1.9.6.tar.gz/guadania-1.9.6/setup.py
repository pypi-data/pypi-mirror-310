import setuptools

DESC = 'Libreria que matara vuestro sufrimiento por la PARCA'

setuptools.setup(
    name='guadania',
    description=DESC,
    version='1.9.6',
    packages=[
        'guadania',
        'guadania.prisma'
    ],
    python_requires='>=3.7',
    install_requires=[
        'numpy',
        'openpyxl',
        'pandas',
        'requests'
    ],
)
