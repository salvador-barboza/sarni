from sly import Lexer, Parser

class CalcLexer(Lexer):
    tokens = {
      ID,
      PROGRAMA,
      PRINCIPAL,
      # Variables
      VAR,
      INT,
      FLOAT,
      CHAR,
      # Tipos
      ENTERO,
      DECIMAL,
      CARACTER,

      # Funciones
      FUNCION,
      REGRESA,
      MIENTRAS,
      # Condicionales
      SI,
      ENTONCES,
      SINO,
      # Ciclos
      MIENTRAS,
      HAZ,
      DESDE,
      HASTA,
      HACER,

      # Funciones reservadas
      LEE,
      ESCRIBE,
      LETRERO
     }

    ignore = ' \t'
    literals = { '=', '+', '-', '*', '/',
                 '[', ']', '{', '}' '(', ')',
                 ',', ';', '.', ':',
                 '>', '<', '&', '|',
                 "'", '"'
                }

    # Tokens
    PROGRAMA = r'programa'
    PRINCIPAL = r'principal\(\)'
    VAR = r'var'
    INT = r'int'
    FLOAT = r'float'
    CHAR = r'char'
    FUNCION = r'funcion'
    REGRESA = r'regresa'
    SI = r'si'
    ENTONCES = r'entonces'
    SINO = r'sino'
    MIENTRAS = r'mientras'
    HAZ = r'haz'
    DESDE = r'desde'
    HASTA= r'hasta'
    HACER = r'hacer'
    LEE = r'lee'
    ESCRIBE = r'escribe'
    IGUAL = r'=='
    DIFERENTE = r'!='

    @_(r'\".*\"')
    def LETRERO(self, t):
      t.value = t.value
      return t # Ver si jala igual sin la funcion    @_(r'\d+')

    @_(r'[a-zA-Z_][a-zA-Z0-9_]*')
    def ID(self, t):
      t.value = t.value
      return t # Ver si jala igual sin la funcion    @_(r'\d+')

    @_(r'\d+.\d+')
    def DECIMAL(self, t):
      t.value = float(t.value)
      return t

    @_(r'[0-9]+')
    def ENTERO(self, t):
        t.value = int(t.value)
        return t

    @_(r'\'.\'')
    def CARACTER(self, t):
      t.value = t.value[1]
      return t


    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1

class CalcParser(Parser):
    tokens = CalcLexer.tokens

    # precedence = (
    #     ('left', '+', '-'),
    #     ('left', '*', '/'),
    #     ('right', 'UMINUS'),
    #     )

    def __init__(self):
        self.names = { }

    @_('PROGRAMA ID',
       'VAR ')
    def statement(self, p):
      return

    # START exp
    @_('termino',
      'termino "+" exp',
      'termino "-" exp')
    def exp(self, p):
      return
    # END exp

    #START termino
    @_('factor',
      'factor "*" factor',
      'factor "/" factor')
    def termino(self, p):
      return
    #END termino

    # START factor
    @_('"(" expresion ")"',
    'ENTERO',
    'ID',
    '"+" ENTERO',
    '"-" ENTERO',
    '"+" ID',
    '"-" ID')
    def factor(self, p):
      return
    # END factor


    # START expresion
    @_('exp',
       'exp "<" exp',
       'exp ">" exp',
       'exp IGUAL exp',
       'exp DIFERENTE exp',
       'exp "&" exp',
       'exp "|" exp')
    def expresion(self, p):
      return
    #END expresion

    #START ESTATUTO
    @_('asignacion',
      'funciones'
      'lectura'
      'escritura'
      'decision'
      'condicional',
      'no_condicional'
    )
    def estatuto(self, p):
      return
    #END ESTATUTO

    # START BLOQUE
    @_('"{" bloqueaux "}"')
    def bloque(self, p):
      return


    @_('estatuto',
        'estatuto bloqueaux')
    def bloqueaux(self, p):
      return
    #END BLOQUE

    #START ASIGNACION
    @_('ID "=" expresion')
    def asignacion(self, p):
      return
    #END ASIGNACION

    #START LECTURA
    @_('LEE "(" lectura_aux ")" ";"')
    def lectura(self, p):
      return

    @_('ID',
      'expresion'
      'ID "," lectura_aux',
      'expresion "," lectura_aux')
    def lectura_aux(self, p):
      return
    #END LECTURA

    #START ESCRITURA
    @_('ESCRIBE "(" escritura_aux ")" ";"')
    def lectura(self, p):
      return

    @_('ID',
      'expresion'
      'ID "," escritura_aux',
      'expresion "," escritura_aux')
    def escritura_aux(self, p):
      return
    #END ESCRITURA

    #START NO_CONDICIO
    @_('ID "=" expresion')
    def asignacion(self, p):
      return
    #END ASIGNACION

if __name__ == '__main__':
    lexer = CalcLexer()
    parser = CalcParser()
    while True:
        try:
            text = input('calc > ')
        except EOFError:
            break
        if text:
            parser.parse(lexer.tokenize(text))