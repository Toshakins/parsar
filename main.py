from parsy import fail, generate, regex, string, seq

# todo: Doesn't handle !important values

anything = regex(r'[^;]*')
whitespace = regex(r'\s*')
lexeme = lambda p: p << whitespace
iden_token_url = lexeme(string('url'))
open_bracket = lexeme(string('('))
close_bracket = lexeme(string(')'))
hex_digit = regex(r'[0-9a-fA-F]')
escape_digits = regex(r'\\[0-9a-fA-F]{1,6}')
slash = lexeme(string('\\'))
colon = lexeme(string(':'))
semicolon = lexeme(string(';'))
ws = regex(r'\s')
single_quote_mark = lexeme(string('\''))
double_quote_mark = lexeme(string('"'))
background_image_token = lexeme(string('background-image'))
quote_mark = double_quote_mark | single_quote_mark
ident_token = regex('-?-?[a-zA-Z_]+')


@generate
def escape():
    yield slash
    digits = yield escape_digits
    yield ws
    return digits


@generate
def url():
    yield iden_token_url
    yield open_bracket
    open_mark = yield quote_mark
    url = yield regex(r'[^\'\"()\s]+')
    close_mark = yield quote_mark
    if open_mark != close_mark:
        fail('shall enclose url into similar quotation marsk "" or ''')
    yield close_bracket
    return url


@generate
def background_url_declaration():
    rule_name = yield background_image_token
    yield colon
    rule_value = yield url
    return rule_name, rule_value


@generate
def declaration():
    ident_token_name = yield ident_token
    yield colon
    value = yield anything
    return ident_token_name, value


@generate
def _declaration_list():
    ret = yield (declaration | background_url_declaration)
    yield semicolon
    return ret


declaration_list = _declaration_list.many()


def main():
    print(background_url_declaration.parse('background-image : url("ololo")'))


if __name__ == '__main__':
    main()
