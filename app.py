import ply.lex as lex
import ply.yacc as yacc
from flask import Flask, request, render_template

app = Flask(__name__)

reserved = {
    'import': 'IMPORT',
    'fmt': 'FMT',
    'func': 'FUNC',
    'main': 'MAIN'
}

tokens = [
'IDENTIFIER', 'STRING_LITERAL',
    'LBRACE', 'RBRACE', 'LPAREN', 'RPAREN', 'DOT', 'SEMICOLON',
] + list(reserved.values())
    

t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_DOT = r'\.'
t_SEMICOLON = r';'
t_STRING_LITERAL = r'\".*?\"'

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value.lower(), 'IDENTIFIER')
    return t

t_ignore = ' \t'

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

def p_program(p):
    '''program : import_statement function_definition'''

def p_import_statement(p):
    '''import_statement : IMPORT STRING_LITERAL'''

def p_function_definition(p):
    '''function_definition : FUNC MAIN LPAREN RPAREN block'''

def p_block(p):
    '''block : LBRACE statements RBRACE'''

def p_statements(p):
    '''statements : statement
                  | statement statements'''

def p_statement(p):
    '''statement : expression'''

def p_expression(p):
    '''expression : FMT DOT IDENTIFIER LPAREN expression_list RPAREN'''

def p_expression_list(p):
    '''expression_list : STRING_LITERAL
                       | empty'''

def p_empty(p):
    '''empty :'''

def p_error(p):
    global error_message
    if p:
        error_message = f"Error de sintaxis en '{p.value}'"
    else:
        error_message = "Syntax error at EOF"


error_message = None


def analyze_code(code):
    global error_message
    global symbol_table
    symbol_table = {}  
    error_message = None 
    lexer = lex.lex()
    parser = yacc.yacc()
    lexer.input(code)
    tokens = []
    token_count = {'PR': 0, 'IDENTIFIER': 0, 'STRING': 0, 'SYM': 0}

    try:
        while True:
            tok = lexer.token()
            if not tok:
                break
            token_type = tok.type
            if token_type in reserved.values():
                token_count['PR'] += 1
            elif token_type == 'IDENTIFIER':
                token_count['IDENTIFIER'] += 1
            elif token_type == 'STRING_LITERAL':
                token_count['STRING'] += 1
            else:
                token_count['SYM'] += 1
            tokens.append((tok.type, tok.value, tok.lineno, tok.lexpos))
        result = parser.parse(code)
    except SyntaxError as e:
        error_message = str(e)
        result = None

    return tokens, token_count, result

@app.route('/', methods=['GET', 'POST'])
def index():
    tokens = []
    result = None
    token_count = {}
    syntax_error = None 
    if request.method == 'POST':
        code = request.form['code']
        tokens, token_count, result = analyze_code(code)
        syntax_error = error_message
    return render_template('index.html', tokens=tokens, token_count=token_count, result=result, syntax_error=syntax_error)

if __name__ == '__main__':
    app.run(debug=True)



# import "fmt"

# func main() {
#     fmt.Println("Hola mundo")
# }

