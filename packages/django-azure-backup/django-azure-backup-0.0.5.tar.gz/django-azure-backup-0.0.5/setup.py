import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-azure-backup",
    version="0.0.5",
    author="Ajit Mourya",
    author_email="ajit@glib.ai",
    description="postgres backup database with cloud upload.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GlibAI/rewa_backup/",
    packages=setuptools.find_packages(exclude=['main_backup', 'manage.py']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'django-storages[azure]'
    ]
)
