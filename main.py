from sly import Lexer, Parser
from dirfunciones import TuplaDirectorioFunciones, ReturnType, TuplaTablaVariables, VarType
from semantic_actions import SemanticActionHandler

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
    DIFERENTE = r'!='

    @_(r'\".*\"')
    def LETRERO(self, t):
      t.value = t.value
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

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1


from code_generation.QuadrupleList import QuadrupleList

class CalcParser(Parser):
    tokens = CalcLexer.tokens

    start = 'programa'

    action_handler = SemanticActionHandler()

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
    def exp(self, p): return self.action_handler.consume_arithmetic_op(p[1], p[0], p[2])
    # END exp

    #START termino
    @_('factor')
    def termino(self, p):
      return p[0]

    @_('factor "*" termino',
      'factor "/" termino')
    def termino(self, p): return self.action_handler.consume_arithmetic_op(p[1], p[0], p[2])
    #END termino

    # START factor
    @_('"(" expresion ")"')
    def factor(self, p): return p[1]

    @_('ID', 'ENTERO', 'DECIMAL')
    def factor(self, p): return p[0]
    # END factor

    # START expresion
    @_('exp', 'llamada_funcion')
    def expresion(self, p): return p[0]

    @_('exp "<" exp',
       'exp ">" exp')
    def expresion(self, p): return self.action_handler.consume_relational_op(p[1], p[0], p[2])

    @_('exp IGUAL exp',
       'exp DIFERENTE exp',
       'exp "&" exp',
       'exp "|" exp')
    def expresion(self, p): return self.action_handler.consume_relational_op(p[1], p[0], p[2])


    @_('verify_function_name args_funcion ")" ";"')
    def llamada_funcion(self, p):
      self.action_handler.function_called(p.verify_function_name, p.args_funcion)
      return p

    @_('ID "("')
    def verify_function_name(self, p):
      self.action_handler.verify_function_name(p.ID)
      return p.ID

    @_('expresion "," args_funcion')
    def args_funcion(self, p):
      return [p.expresion] + p.args_funcion

    @_('expresion')
    def args_funcion(self, p):
      return [p[0]]


    @_('empty')
    def args_funcion(self, p):
      return []

    #END expresion

    #START ESTATUTO
    @_('asignacion ";"',
      'funciones',
      'lectura',
      'escritura',
      'decision',
      'condicional',
      'no_condicional',
      'llamada_funcion'
    )
    def estatuto(self, p):
      return p[0]

    #END ESTATUTO

    # START BLOQUE
    @_('"{" bloqueaux "}"')
    def bloque(self, p):
      return #p[1]

    
    @_('"{" bloqueaux REGRESA exp ";" "}"')
    def bloque(self, p):
      return p[3]


    @_('empty',
        'estatuto',
        'estatuto bloqueaux')
    def bloqueaux(self, p):
      return p[0]
    #END BLOQUE

    #START ASIGNACION
    @_('ID "=" expresion', 'ID "=" CARACTER')
    def asignacion(self, p): return self.action_handler.consume_assignment(p[0], p[2])
    #END ASIGNACION

    #START LECTURA
    @_('LEE "(" lectura_aux ")" ";"')
    def lectura(self, p): return

    @_('ID',
      'expresion')
    def lectura_aux(self, p): self.action_handler.consume_read(p[0])

    @_('ID "," lectura_aux',
      'expresion "," lectura_aux')
    def lectura_aux(self, p): self.action_handler.consume_read(p[0])

    #END LECTURA

    #START ESCRITURA
    @_('ESCRIBE "(" escritura_aux ")" ";"')
    def escritura(self, p): return

    @_('ID',
      'expresion')
    def escritura_aux(self, p): self.action_handler.consume_write(p[0])

    @_('ID "," escritura_aux',
      'expresion "," escritura_aux')
    def escritura_aux(self, p): self.action_handler.consume_write(p[0])
    #END ESCRITURA

    #START NO_CONDICIONAL
    @_('DESDE asignacion HASTA expresion seen_for HACER bloque')
    def no_condicional(self, p): self.action_handler.end_for(p.expresion)

    @_('')
    def seen_for(self, p):  self.action_handler.start_for()
    #END NO_CONDICIONAL

    #START CONDICIONAL
    @_('MIENTRAS "(" expresion ")" seen_while HAZ bloque')
    def condicional(self, p): self.action_handler.end_while(p.expresion)

    @_('')
    def seen_while(self, p): self.action_handler.start_while()
    #END CONDICIONAL

    #START DECISION
    @_('SI "(" expresion ")" seen_if ENTONCES bloque')
    def decision(self, p): self.action_handler.end_if(cond=p.expresion)

    @_('')
    def seen_if(self, p):
      return self.action_handler.start_if()

    @_('SI "(" expresion ")" seen_if ENTONCES bloque SINO seen_else bloque')
    def decision(self, p): self.action_handler.end_else(cond=p.expresion)

    @_('')
    def seen_else(self, p): self.action_handler.start_else()

    #END DECISION

    #START PARAMS

    @_('"(" empty ")"')
    def params(self, p):
      return []

    @_('"(" tipo ID paramsaux ")"')
    def params(self, p):
      return self.action_handler.add_param_to_current_scope(name=p.ID, tipo=VarType(p.tipo))


    @_('"," tipo ID paramsaux')
    def paramsaux(self, p):
      return self.action_handler.add_param_to_current_scope(name=p.ID, tipo=VarType(p.tipo))

    @_('empty')
    def paramsaux(self, p): return
    #END PARAMS

    #START FUNCIONES
    @_('function_init params vars bloque end_funcion_declaration funciones_aux')
    def funciones(self, p):
      self.action_handler.func_return(p.function_init, p.bloque)

      return

    @_('empty')
    def end_funcion_declaration(self, p):
      self.action_handler.end_function_declaration()

    @_('FUNCION funciones_tipo_de_retorno ID')
    def function_init(self, p):
      self.action_handler.start_func_scope_var_declaration(p.funciones_tipo_de_retorno, p.ID)
      return p.ID

    @_('tipo',
      'VOID')
    def funciones_tipo_de_retorno(self, p): return p[0]

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
    @_('VAR varios_tipos')
    def vars(self, p): pass

    @_('declaracion varios_tipos')
    def varios_tipos(self, p): pass

    @_('empty')
    def varios_tipos(self, p): pass

    @_('tipo lista_id_aux ";"')
    def declaracion(self, p):
      self.action_handler.add_variable_to_current_scope(tipo=VarType(p.tipo), args=p.lista_id_aux)

    @_(' lista_id  "," lista_id_aux')
    def lista_id_aux(self, p):
      return [p.lista_id] + p.lista_id_aux
      
    @_(' lista_id')
    def lista_id_aux(self, p):
      return [p[0]]
    
    @_('empty')
    def lista_id_aux(self, p):
      return []

    @_('empty')
    def vars(self, p): pass
    #END VARS

    #START LISTA_ID
    @_('ID')
    def lista_id(self, p):
      return p[0]

    @_('ID lista_accesor lista_accesor')
    def lista_id(self, p):
      return

    @_('"[" ENTERO "]"')
    def lista_accesor(self, p):
      return
    #END LISTA_ID

    #START PROGRAMA
    @_('PROGRAMA jump_principal ID ";" set_global_var_scope vars funciones PRINCIPAL upd_principal bloque')
    def programa(self, p):
      return

    @_('PROGRAMA jump_principal ID ";" set_global_var_scope funciones PRINCIPAL upd_principal bloque')
    def programa(self, p):
      return
    
    @_('PROGRAMA jump_principal ID ";" set_global_var_scope vars PRINCIPAL upd_principal bloque')
    def programa(self, p):
      return
    
    @_('PROGRAMA jump_principal ID ";" set_global_var_scope PRINCIPAL upd_principal bloque')
    def programa(self, p):
      return

    @_('')
    def set_global_var_scope(self, p):
      self.action_handler.start_global_var_declaration()

    @_('empty')
    def jump_principal(self, p):
      self.action_handler.first_quad()
    
    @_('empty')
    def upd_principal(self, p):
      self.action_handler.principal()
    #END PROGRAMA

    #START EMPTY
    @_('')
    def empty(self, p):
      pass
    #END EMPTY



if __name__ == '__main__':
    lexer = CalcLexer()
    parser = CalcParser()

    bloque = "{ C=1; escribe(A+B+C*X); hola = 5; hola = 6; hola = 6; hola = 7; hola = 8;}"
    decision = "si ( 5 > 1 ) entonces {escribe(A+B+C+D+E);} sino {escribe(A+B+C+D+E);}"
    ciclo = "mientras ( 5 > 1 ) haz {escribe(A+B+C+D+E);}"
    aritmetica = "1 + 2"

    no_condicional = "desde C=1 hasta ( 5 > 1 ) hacer {escribe(A+B+C+D+E);}"
    modulos = """
    funcion void test (int: a, int: b)
    var int: c;
    var int: d;
    var int: e;
    {
      a = a + 2;
    }
    """
    with open('./examples/main1.sarny', 'r') as file:
      program = file.read()
      parser.parse(lexer.tokenize(program))

      i = 0
      for q in parser.action_handler.quad_list.quadruples:
        print(str(i) + ": " + str(q))
        i+=1

      for q in parser.action_handler.constant_map.items():
        print(q)
