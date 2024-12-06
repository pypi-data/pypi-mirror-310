from setuptools import setup, find_packages

setup(
    name='zx-config-manager',
    version='0.2.6',
    author='shallots',
    author_email='shallotsh@gmail.com',
    description='zx-config-manager is a tool for managing configuration files.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://gitee.com/programer/zx-config-manager.git',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'flask>=1.1.1',
        'uwsgi>=2.0.17',
        'APScheduler>=3.6.3'
        ],
    python_requires='>=3.6',
    scripts=['scripts/zx_config_app.py'],
    entry_points={
        'console_scripts': [
            'zx-config-app=scripts.zx_config_app:main',
        ]
    }
)