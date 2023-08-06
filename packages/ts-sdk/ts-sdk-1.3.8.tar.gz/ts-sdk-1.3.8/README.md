# ts-sdk

Tetrascience Python SDK

## Install

```
pip3 install ts-sdk
```

## Usage

### Init a new protocol

```
ts-sdk init -o <org> -p <protocol-slug> -t <task-script-slug> -f <protocol-folder>
cd <protocol-folder>/task-script
pipenv install --dev
# task-script code modifications...
pipenv run pytest
```

### Upload artifact

```
export TS_ORG=<your-org-slug>
export TS_API_URL=https://api.tetrascience.com/v1
export TS_AUTH_TOKEN=<token>
ts-sdk put <ids|protocol|task-script> <namespace> <slug> <version> <artifact-folder>
```

It's also possible to use the configuration JSON file (`cfg.json`):

```
{
    "api_url": "https://api.tetrascience.com/v1",
    "auth_token": "your-token",
    "org": "your-org",
    "ignore_ssl": false
}
```

Usage: `ts-sdk put <ids|protocol|task-script> <namespace> <slug> <version> <artifact-folder> -c cfg.json`

### IDS Validation

When uploading IDS artifact, validation will be performed using `ts-ids-validator` package.
Validation failures for IDS will be printed on the console.

## Changelog

## v1.3.8

- Internal fixes (secrets handling)

## v1.3.7

- Add `--exclude-folders` argument to `ts-sdk put task-script` that excludes common folders that generally do not need to be part of the uploaded task script (e.g. `.git`, `example-input`, `__tests__`)
- Add local check to prevent uploading artifacts using `ts-sdk put` that would be rejected by the server for being too large
- Improve error messages for adding invalid labels to files

## v1.3.6

- Add new s3 meta:
    - DO_NOT_INHERIT_LABELS
    - CONTENT_CREATED_FROM_FILE_ID

## v1.3.5

- Fix bug where datalake file_key was incorrectly generated

## v1.3.2

- Update `context.write_file()` to validate file upload path
- Fix logging issues
- Improve namespace validation
- Update `print` functionality to be more accurate and group arguments to the same call together
