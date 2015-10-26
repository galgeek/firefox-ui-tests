## How to contribute
So you want to write code and get it landed in the official Firefox UI Tests repository? Then first fork [our repository](https://github.com/mozilla/firefox-ui-tests) into your own Github account, and create a local clone of it as described in the [installation instructions](https://github.com/mozilla/firefox-ui-tests#installation). The latter will be used to get new features implemented or bugs fixed. Once done and you have the code locally on the disk, you can get started. It's best not to work directly on the master branch, but to create a separate branch for each issue you are working on. That way you can easily switch between different work, and you can update each branch individually with the latest changes on upstream master . Check also our [best practices for Git](http://ateam-bootcamp.readthedocs.org/en/latest/reference/git_github.html).

### Writing Code
Please follow our [Python style guide](http://ateam-bootcamp.readthedocs.org/en/latest/reference/python-style.html), and also test with [pylama](https://pypi.python.org/pypi/pylama). If something is unclear, look at existing code which might help you to understand it better.

### Submitting Patches
When you think the code is ready for review, a pull request should be created on Github. Owners of the repository will watch out for new PR's and review them at regular intervals. For each update to the PR, we automatically run all the tests via [Travis CI](http://travis-ci.org/). If tests are failing, it's best to address the failures before requesting review. Otherwise you can wait for a review. If comments have been given in a review, they have to get integrated. For those changes, a separate commit should be created and pushed to your remote development branch. Don't forget to add a comment in the PR afterward, so everyone gets notified by Github. Keep in mind that reviews can span multiple cycles until the owners are happy with the new code.

## Managing the Repository

### Merging Pull Requests
Once a PR is in its final state it needs to be merged into the upstream master branch. For that please **DO NOT** use the Github merge button! But merge it yourself on the command line. Reason is that we want to have a clean history. Before pushing the changes to upstream master, make sure that all individual commits have been squashed into a single one with a commit message ending with the issue number, e.g. "Fix for broken download behavior (#45)". Also check with `git log` to not push merge commits. Only merge PRs where Travis does not report any failure!

### Versioning
At irregular intervals, we release new versions of Firefox UI Tests. Therefore we make use of milestones in the repository. For each implemented feature or fix, the issue's milestone flag should be set to the next upcoming release. That way it's easier to see what will be part of the next release.

When releasing a new version of Firefox UI ests please ensure to also update the history.md file with all the landed features and bug fixes. You are advised to use the [following issue](https://github.com/mozilla/firefox-ui-tests/issues/303) as template for the new release issue which needs to be filed. Please also check the associated PR for the code changes to be made.