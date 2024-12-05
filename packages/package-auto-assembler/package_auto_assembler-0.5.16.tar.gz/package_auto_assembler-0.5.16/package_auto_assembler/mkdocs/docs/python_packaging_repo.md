## About

A Python Packaging Repository (PPR) is a Git repository with a CI/CD pipeline designed to create and publish Python packages from code pushed to the repository. Using the `package-auto-assembler` tool, PPR can dynamically generate a packaging structure for `.py` files in a highly automated manner. This allows you to publish and maintain multiple packages from a single repository.

In its simplest form, adding a new `.py` file (or modifying an existing one) triggers the CI/CD pipeline to automatically prepare and publish release of new or existing package. Packages can be published to [PyPI](https://pypi.org/) or private storage solutions such as [Azure Artifacts Storage](https://learn.microsoft.com/en-us/azure/devops/artifacts/start-using-azure-artifacts?view=azure-devops).

![publishing-repo-flow](images/package_auto_assembler-usage.png)

*Diagram: Automated flow for packaging and publishing Python packages using PPR.*

### Inputs and Outputs of PPR

PPR produces Python packages with the structure shown below when all optional files are present. You can find more details about these files [here](https://kiril-mordan.github.io/reusables/package_auto_assembler/description/#7-assembling-setup-directory).

Each package can include optional features:

- [Store files](https://kiril-mordan.github.io/reusables/package_auto_assembler/description/#13-adding-artifacts-to-packages) - Include files or links to files within the package.
- [CLI interface](https://kiril-mordan.github.io/reusables/package_auto_assembler/description/#10-adding-cli-interfaces) - Add command-line utilities to the package.
- [FastAPI routes](https://kiril-mordan.github.io/reusables/package_auto_assembler/description/#11-adding-routes-and-running-fastapi-application) - Embed API routes to run FastAPI applications from packages.
- [Streamlit apps](https://kiril-mordan.github.io/reusables/package_auto_assembler/description/#12-adding-ui-and-running-streamlit-application) - Include interactive UIs.
- [MkDocs pages](https://kiril-mordan.github.io/reusables/package_auto_assembler/description/#15-making-simple-mkdocs-site) - Generate simple static documentation websites for each package.

![Publishing Repo Input/Output](images/package_auto_assembler-input_output_files.png)

*Diagram: The structure includes core package files and additional optional components such as CLI interfaces, FastAPI routes, or documentation.*



## Setting up new PPR

A Python Packaging Repository can be created for:
- [GitHub](https://github.com/) with PyPI
- [Azure DevOps](https://azure.microsoft.com/en-us/products/devops) with Azure Artifacts

### Prerequisites

- **New Git Repository:** A repository where the PPR will be set up.
- **Pipeline Permissions:** CI/CD pipelines must have read and write access to commit to the repository.
- **Package Storage:**
    - **GitHub:** A [PyPI](https://pypi.org/) account.
    - **Azure DevOps:** An [Azure Artifacts Feed](https://learn.microsoft.com/en-us/azure/devops/artifacts/concepts/feeds?view=azure-devops).

Only two templates are provided:
- `github + pypi`
- `azure devops + azure artifacts feed`

### Github

1. **Set Up GitHub Pages**:
    - Navigate to `Settings` -> `Pages`.
    - Select "Deploy from a branch," choose the `gh-pages` branch (if it does not exist, create a new branch named `gh-pages`), and set the directory to `/root`. [More details](https://docs.github.com/en/pages/quickstart).

2. **Configure GitHub Actions**:
    - Navigate to `Settings` -> `Actions` -> `General`.
    - Under "Actions permissions," select "Allow all actions and reusable workflows."
    - Under "Workflow permissions," select "Read and write permissions." [More details](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository).

3. **Add PyPI Credentials**:
    - Go to `Settings` -> `Secrets and variables` -> `Actions`.
    - Add `TWINE_USERNAME` and `TWINE_PASSWORD` as secrets. [More details](https://pypi.org/help/#apitoken).

4. **Initialize the Template**:
    - Use `paa` to set up the PPR:
     ``` bash
     paa init-ppr --github
     ```
     
     Or include all optional directories:

     ``` bash
     paa init-ppr --github --full
     ```

    - Edit `.paa.config` if needed
    - Run `paa init-ppr --github` or `paa init-paa` a second time to initialize directories for storing packaging files based on `.paa.config`.

5. **Customize**:
    - Edit `.github/docs/README_base.md` and `.github/tools/update_README.sh` to modify the repository-level README.

Once setup is complete, pushing changes to the `main` will automatically trigger the pipeline to package and publish your Python packages.

### Azure DevOps


1. **Repository Permissions**:
    - Navigate to `Project settings` -> `Repositories` -> `Your Repository`.
    - Set `Contribute` and `Create tag` permissions for `Your project build service` to "Allow"

2. **Set Up Azure Artifacts Feed**:
    - Create an artifacts feed or use an existing one. [More details](https://learn.microsoft.com/en-us/azure/devops/artifacts/quickstarts/python-packages?view=azure-devops&tabs=Windows).


3. **Add Credentials**:
    - Generate a Personal Access Token (`TWINE_USERNAME` and `TWINE_PASSWORD`) with "Read & write" permissions for "Packaging." [More details](https://learn.microsoft.com/en-us/azure/devops/organizations/accounts/use-personal-access-tokens-to-authenticate?view=azure-devops).


4. **Initialize the Template**:
    - Use `paa` to set up the PPR:

    ``` bash
    paa init-ppr --azure
    ```
     
    Or include all optional directories:

    ``` bash
    paa init-ppr --azure --full
    ```

    - Edit `.paa.config` if needed
    - Run `paa init-ppr --azure` or `paa init-paa` a second time to initialize  directories for storing packaging files based on `.paa.config`.
    - Create `.azure/feeds/YOUR_FEED_NAME.yml` files based on `.azure/feeds/example_feed.yml` and remove the example.

5. **Configure the Pipeline**:

    - Navigate to `Pipelines` -> `New pipeline`.
    - Choose `Azure Repos Git` -> `Your Repository`.
    - Select the `main` branch and `.azure/azure-pipelines.yml` to define the pipeline configuration for packaging and publishing.
    - Add `TWINE_USERNAME` and `TWINE_PASSWORD` under "Variables"

6. **Customize**:

    - Edit `.azure/docs/README_base.md` and `.azure/tools/update_README.sh` to modify the repository-level README.

**Note:** Pushing changes to the `main` branch does not necessarily mean that a package will be published. Since multiple feeds can be published from this repository, a **manual trigger** is preferred.

To trigger the workflow:

1. Navigate to `Pipelines` -> `your-packaging-repo-pipeline` -> `Run pipeline`.
2. Select one of the configured upload feeds in the `Upload Feed` dropdown.
3. Specify the package name in the `Package Name` field (use underscores (`_`) instead of hyphens (`-`)).

---

