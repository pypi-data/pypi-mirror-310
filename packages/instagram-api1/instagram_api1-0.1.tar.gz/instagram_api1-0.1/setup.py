from setuptools import setup, find_packages

setup(
    name='instagram_api1',
    version='0.1',
    author='ALMHEB',
    author_email='appasqw107@gmail.com',
    description='مكتبه تخص الانستقرام',
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/AL-MHIB',
    packages=find_packages(), 
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
