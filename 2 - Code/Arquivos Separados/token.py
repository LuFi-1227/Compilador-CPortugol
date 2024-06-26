#Tipos de tags e suas numerações (Estamos usando os 255 caracteres da tabela ASCII)
STRING = 256
MAIIGU = 257
MENIGU = 258
COMP = 259
DIF = 260
INT = 261
FLUT = 262
RES = 263
ID = 264

palavrasReservadas = ['se', 'senao', 'para', 'enquanto', 'funcao', 'inteiro', 'flut', 'variaveis', 'algoritmo', 'cadeia', 'retorne']
class Token():
  def classifier(self, valor, tipo):
    if tipo == -1:
      return -1
    elif tipo == 77: #Quer dizer que o valor do token é uma string feita com aspas
      return STRING#STRING
    else:
      if tipo == 3:
        if len(valor) == 1:
          return ord(valor)
        else:
          if valor[1]=='>':
            return MAIIGU#maiororigual
          else:
            if valor[1]=='<':
              return MENIGU#menororigual
            else:
              if valor[1]=='=':
                return COMP#compare
              else:
                return DIF#diferente
      else:
        if tipo == 0:
          return INT#inteeiro
        else:
          if tipo==1:
            return FLUT#float
          else:
            for palavra in palavrasReservadas:
              if palavra.lower() == valor.lower():
                return RES#palavraReservada
            return ID#identificador ou variavel

  def __init__(self, valor, tipo, flag=0):
    if flag == 1:
      self.tipo = tipo
    else:
      self.tipo = self.classifier(valor, tipo)
    self.valor = valor

  def toString(self):
    print("<"+str(self.tipo)+","+str(self.valor)+">")
