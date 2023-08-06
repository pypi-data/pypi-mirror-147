import re

from typing import Iterable, Optional

from ts_sdk.task.type_hints import Label

# Please keep these regex is sync with:
# https://github.com/tetrascience/ts-sdk-python/blob/main/ts_sdk/task/__util_validation.py
meta_name_reg = re.compile(r'^[0-9a-zA-Z-_+ ]+$')
meta_value_reg = re.compile(r'^[0-9a-zA-Z-_+.,/ ]+$')
tag_reg = re.compile(r'^[0-9a-zA-Z-_+./ ]+$')
label_name_reg = re.compile(r'^[0-9a-zA-Z-_+. ]+$')
label_value_reg = re.compile(r'^[0-9a-zA-Z-_+.,/ ]+$')
string_is_trimmed_reg = re.compile(r'^[^\s](.*[^\s])?$')


def validate_file_meta(meta):
    if meta is None:
        return True
    for k,v in meta.items():
        if not meta_name_reg.match(k):
            raise ValueError(f'Invalid metadata key {k}! Expected pattern: {meta_name_reg.pattern}')
        if not meta_value_reg.match(str(v)):
            raise ValueError(f'Invalid metadata value {v}! Expected pattern: {meta_value_reg.pattern}')
        validate_string_is_trimmed(k)
        validate_string_is_trimmed(v)
    return True
    

def validate_file_tags(tags):
    if tags is None:
        return True
    for t in tags:
        if not tag_reg.match(str(t)):
            raise ValueError(f'Invalid tag {t}! Expected pattern: {tag_reg.pattern}')
    return True


def validate_file_labels(labels: Optional[Iterable[Label]]) -> bool:
    if labels is None:
        return True
    for label in labels:
        if "name" not in label:
            raise ValueError('Label is missing the "name" key.')
        if "value" not in label:
            raise ValueError('Label is missing "value" key.')

        label_name = label["name"]
        label_value = label["value"]
        if label_name_reg.match(str(label_name)) is None:
            raise ValueError(f'Invalid label name "{label_name}"! Expected pattern: "{label_name_reg.pattern}"')
        if label_value_reg.match(str(label_value)) is None:
            raise ValueError(f'Invalid label value "{label_value}"! Expected pattern: "{label_value_reg.pattern}"')
        validate_string_is_trimmed(label_name)
        validate_string_is_trimmed(label_value)
    return True

def validate_string_is_trimmed(s):
    # Need to typecast non-string values to string in order to use the regex
    if type(s) is not str:
        s = str(s)
    if not string_is_trimmed_reg.match(s):
        raise ValueError(f'string \"{s}\" cannot contain leading or trailing spaces!')
    return True
