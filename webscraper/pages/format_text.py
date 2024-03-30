def trunc(string):
    return string.replace('(', '').replace(')', '').replace(' ', '_').replace('/', '_').replace(',', '').replace('-', '_').replace('__', '_').lower()