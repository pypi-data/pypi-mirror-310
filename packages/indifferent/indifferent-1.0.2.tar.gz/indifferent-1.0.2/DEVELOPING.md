# Developing `indifferent`

`indifferent` is intentionally unopinionated so that it remains easy to use and maintain.

## Local development

VS Code is strongly recommended. Install the recommended extensions and use the default Extension settings defined in the repo.

### Install a development version of `indifferent`

The best way to make changes to `indifferent` is to create a simple Python project that invokes your development version in situ.

1. Create a new empty Python project and a virtual environment
1. Install the module using the [editable flag](https://pip.pypa.io/en/stable/topics/local-project-installs/#editable-installs), specifying the location of `indifferent`:

   ```bash
   python3 -m pip -e path/to/indifferent
   ```

1. Make your changes

### Use pytest early and often

Two rules:

1. All functionality must be in a function
1. All functions must have tests

Create a new test file in `tests/` for each function you add.
