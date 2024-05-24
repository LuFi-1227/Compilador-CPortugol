from token import Token

class lexicografo():
  def __init__(self, nArquivo):
    self.pos = 0 #Posiçao que o lexicógrafo está lendo no estado atual do programa
    self.flagEOL = 1
    self.arquivo = open(nArquivo, 'r')
    self.linha = None
    self.tamLinha = 0
    self.linhaAtual = 0
    self.tokenVazio = Token("Ignore", -1)

  def getLinhaAtual(self):
    return self.linhaAtual

  def scan(self):
    buffer = ""
    tipo = None
    if self.flagEOL == 1 or self.linha == None:
      self.linha = self.arquivo.readline()
      self.tamLinha = len(self.linha)
      if len(self.linha.replace("\n", "").replace(" ", "")) == 0:
        self.linha = self.arquivo.readline()
        self.tamLinha = len(self.linha)
      self.pos = 0
      self.flagEOL = 0
    while self.linha:
      if self.linha[self.pos].isspace():
        while self.linha[self.pos].isspace() and self.pos < self.tamLinha-1:
          self.pos = self.pos + 1
      if self.linha[self.pos].isdigit():
        buffer = 0
        while self.linha[self.pos].isdigit():
          buffer = int(buffer)*10 + int(self.linha[self.pos])
          self.pos = self.pos + 1
        if self.linha[self.pos] == '.':
          self.pos = self.pos + 1
          buffer2 = "0."
          while self.linha[self.pos].isdigit():
            buffer2 = buffer2 + self.linha[self.pos]
            self.pos = self.pos + 1
          buffer = buffer + float(buffer2)
          tipo = 1 #Configurando o tipo do token para ponto flutuante
        else:
          tipo = 0 #Configurando o tipo do token para inteiro
      else:
        flag = 1
        if self.seOperador(self.linha[self.pos]) != -1:
          flagOp = self.seOperador(self.linha[self.pos])
          buffer = buffer + self.linha[self.pos]
          if self.linha[self.pos] == '"':
            flag = -1
            tipo = 77 #Este tipo de token é uma String
          self.pos = self.pos + 1
          if self.tamLinha > self.pos:
            if flagOp != 0:
              while self.seOperador(self.linha[self.pos]) == flag:
                buffer = buffer + self.linha[self.pos]
                self.pos = self.pos + 1
              if flag == -1:
                buffer = buffer + self.linha[self.pos]
                self.pos = self.pos + 1
              if buffer == "//" or buffer == "/":
                tipo = -1
                while self.pos <= self.tamLinha-1:
                  self.pos += 1
                if buffer == "/":
                  self.linha = self.arquivo.readline()
                  while self.linha.find("*/")==-1:
                    self.linha = self.arquivo.readline()
          if tipo != -1:
            tipo = 3 #Configurando o tipo do token para Operadores
        else:
          if self.linha[self.pos].isalnum():
            while self.linha[self.pos].isalnum():
              buffer = buffer + self.linha[self.pos]
              self.pos = self.pos + 1
          else:
            tipo = -1
      if tipo != 0 and tipo != 1:
        buffer.replace("\n", "")
      if tipo != -1:
        token = Token(buffer, tipo)
      else:
        token = self.tokenVazio
        self.flagEOL = 1
        self.linhaAtual += 1
      if tipo == 0 or tipo == 1:
        buffer = ""
      if self.tamLinha-1 <= self.pos:
        self.flagEOL = 1
        self.linhaAtual += 1
      return token
    return 1

  def seOperador(self, caractere):
    if '=<>|&!"/'.find(caractere) != -1:
      return 1
    else:
      if '+-*/()[]%{},;'.find(caractere) != -1:
        return 0
      return -1