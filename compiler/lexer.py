from sly import Lexer
from compiler.dirfunciones import TuplaDirectorioFunciones, ReturnType, TuplaTablaVariables, VarType
from compiler.semantic_actions import SemanticActionHandler

"""
Lexer para el compilador
"""
class CalcLexer(Lexer):
    """
    Primero se especifican todos los tokens que exisen en el leguaje
    """
    tokens = {
      ID,
      PROGRAMA,
      PRINCIPAL,
      UMINUS,
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
      DIFERENTE,
      GTR_EQ,
      SML_EQ
     }

    ignore = ' \t'
    literals = { '=', '+', '-', '*', '/', '%',
                 '[', ']', '{', '}', '(', ')',
                 ',', ';', '.', ':',
                 '>', '<', '&', '|',
                 "'", '"', '%',
                 '$', '¡', '?'
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
    SINO = r'sino'
    SI = r'si'
    ENTONCES = r'entonces'
    MIENTRAS = r'mientras'
    HAZ = r'haz'
    DESDE = r'desde'
    HASTA= r'hasta'
    HACER = r'hacer'
    LEE = r'lee'
    ESCRIBE = r'escribe'
    IGUAL = r'=='
    GTR_EQ = r'>='
    SML_EQ = r'<='
    DIFERENTE = r'!='

    """
    Para los tokens que no sean una literal o que necesiten mas procesamiento,
    se puede añadir un metodo decorado con el metodo @_
    """
    @_(r'\"[^\".]*\"')
    def LETRERO(self, t):
      t.value = "@"+t.value
      return t # Ver si jala igual sin la funcion    @_(r'\d+')

    @_(r'[a-zA-Z_][a-zA-Z0-9_]*')
    def ID(self, t):
      t.value = t.value
      return t # Ver si jala igual sin la funcion    @_(r'\d+')

    @_(r'[0-9]+\.[0-9]+')
    def DECIMAL(self, t):
      t.value = float(t.value)
      return t

    @_(r'[0-9]+')
    def ENTERO(self, t):
        t.value = int(t.value)
        return t

    @_(r"\'.\'")
    def CARACTER(self, t):
      t.value = "'" + t.value[1] + "'"
      return t

    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')

    """
    En el metodo error es donde se define que se imprimira en caso de que haya
    un error de sintaxis en el codigo de entrada.
    """
    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1


Tokens = CalcLexer.tokens