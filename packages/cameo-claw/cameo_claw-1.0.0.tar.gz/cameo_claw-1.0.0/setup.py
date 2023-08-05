from setuptools import setup

setup(
    name='cameo_claw',
    version='1.0.0',
    description=
    'Multiprocessing download, filter, streaming. ⚡️FAST⚡️ '
    '2022-04-16 v1.0.0 support cache, support same deviceId append to single .csv.gz'
    '2022-04-16 v0.9.1 support python filelock prevent 6 users crash, fix it_filter mkdir bug',
    release_notes=
    '2022-04-12 v0.8.1 fix mkdir bug'
    '2022-04-12 v0.7.3 no duplicates'
    '2022-04-12 v0.7.20412 add filter group'
    '2022-04-09 v0.6.6 streaming, fix certificate bug, requests verify false'
    '2022-04-08 v0.5.8 no duplicates'
    '2022-04-08 v0.5.7 fix Exception: Could not parse 0.0 as dtype Int64 at column 7.'
    '2022-04-05 v0.5.5 add filter and sort'
    '2022-04-05 v0.5.4 benchmark, 59s, 5MB/s, group by, 50 deviceId, March, ADSL'
    '2022-04-05 v0.5.3 skip polars deprecated warning'
    '2022-04-05 v0.5.2 fix write_csv -> to_csv for python 3.7 bugs'
    '2022-04-05 v0.5.1 fix istarmap for python 3.7 bugs'
    '2022-04-05 v0.5.0 group by dataframe, ready for developers'
    '2022-04-03 v0.4.0 add parameters'
    '2022-04-03 v0.3.0 independent test'
    '2022-04-02 v0.2.0 multiprocessing, download select to parquet'
    '  . polars select and to parquet'
    '  . 51.8s, ADSL, total 44MB parquets, convert to 1533 .parquet files'
    '  . from 453MB .csv.gz, from 2.6GB .csv'
    '2022-04-02 v0.1.1 default processes 25'
    '2022-04-02 v0.1.0 initial',
    url='https://github.com/bohachu/cameo_claw',
    author='Bowen Chiu',
    author_email='bohachu@gmail.com',
    license='BSD 2-clause',
    packages=['cameo_claw'],
    install_requires=[
        'requests',
        'polars',
        'tqdm',
        'fastapi',
        'uvicorn',
        'pandas',
        'filelock'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
)
