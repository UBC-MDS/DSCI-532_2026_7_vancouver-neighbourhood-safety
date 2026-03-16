# Contributing to the Vancouver Neighbourhood Safety Dashboard project

This file outlines how to propose changes to the Vancouver Neighbourhood Safety Dashboard project. 

### Fixing typos

Small typos or grammatical errors in documentation may be edited directly using
the GitHub web interface, as long as the changes are made in the _source_ file.

*  Correct: you edit a docstring or comment in a `.py` file below `src/` directory.
*  Incorrect: you edit a generated documentation file, such as a `.html` under `docs/_build/`.

### Prerequisites

Before you make a substantial pull request, you should always file an issue and
make sure someone from the team agrees that it's a problem. If you've found a
bug, create an associated issue and report the issue with enough detail so we can provide help faster.

### Pull request process

*  We recommend that you create a Git branch for each pull request (PR).  
*  New code should follow PEP8 [style guide](https://www.python.org/dev/peps/pep-0008/).

### Code of Conduct

Please note that this project is released with a [Contributor Code of
Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to
abide by its terms.

### M3 Retrospective

## What worked well
- Maintained strong pull request hygiene by configuring branch protection rules that required at least one reviewer before merging into the default branch.
- Broke down complex features into modular tasks with minimal dependencies, allowing team members to work in parallel and reduce development bottlenecks.
- Communicated regularly through GitHub issues and team check-ins, which helped clarify requirements early and ensured steady progress toward milestone goals.

## What did not work well
- Some overlap in functionality developed by different team members resulted in duplicated code instead of shared reusable functions. This highlighted a need for earlier communication around refactoring opportunities and code reuse.
- Task scope and ownership were occasionally unclear, which led to minor rework and delays in integrating features.

### M4 Collaboration Norms

For M4, as a team we agreed to:
- Refactor duplicated logic into reusable functions and organise them within shared utility scripts.
- Write clearer and more descriptive functionality summaries and user stories to ensure requirements are well understood before development begins.
- Communicate frequently to monitor progress, align on shared components, and mention when introducing or updating common functions.

### Attribution
These contributing guidelines were adapted from the [dplyr contributing guidelines](https://github.com/tidyverse/dplyr/blob/master/.github/CONTRIBUTING.md).