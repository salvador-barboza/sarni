class CuboSemantico:
  operando = {"int": 0,"float": 1, "char": 2,"bool": 3}
  operador = {"+": 0,"-": 1,"/": 2,"*": 3,"<": 4,">": 5,"==": 6,"!=": 7,"&":8,"|":9}

  Cubo = [[["int","int","float","int","bool","bool","bool","bool","error","error"],
          ["float","float","float","float","bool","bool","bool","bool","error","error"],
          ["error","error","error","error","error","error","error","error","error","error"],
          ["error","error","error","error","error","error","error","error","bool","bool"]],
          [["float","float","float","float","bool","bool","bool","bool","error","error"],
          ["float","float","float","float","bool","bool","bool","bool","error","error"],
          ["error","error","error","error","error","error","error","error","error","error"],
          ["error","error","error","error","error","error","error","error","error","error"]],
          [["error","error","error","error","error","error","error","error","error","error"],
          ["error","error","error","error","error","error","error","error","error","error"],
          ["error","error","error","error","error","error","bool","bool","error","error"],
          ["error","error","error","error","error","error","error","error","error","error"]],
          [["error","error","error","error","error","error","error","error","bool","bool"],
          ["error","error","error","error","error","error","error","error","error","error"],
          ["error","error","error","error","error","error","error","error","error","error"],
          ["error","error","error","error","error","error","bool","bool","bool","bool"]]
  ]

  def typematch(self,op_izq,operador,op_der):
    return self.Cubo[self.operando[op_izq]][self.operador[operador]][self.operando[op_der]]
