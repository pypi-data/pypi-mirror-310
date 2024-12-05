# Python Packaging Repository for Github

This repository helps automate the development and deployment of Python packages to PyPI using GitHub workflows.

It is an instance of a Python Packaging Repository (PPR) created using the [`package-auto-assembler`](https://kiril-mordan.github.io/reusables/package_auto_assembler/) packaging tool. The repository is designed to streamline the development cycle of `single-module packages`, taking them from an initial idea to a functional alpha version accessible via [PyPI](https://pypi.org/).

Its highly automated CI/CD pipeline can package multiple packages stored in this repository, requiring as little as a single `.py` file, for basic designs. Learn more about this type of PPR [here](https://kiril-mordan.github.io/reusables/package_auto_assembler/python_packaging_repo/).

---

## Basic usage

### Prepare the Environment

Before developing code within this repository, ensure that the `package-auto-assembler` Python package is installed in your environment:

``` bash
pip install package-auto-assembler
```

### Test-Install a Package

After adding or editing files related to your package, install it locally and ensure it works as expected. Use the `--skip-deps-install` flag if reinstalling dependencies is unnecessary:

``` bash
paa test-install your-package
```

### Push Changes to PPR

When code is ready for release, commit changes, including the package name and a list of changes in your commit messages. Push the changes to a new branch in this repository, then create a pull request to the `main` branch.

``` bash
git commit -m "[your_package] change one; comment about change two"
```

**Note**: Merge files for only one package at a time. The pipeline relies on commit history to determine which package to test and publish.

### Publish a Package

If the test results are satisfactory, merge the pull request with `main`. The pipeline will then:

1. Initialize the packaging process.
2. Prepare the package.
3. Publish it to [PyPI](https://pypi.org/).
4. Update tracking files in `.paa` and README.

If packaging pipeline is successful, latest release will be available from [PyPI](https://pypi.org/).

### Additional Information

To see more CLI tools and options, run:

``` bash
paa --help
```

Or visit [`package-auto-assembler` documentation](https://kiril-mordan.github.io/reusables/package_auto_assembler/).

---