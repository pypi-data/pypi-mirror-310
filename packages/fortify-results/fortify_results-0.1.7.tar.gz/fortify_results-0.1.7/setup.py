import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fortify_results",
    version="0.1.7",
    author="Fabio Arciniegas",
    author_email="fabio_arciniegas@trendmicro.com",
    description="Get matching fortify applications and versions, summarize their results and notify.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://https://dsgithub.trendmicro.com/cloudone-common/fortify-results",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts':
        ['fortify-results=fortify_results.fortifyresults:cli'],
    },
    test_suite='nose.collector',
    tests_require=['nose'],
    python_requires='>=3.6',
    install_requires=[
        'requests',
    ]
)
