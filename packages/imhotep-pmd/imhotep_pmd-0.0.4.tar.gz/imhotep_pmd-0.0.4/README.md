# imhotep_pmd

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![CodeQL](https://github.com/tslmy/imhotep_pmd/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/tslmy/imhotep_pmd/actions/workflows/codeql-analysis.yml)

An [Imhotep][i] plugin for [PMD][p], the static analyzer.

[i]: https://github.com/justinabrahms/imhotep
[p]: https://pmd.github.io/

[PMD][p] talks to [Imhotep][i] via the [Static Analysis Results Interchange Format (sarif)][s], which is simply a JSON with a specific schema.

[s]: https://docs.oasis-open.org/sarif/sarif/v2.0/sarif-v2.0.html

## Installation

1. Install [Imhotep][i] itself from [PyPI](https://pypi.org/project/imhotep/), since `imhotep_pmd` is merely a binding/plugin for [Imhotep][i]:
   ```shell
   pip install imhotep
   ```
2. Install `imhotep_pmd` from [PyPI](https://pypi.org/project/imhotep-pmd/):
   ```shell
   pip install imhotep_pmd
   ```
3. Install [PMD][p]. Please refer to their website for instructions.

Unless you've unzipped the [PMD][p] archive file to `~/bin/pmd-bin-6.44.0/`, you'll have to tell `imhotep_pmd` where to find the executable. This can be achieved by providing a `imhotep_pmd.toml` at the root directory of the repo you want to run PMD against. The file should contain this line that specifies the command used to invoke [PMD][p]:

```toml
pmd_command = "~/bin/pmd-bin-6.44.0/bin/run.sh pmd"
```

## Usage

To use the plugin, you'll have to pass a path to the linter in question to the imhotep runtime.

```shell
imhotep --linter imhotep_pmd.plugin:PmdLinter
```

## Demo
Let's take #1 as an example.

```shell
$ imhotep \
   --repo_name="tslmy/imhotep_pmd" \
   --github-username="tslmy" \
   --github-password="$GITHUB_PASSWORD" \
   --pr-number=1 \
   --linter imhotep_pmd.plugin:PmdLinter
```

Screenshots:

| Before | After |
| ------- | --- |
| ![Screen Shot 2022-04-03 at 14 04 45](https://user-images.githubusercontent.com/594058/161449329-7c43d6d8-547e-43a6-ac21-57701cb3b8fd.png) | ![Screen Shot 2022-04-03 at 14 27 11](https://user-images.githubusercontent.com/594058/161449378-6c20f0df-9785-43a0-99da-67a07574bb8e.png) |

## Integrate with Jenkins

This section walks you through the process of setting up a Jenkins job that automatically run PMD and post review comments to new pull requests (PRs) in a specific GitHub repository.

1. Install the Jenkins plugin _[GitHub Pull Request Builder](https://plugins.jenkins.io/ghprb/)_:
   ![GitHub Pull Request Builder](https://user-images.githubusercontent.com/594058/162634529-f8082b88-8496-4255-8c44-704e52c75ad5.png)
2. In GitHub, create a personal access token (PAT):
   ![create a personal access token](https://user-images.githubusercontent.com/594058/162634618-77e1abd6-6627-4188-b7f3-8ce61f24751c.png)
3. In Jenkins, create a freestyle project:
   ![Create a freestyle project](https://user-images.githubusercontent.com/594058/162634486-967e61ab-123f-4ed7-9494-8ca3c05b335f.png)
4. Under _General_, tick _This project is parameterized_, and then add these parameters:
   ![This project is parameterized](https://user-images.githubusercontent.com/594058/162634660-0dc67f43-8002-4f3a-bfcf-009db8786ba8.png)
5. Under _Source Code Management_, tick _Git_, and then configure it like this:
   ![Source Code Management](https://user-images.githubusercontent.com/594058/162634691-e1369516-033d-41f7-8d20-793afb66c92d.png)
6. Under _Build Triggers_, tick _GitHub Pull Request Builder_, and then configure it your way.
   ![Build Triggers](https://user-images.githubusercontent.com/594058/162634735-1ff3ccfc-1e63-44ab-ab7d-d78e6b37f30b.png)
7. Under _Build Environment_, map your GitHub PAT to the environment variable `GITHUB_PASSWORD`:
   ![Build Environment](https://user-images.githubusercontent.com/594058/162634585-99c8060e-6de5-4fd2-b162-fc2f1d710cc2.png)
   If you haven't, you can add the credential to Jenkins like this:
   ![add the credential to Jenkins](https://user-images.githubusercontent.com/594058/162634604-c05070af-c29d-4a4c-a37f-11472f08caf0.png)
8. Under _Build_, add a step _Execute shell_. Populate it with the content of `jenkins.sh`.
9. Your Jenkins jobs should now automatically run PMD and post review comments whenever a PR is opened.
   ![result](https://user-images.githubusercontent.com/594058/162634813-4d03453a-2193-4ac8-a7cd-e30891719b1c.png)

## Development

To upload a new version to PyPI:

```shell
python setup.py sdist bdist_wheel
twine upload dist/*
```
