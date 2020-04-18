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
      VOID,

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
      LETRERO,

      # Operadores
      IGUAL,
      DIFERENTE
     }

    ignore = ' \t'
    literals = { '=', '+', '-', '*', '/',
                 '[', ']', '{', '}', '(', ')',
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
    VOID = r'void'
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
    start = 'programa'

    def __init__(self):
        self.names = { }

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
      'funciones',
      'lectura',
      'escritura',
      'decision',
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
      'expresion',
      'ID "," lectura_aux',
      'expresion "," lectura_aux')
    def lectura_aux(self, p):
      return
    #END LECTURA

    #START ESCRITURA
    @_('ESCRIBE "(" escritura_aux ")" ";"')
    def escritura(self, p):
      return

    @_('ID',
      'expresion',
      'ID "," escritura_aux',
      'expresion "," escritura_aux')
    def escritura_aux(self, p):
      return
    #END ESCRITURA

    #START NO_CONDICIONAL
    @_('DESDE ID "=" expresion HASTA expresion HACER')
    def no_condicional(self, p):
      return
    #END NO_CONDICIONAL

    #START CONDICIONAL
    @_('MIENTRAS "(" expresion ")" HAZ bloque')
    def condicional(self, p):
      return
    #END CONDICIONAL

    #START DECISION
    @_('SI "(" expresion ")" ENTONCES estatuto SINO bloque',
        'SI "(" expresion ")" ENTONCES estatuto')
    def decision(self, p):
      return
    #END DECISION

    #START PARAMS
    @_('"(" VAR tipo ":" ID ";" ")"',
      '"(" VAR tipo ":" ID ";" paramsaux ")"')
    def params(self, p):
      return

    @_('tipo ":" ID ";"')
    def paramsaux(self, p):
      return
    #END PARAMS

    #START FUNCIONES
    @_('FUNCION funciones_tipo_de_retorno ID params ";" bloque funciones_aux')
    def funciones(self, p):
      return

    @_('tipo',
      'VOID')
    def funciones_tipo_de_retorno(self, p):
      return

    @_('funciones', '')
    def funciones_aux(self, p):
      return
    #END FUNCIONES

    #START TIPO
    @_('INT',
      'FLOAT',
      'CHAR')
    def tipo(self, p):
      return
    #END TIPO

    #START VARS
    @_('VAR tipo ":" lista_id ";"',
    'VAR tipo ":" lista_id ";" varsaux')
    def vars(self, p):
      return

    @_('tipo ":" lista_id ";"')
    def varsaux(self, p):
      return
    #END VARS

    #START LISTA_ID
    @_('ID lista_accesor lista_accesor')
    def lista_id(self, p):
      return

    @_('"[" ENTERO "]"')
    def lista_accesor(self, p):
      return
    #END LISTA_ID

    #START PROGRAMA
    @_('PROGRAMA ID ";" vars funciones PRINCIPAL bloque',
        'PROGRAMA ID ";" vars PRINCIPAL bloque',
        'PROGRAMA ID ";" funciones PRINCIPAL bloque',
        'PROGRAMA ID ";" PRINCIPAL bloque')
    def programa(self, p):
      return
    #END PROGRAMA



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
