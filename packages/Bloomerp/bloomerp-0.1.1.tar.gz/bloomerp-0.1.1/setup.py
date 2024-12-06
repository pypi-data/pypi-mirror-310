from setuptools import find_packages, setup

setup(
    name="Bloomerp",
    version="0.1.1",
    packages=find_packages(),
    include_package_data=True,
    license="MIT License",
    description="Bloomerp is an open source Business Management Software framework that let's you create a fully functioning business management applications by just Django models.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/davidbloomer11/Bloomerp",
    author="David Bloomer",
    author_email="bloomer.david@outlook.com",
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'django>=4.2',
        'requests>=2.0.0',
        'djangorestframework>=3.12.0',
        'django-htmx>=1.0.0',
        'django-formtools>=2.3',
        'Pillow>=8.0.0',
        'psycopg2>=2.8.0',
        'django-crispy-forms>=1.11.0',
        'django-filter>=24.3',
        'xhtml2pdf>=0.2.16',
        'pandas>=2.0.0',
        'openpyxl>=3.1.5',
        'openai>=1.54.1',
        'plotly>=5.0.0'
    ],
    extras_require={
        'images': ['Pillow>=8.0.0'],
    },
)