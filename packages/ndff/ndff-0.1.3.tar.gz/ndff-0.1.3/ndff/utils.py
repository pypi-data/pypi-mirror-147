import re

# good enough test for uri? https://stackoverflow.com/questions/6718633/python-regular-expression-again-match-url
uri_regex = re.compile(r"((https?):((//)|(\\\\))+[\w\d:#@%/;$()~_?\+-=\\\.&]*)", re.MULTILINE | re.UNICODE)
# uri_regex = re.compile(r"((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*", re.MULTILINE | re.UNICODE)
def is_uri(uri_string: str):
    return uri_regex.match(f'{uri_string}')
