from sly import Lexer, Parser
from dirfunciones import DirectorioFunciones, TuplaDirectorioFunciones, ReturnType, TuplaTablaVariables, VarType
# from statements.Statement import Expr, DiffExpr, SumExpr, Literal, Var, MultExpr, DivExpr


func_dir = DirectorioFunciones()
# cubo_seman = CuboSemantico()

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

    @_(r'[0-9]+')
    def ENTERO(self, t):
        t.value = int(t.value)
        return t

    @_(r'\d+.\d+')
    def DECIMAL(self, t):
      t.value = float(t.value)
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


from code_generation.QuadrupleList import QuadrupleList

class CalcParser(Parser):
    tokens = CalcLexer.tokens
    start = 'decision'
    quad_list = QuadrupleList()

    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/')
      )

    def __init__(self):
        self.names = { }

    # START exp
    @_('termino')
    def exp(self, p):
      return p[0]

    @_('termino "+" exp',
      'termino "-" exp')
    def exp(self, p):
      temp_var = self.quad_list.get_next_temp()
      self.quad_list.add_quadd(p[1], p[0], p[2], temp_var)
      return temp_var
    # END exp

    #START termino
    @_('factor')
    def termino(self, p):
      return p[0]

    @_('factor "*" termino',
      'factor "/" termino')
    def termino(self, p):
      temp_var = self.quad_list.get_next_temp()
      self.quad_list.add_quadd(p[1], p[0], p[2], temp_var)
      print(p[0], p[1], p[2])
      return temp_var
    #END termino

    # START factor
    @_('"(" expresion ")"')
    def factor(self, p): return p[1]
    @_('ENTERO')
    def factor(self, p):
      return p[0]
    @_('ID')
    def factor(self, p): return p[0]

    # END factor


    # START expresion
    @_('exp')
    def expresion(self, p): return p[0]

    @_('exp "<" exp',
       'exp ">" exp')
    def expresion(self, p):
      temp_var = self.quad_list.get_next_temp()
      self.quad_list.add_quadd(p[1], p[0], p[2], temp_var)
      return temp_var

    @_('exp IGUAL exp',
       'exp DIFERENTE exp',
       'exp "&" exp',
       'exp "|" exp')
    def expresion(self, p):
      return p
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
      return p[0]
    #END ESTATUTO

    # START BLOQUE
    @_('"{" bloqueaux "}"')
    def bloque(self, p):
      return p[1]


    @_('empty',
        'estatuto',
        'estatuto bloqueaux')
    def bloqueaux(self, p):
      return p[0]
    #END BLOQUE

    #START ASIGNACION
    @_('ID "=" expresion ";"')
    def asignacion(self, p):
      self.quad_list.add_quadd('=', p[0], '', p[2])
      print('=', p[0], '', p[2])
      return
    #END ASIGNACION

    #START LECTURA
    @_('LEE "(" lectura_aux ")" ";"')
    def lectura(self, p):
      return

    @_('ID',
      'expresion')
    def lectura_aux(self, p):
      self.quad_list.add_quadd('READ', '', '', p[0])
      return

    @_('ID "," lectura_aux',
      'expresion "," lectura_aux')
    def lectura_aux(self, p):
      self.quad_list.add_quadd('READ', '', '', p[0])
      return
    #END LECTURA

    #START ESCRITURA
    @_('ESCRIBE "(" escritura_aux ")" ";"')
    def escritura(self, p):
      return

    @_('ID',
      'expresion')
    def escritura_aux(self, p):
      self.quad_list.add_quadd('WRITE', '', '', p[0])
      return

    @_('ID "," escritura_aux',
      'expresion "," escritura_aux')
    def escritura_aux(self, p):
      self.quad_list.add_quadd('WRITE', '', '', p[0])
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
    @_('SI "(" expresion ")" seen_if ENTONCES bloque seen_estatuto')
    def decision(self, p):
      self.quad_list.update_quad_target(p.seen_if, p.seen_estatuto)
      return

    @_('')
    def seen_if(self, p):
      self.quad_list.add_quadd('JUMPF', -1, -1, -1)
      return self.quad_list.pointer - 1

    @_('')
    def seen_estatuto(self, p):
      return self.quad_list.pointer





    @_('SI "(" expresion ")" seen_if ENTONCES bloque SINO bloque')
    def decision(self, p):
      return

    @_('')
    def seen_(self, p):
      #print("Saw an A = ", p[-1])
      return
    #END DECISION

    #START PARAMS

    @_('"(" empty ")"')
    def params(self, p):
      return []

    @_('"(" VAR tipo ":" ID ")"')
    def params(self, p):
      var_list = [TuplaTablaVariables(name=p.ID, type=VarType(p.tipo))]
      return var_list

    @_('"(" VAR tipo ":" ID paramsaux ")"')
    def params(self, p):
      var_list = [TuplaTablaVariables(name=p.ID, type=VarType(p.tipo))] + p.paramsaux
      return var_list


    @_('"," VAR tipo ":" ID paramsaux')
    def paramsaux(self, p):
      return [TuplaTablaVariables(
        name= p.ID,
        type = VarType(p.tipo)
      )] + p.paramsaux

    @_('empty')
    def paramsaux(self, p):
      return []
    #END PARAMS

    #START FUNCIONES
    @_('FUNCION funciones_tipo_de_retorno ID params ";" bloque funciones_aux')
    def funciones(self, p):
      dir_entry = TuplaDirectorioFunciones(
        name = p.ID,
        return_type = ReturnType(p.funciones_tipo_de_retorno),
        vars_table = dict(),
      )
      dir_entry.add_vars(p.params)

      print(dir_entry)
      func_dir.add_func_entry(dir_entry)


    @_('tipo',
      'VOID')
    def funciones_tipo_de_retorno(self, p):
      return p[0]

    @_('funciones', 'empty')
    def funciones_aux(self, p):
      return
    #END FUNCIONES

    #START TIPO
    @_('INT',
      'FLOAT',
      'CHAR')
    def tipo(self, p):
      return p[0]
    #END TIPO

    #START VARS
    @_('VAR tipo ":" lista_id ";"')
    def vars(self, p):
      return [TuplaTablaVariables(name=p.lista_id, type=VarType(p.tipo))]

    @_('VAR tipo ":" lista_id ";" varsaux')
    def vars(self, p):
      return [TuplaTablaVariables(name=p.lista_id, type=VarType(p.tipo))] + p.varsaux
      #return

    @_('tipo ":" lista_id ";" varsaux')
    def varsaux(self, p):
      return [TuplaTablaVariables(
        name= p.ID,
        type = VarType(p.tipo)
      )] + p.paramsaux

    @_('empty')
    def varsaux(self, p):
      return []
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
        'PROGRAMA ID ";" vars PRINCIPAL bloque')
    def programa(self, p):
      func_dir.add_global_vars(p.vars)
      return

    @_('PROGRAMA ID ";" funciones PRINCIPAL bloque',
        'PROGRAMA ID ";" PRINCIPAL bloque')
    def programa(self, p):
      return
    #END PROGRAMA

    #START EMPTY
    @_('')
    def empty(self, p):
      pass
    #END EMPTY



if __name__ == '__main__':
    lexer = CalcLexer()
    parser = CalcParser()
    # while True:
        # try:
        #     text = input('calc > ')
        # except EOFError:
        #     break
        # if text:
    # parser.parse(lexer.tokenize("funcion void cacas (var int:par1, var char:chava, var float:param3) ; {}"))
    bloque = "{ C=1; escribe(A+B+C*X); hola = 5; hola = 6; hola = 6; hola = 7; hola = 8;}"
    decision = "si ( 5 > 1 ) entonces {escribe(A+B+C+D+E);}"
    program = decision
    print(program)
    #for a in lexer.tokenize(program):
      #print(a)
    parser.parse(lexer.tokenize(program))
    for q in parser.quad_list.quadruples:
      print(q)
