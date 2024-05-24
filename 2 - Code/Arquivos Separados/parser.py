from error import error
from lexer import lexicografo

class parser:
  def __init__(self, nomeArquivo):
    self.errors = error()
    self.lex = lexicografo(nomeArquivo)
    self.lookahead = self.lex.scan()
    self.declaracao_algoritmo()

  def match(self, token):
    print(self.lookahead.valor)
    if token == self.lookahead.tipo:
      self.lookahead = self.lex.scan()
    else:
      print("Erro de Sintaxe na linha", self.lex.getLinhaAtual()+1, self.lookahead.toString())
      self.errors.error(token)
      return -1

  def lvalue(self, flag=0): # lvalue -> 264 ("[" expressao "]")*;
    if flag == 0:
      self.match(264)
    while self.lookahead.tipo == 91:
      self.match(91)
      self.expressao()
      self.match(93)

  def linha_lista(self): # linha_lista -> linha_atribuicao | funcao_chamar ";"| linha_retorno | linha_se | linha_enquanto | linha_para;
    if self.lookahead.valor.lower() == "para":
      self.linha_para()
    else:
      if self.lookahead.valor.lower() == "enquanto":
        self.linha_enquanto()
      else:
        if self.lookahead.valor.lower() == "se":
          self.linha_se()
        else:
          if self.lookahead.valor.lower() == "retorne":
            self.linha_retorno()
          else:
            if self.lookahead.tipo == 264:
              if(self.funcao_chamar()!=-1):
                self.match(59)
              else:
                self.linha_atribuicao(1)

  def linha_atribuicao(self, number): # linha_atribuicao -> lvalue "=" expressao ";";
    self.lvalue(number)
    self.match(61)
    self.expressao()
    if number != 0:
      self.match(59)

  def linha_se(self): # linha_se -> "se" expressao 123 linha_lista 125 ("senão" 123 linha_lista 125)?;
    if self.lookahead.tipo == 263:
      self.match(263)
      self.expressao()
      self.match(123)
      self.linha_lista()
      self.match(125)
    if self.lookahead.tipo == 263 and self.lookahead.valor.lower() == "senao":
      self.match(263)
      self.match(123)
      self.linha_lista()
      self.match(125)

  def linha_para(self): # linha_para -> "para" 40 linha_atribuicao 59 expressao 59 linha_atribuicao 41 123 linha_lista 125;
    if self.lookahead.tipo == 263:
      self.match(263)
      self.match(40)
      if self.lookahead.tipo != 59:
        self.linha_atribuicao(0)
      self.match(59)
      if self.lookahead.tipo != 59:
        self.expressao()
      self.match(59)
      if self.lookahead.tipo != 41:
        self.linha_atribuicao(0)
      self.match(41)
      self.match(123)
      self.linha_lista()
      self.match(125)

  def linha_retorno(self): # linha_retorno -> "retorne" expressao? ";";
    if self.lookahead.tipo == 263:
      self.match(263)
      if self.lookahead.tipo != 59:
        self.expressao()
      self.match(59)

  def linha_enquanto(self): # linha_enquanto -> "enquanto" 40 expressao 41 123 linha_lista 125;
    if self.lookahead.tipo == 263:
      self.match(263)
      self.match(40)
      self.expressao()
      self.match(41)
      self.match(123)
      self.linha_lista()
      self.match(125)

  def tipo_primitivo(self): # tipo_primitivo -> 263;
    if self.lookahead.tipo == 263:
      self.match(263)

  def funcao_parametro(self): # funcao_parametro -> tipo_primitivo 264;
    self.tipo_primitivo()
    self.match(264)

  def funcao_parametros(self): # funcao_parametros -> funcao_parametro (<44> funcao_parametro)*;
    self.funcao_parametro()
    while self.lookahead.tipo == 44:
      self.match(44)
      self.funcao_parametro()

  def funcao_argumentos(self): # funcao_argumentos -> expressao ("," expressao)*;
    self.expressao()
    while self.lookahead.tipo == 44:
      self.match(44)
      self.expressao()

  def funcao_chamar(self): # funcao_chamar -> 264 "(" funcao_argumentos? ")";
    if self.lookahead.tipo == 264:
      self.match(264)
      if self.lookahead.tipo == 40:
        self.match(40)
      else:
        return -1
      if self.lookahead.tipo != 41:
        self.funcao_argumentos()
      self.match(41)

  def literais(self): # literais -> 261 | 262 | 256;
    if self.lookahead.tipo == 261:
      self.match(261)
    else:
      if self.lookahead.tipo == 262:
        self.match(262)
      else:
        if self.lookahead.tipo == 256:
          self.match(256)

  def declaracao_variaveis(self): # declaracao_variaveis -> tipo_primitivo 264 (("," 264)*| ("[" literais "]")*)*";";
    self.tipo_primitivo()
    self.match(264)
    while self.lookahead.tipo == 44 or self.lookahead.tipo == 91:
      if self.lookahead.tipo == 44:
        self.match(44)
        self.match(264)
      else:
        self.match(91)
        self.literais()
        self.match(93)
    self.match(59)

  def Add(self): # Add - > "|" expressao Add | "&" expressao  Add | ("=") expressao Add | (">"|">="|"<"|"<="|"=="|"!=") expressao Add
  # | ("+" | "-") expressao Add | ("/"|"*"|"%") expressao Add | lambda;
    flag = 0
    if self.lookahead.tipo == 124: # "|"
      flag = 10
      self.match(124)
    else:
      if self.lookahead.tipo == 38: # "&"
        flag = 10
        self.match(38)
      else:
        if self.lookahead.tipo == 61: # ("=")
          flag = 10
          self.match(61)
        else:
          if self.lookahead.tipo == 62 or self.lookahead.tipo == 257 or self.lookahead.tipo == 60 or self.lookahead.tipo == 258 or self.lookahead.tipo == 259 or self.lookahead.tipo == 260:
          # (">"|">="|"<"|"<="|"=="|"!=")
            flag = 10
            if self.lookahead.tipo == 62:
              self.match(62)
            else:
              if self.lookahead.tipo == 257:
                self.match(257)
              else:
                if self.lookahead.tipo == 60:
                  self.match(60)
                else:
                  if self.lookahead.tipo == 258:
                    self.match(258)
                  else:
                    if self.lookahead.tipo == 259:
                      self.match(259)
                    else:
                      self.match(260)
          else:
            if self.lookahead.tipo == 43 or self.lookahead.tipo == 45: # ("+" | "-")
              flag = 10
              if self.lookahead.tipo == 43:
                self.match(43)
              else:
                self.match(45)
            else:
              if self.lookahead.tipo == 47 or self.lookahead.tipo == 42 or self.lookahead.tipo == 37: # ("/"|"*"|"%")
                flag = 10
                if self.lookahead.tipo == 47:
                  self.match(47)
                else:
                  if self.lookahead.tipo == 42:
                    self.match(42)
                  else:
                    self.match(37)

    if flag == 10: # expressao Add
      self.expressao()
      self.Add()
    else: # Lambda
      return

  def termo(self): # termo -> funcao_chamar | lvalue | literais | "(" expressao ")";
    if self.lookahead.tipo == 40:
      self.match(40)
      self.expressao()
      self.match(41)
    else:
      if self.lookahead.tipo == 264:
        if self.funcao_chamar() == -1:
          self.lvalue(1)
          return
        else:
          return
      self.literais()

  def expressao(self): # expressao - > ("+"|"-"|"!")? termo Add;
    if self.lookahead.tipo == 43:
      self.match(43)
    else:
      if self.lookahead.tipo == 45:
        self.match(45)
      else:
        if self.lookahead.tipo == 33:
          self.match(33)
    self.termo()
    self.Add()

  def funcao_declaracao_variaveis(self): # funcao_declaracao_variaveis -> (declaracao_variaveis ";")*;
    while self.lookahead.tipo == 263:
      self.declaracao_variaveis()
      self.match(59)

  def declaracao_variaveis_bloco(self): # declaracao_variaveis_bloco -> 263 123  declaracao_variaveis* 125;
    if self.lookahead.tipo == 263:
      self.match(263)
      self.match(123)
      while self.lookahead.tipo != 125:
        self.declaracao_variaveis()
      self.match(125)
    else:
      return

  def linha_bloco(self): # linha_bloco -> 123 (linha_lista)* 125;
    self.match(123)
    while self.lookahead.tipo != 125:
      self.linha_lista()
    self.match(125)

  def funcao_declaracao(self): # funcao_declaracao ->  "função" tipo_primitivo 264 "(" funcao_parametros? ")" funcao_declaracao_variaveis linha_bloco;
    if self.lookahead.tipo == 263:
      self.match(263)
      self.tipo_primitivo()
      self.match(264)
      self.match(40)
      if self.lookahead.tipo != 41:
        self.funcao_parametros()
      self.match(41)
      self.funcao_declaracao_variaveis()
      self.linha_bloco()

  def declaracao_algoritmo(self): # declaracao_algoritmo -> 264 123 (declaracao_variaveis_bloco)? linha_bloco (funcao_declaracao)* 125;
    if self.lookahead.tipo == 263:
      self.match(263)
      self.match(123)
      self.declaracao_variaveis_bloco()
      self.linha_bloco()
      while self.lookahead.tipo != 125:
        self.funcao_declaracao()
      self.match(125)

parser(r'teste.cp')