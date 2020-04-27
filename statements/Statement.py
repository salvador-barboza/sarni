from dataclasses import dataclass
from cubosemantico import CuboSemantico
cubo = CuboSemantico()

class Expr:
  return_type = ""
  value = any
  def get_quad(self): return ('', '' ,'' ,'')
  pass

class ArithmeticExpr(Expr):
  leftOp = '',
  rightOp = '',
  op = ''

  def __init__(self, op, exprA, exprB):
    result = cubo.typematch(exprA.type, op, exprB.type)
    self.leftOp = exprA
    self.rightOp = exprB
    self.op = op

    if result == 'error':
      raise Exception("Hay un error aqui xd.")

class Literal(Expr):
  pass


@dataclass
class Var(Expr):
  identifier: str
