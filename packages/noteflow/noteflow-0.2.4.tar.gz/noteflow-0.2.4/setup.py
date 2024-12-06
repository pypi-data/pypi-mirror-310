from setuptools import setup, find_packages

setup(
    name='noteflow',
    version='0.2.4',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'fastapi',
        'uvicorn',
        'markdown-it-py',
        'mdit-py-plugins',
        'requests>=2.31.0',
        'beautifulsoup4>=4.12.0',
        'pydantic',
        'python-multipart',
        'jinja2',
        'platformdirs',
    ],
    entry_points={
        'console_scripts': [
            'noteflow=noteflow.noteflow:main',
        ],
    },
    package_data={
        'noteflow': ['fonts/*', 'static/*'],
    },
) 