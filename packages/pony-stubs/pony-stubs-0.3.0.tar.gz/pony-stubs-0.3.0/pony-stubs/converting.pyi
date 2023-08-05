from typing import Any

from pony.utils import is_ident as is_ident

class ValidationError(ValueError): ...

def check_ip(s: Any) -> Any: ...
def check_positive(s: Any) -> Any: ...
def check_identifier(s: Any) -> Any: ...

isbn_re: Any

def isbn10_checksum(digits: Any) -> Any: ...
def isbn13_checksum(digits: Any) -> Any: ...
def check_isbn(s: Any, convert_to: Any | None = ...) -> Any: ...
def isbn10_to_isbn13(s: Any) -> Any: ...
def isbn13_to_isbn10(s: Any) -> Any: ...

email_re: Any
rfc2822_email_re: Any

def check_email(s: Any) -> Any: ...
def check_rfc2822_email(s: Any) -> Any: ...

date_str_list: Any
date_re_list: Any
time_str: str
time_re: Any
datetime_re_list: Any
month_lists: Any
month_dict: Any

def str2date(s: Any) -> Any: ...
def str2time(s: Any) -> Any: ...
def str2datetime(s: Any) -> Any: ...
def str2timedelta(s: Any) -> Any: ...
def timedelta2str(td: Any) -> Any: ...

converters: Any

def str2py(value: Any, type: Any) -> Any: ...
