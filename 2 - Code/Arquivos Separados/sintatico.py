from error import error
from lexer import lexicografo
from arvore import Arvore
from pilha import Pilha
from tabelaDeSimbolos import TabelaDeSimbolos
from no import no
import token
class parser():
  def __init__(self, nomeArquivo):
    self.bufferTipo = ""
    self.bufferIdent = ""
    self.errors = error()
    self.pilha = Pilha()
    self.Tabela_de_Simbolos = TabelaDeSimbolos("main")
    self.arvore = Arvore()
    self.lex = lexicografo(nomeArquivo)
    self.lookahead = self.lex.scan()
    self.declaracao_algoritmo()

  def match(self, token, node): ##
    #print(self.lookahead.valor)
    if token == self.lookahead.tipo:
      nof = no(self.lookahead)
      nof.setPai(node)
      node.addFilho(nof)
      self.pilha.empilha(nof)
      self.lookahead = self.lex.scan()
    else:
      print("Erro de Sintaxe na linha", self.lex.getLinhaAtual()+1, self.lookahead.toString())
      self.errors.error(token)
      #self.pilha.esvazia()
      #exit()

  def lvalue(self, node, flag=0): ## lvalue -> 264 ("[" expressao "]")*;
    aux = no(token.Token("lvalue", -1, 1))
    node.addFilho(aux)
    aux.setPai(node)
    if flag == 0:
      if self.Tabela_de_Simbolos.getReg(self.lookahead.valor.lower()) == None:
          self.Tabela_de_Simbolos.register(self.lookahead.valor.lower(), self.bufferTipo)
      self.match(264, aux)
    while self.lookahead.tipo == 91:
      self.match(91, aux)
      self.expressao(aux)
      self.match(93, aux)
    self.pilha.empilha(aux)

  def linha_lista(self, node): ## linha_lista -> linha_atribuicao | funcao_chamar ";"| linha_retorno | linha_se | linha_enquanto | linha_para;
    #print(self.lookahead.valor.lower())
    if self.lookahead.valor.lower() == "para":
      aux = no(token.Token("linha_lista", -2, 1))
      node.addFilho(aux)
      aux.setPai(node)
      self.linha_para(aux)
      self.pilha.empilha(aux)
    else:
      if self.lookahead.valor.lower() == "enquanto":
        aux = no(token.Token("linha_lista", -2, 1))
        node.addFilho(aux)
        aux.setPai(node)
        self.linha_enquanto(aux)
        self.pilha.empilha(aux)
      else:
        if self.lookahead.valor.lower() == "se":
          aux = no(token.Token("linha_lista", -2, 1))
          node.addFilho(aux)
          aux.setPai(node)
          self.linha_se(aux)
          self.pilha.empilha(aux)
        else:
          if self.lookahead.valor.lower() == "retorne":
            aux = no(token.Token("linha_lista", -2, 1))
            node.addFilho(aux)
            aux.setPai(node)
            self.linha_retorno(aux)
            self.pilha.empilha(aux)
          else:
            if self.lookahead.tipo == 264:
              aux = no(token.Token("linha_lista", -2, 1))
              node.addFilho(aux)
              aux.setPai(node)
              if(self.funcao_chamar(aux)!=-1):
                self.match(59, aux)
                self.pilha.empilha(aux)
              else:
                #print("Linha Atrib")
                self.linha_atribuicao(1, aux)
                self.pilha.empilha(aux)

  def linha_atribuicao(self, number, node): ## linha_atribuicao -> lvalue "=" expressao ";";
    aux = no(token.Token("linha_atribuicao", -3, 1))
    node.addFilho(aux)
    aux.setPai(node)
    self.lvalue(aux, number)
    self.match(61, aux)
    self.expressao(aux)
    if number != 0:
      self.match(59, aux)
    self.pilha.empilha(aux)

  def linha_se(self, node): ## linha_se -> "se" expressao 123 linha_lista 125 ("senão" 123 linha_lista 125)?;
    if self.lookahead.tipo == 263:
      aux = no(token.Token("linha_se", -4, 1))
      node.addFilho(aux)
      aux.setPai(node)
      self.match(263, aux)
      self.expressao(aux)
      self.match(123, aux)
      self.linha_lista(aux)
      self.match(125, aux)
      self.pilha.empilha(aux)
    if self.lookahead.tipo == 263 and self.lookahead.valor.lower() == "senao":
      aux = no(token.Token("linha_se", -4, 1))
      node.addFilho(aux)
      aux.setPai(node)
      self.match(263, aux)
      self.match(123, aux)
      self.linha_lista(aux)
      self.match(125, aux)
      self.pilha.empilha(aux)

  def linha_para(self, node): ## linha_para -> "para" 40 linha_atribuicao 59 expressao 59 linha_atribuicao 41 123 linha_lista 125;
    if self.lookahead.tipo == 263:
      aux = no(token.Token("linha_para", -5, 1))
      node.addFilho(aux)
      aux.setPai(node)
      self.match(263, aux)
      self.match(40, aux)
      if self.lookahead.tipo != 59:
        self.linha_atribuicao(0, aux)
      self.match(59, aux)
      if self.lookahead.tipo != 59:
        self.expressao(aux)
      self.match(59, aux)
      if self.lookahead.tipo != 41:
        self.linha_atribuicao(0, aux)
      self.match(41, aux)
      self.match(123, aux)
      self.linha_lista(aux)
      self.match(125, aux)
      self.pilha.empilha(aux)

  def linha_retorno(self, node): ## linha_retorno -> "retorne" expressao? ";";
    if self.lookahead.tipo == 263:
      aux = no(token.Token("linha_retorno", -6, 1))
      node.addFilho(aux)
      aux.setPai(node)
      self.match(263, aux)
      if self.lookahead.tipo != 59:
        self.expressao(aux)
      self.match(59, aux)
      self.pilha.empilha(aux)

  def linha_enquanto(self, node): ## linha_enquanto -> "enquanto" 40 expressao 41 123 linha_lista 125;
    if self.lookahead.tipo == 263:
      aux = no(token.Token("linha_enquanto", -7, 1))
      node.addFilho(aux)
      aux.setPai(node)
      self.match(263, aux)
      self.match(40, aux)
      self.expressao(aux)
      self.match(41, aux)
      self.match(123, aux)
      while self.lookahead.tipo != 125:
        self.linha_lista(aux)
      self.match(125, aux)
      self.pilha.empilha(aux)

  def tipo_primitivo(self, node): ## tipo_primitivo -> 263;
    if self.lookahead.tipo == 263:
      aux = no(token.Token("tipo_primitivo", -8, 1))
      node.addFilho(aux)
      aux.setPai(node)
      self.bufferTipo = self.lookahead.valor.lower()
      self.match(263, aux)
      self.pilha.empilha(aux)

  def funcao_parametro(self, node): ## funcao_parametro -> tipo_primitivo 264;
    aux = no(token.Token("funcao_parametro", -9, 1))
    node.addFilho(aux)
    aux.setPai(node)
    self.tipo_primitivo(aux)
    self.Tabela_de_Simbolos.register(self.lookahead.valor.lower(), self.bufferTipo)
    self.match(264, aux)
    self.pilha.empilha(aux)

  def funcao_parametros(self, node): ## funcao_parametros -> funcao_parametro (<44> funcao_parametro)*;
    aux = no(token.Token("funcao_parametros", -10, 1))
    node.addFilho(aux)
    aux.setPai(node)
    self.funcao_parametro(aux)
    while self.lookahead.tipo == 44:
      self.match(44, aux)
      self.funcao_parametro(aux)
    self.pilha.empilha(aux)

  def funcao_argumentos(self, node): ## funcao_argumentos -> expressao ("," expressao)*;     _____ Quando chama a função
    aux = no(token.Token("funcao_argumentos", -11, 1))
    node.addFilho(aux)
    aux.setPai(node)
    self.expressao(aux)
    while self.lookahead.tipo == 44:
      self.match(44, aux)
      self.expressao(aux)
    self.pilha.empilha(aux)

  def funcao_chamar(self, node): ## funcao_chamar -> 264 "(" funcao_argumentos? ")";
    if self.lookahead.tipo == 264:
      aux = no(token.Token("funcao_chamar", -12, 1))
      node.addFilho(aux)
      aux.setPai(node)
      self.match(264, aux)
      if self.lookahead.tipo == 40:
        self.match(40, aux)
      else:
        return -1
      if self.lookahead.tipo != 41:
        self.funcao_argumentos(aux)
      self.match(41, aux)
      self.pilha.empilha(aux)

  def literais(self, node): ## literais -> 261 | 262 | 256;
    if self.lookahead.tipo == 261:
      aux = no(token.Token("literais", -13, 1))
      node.addFilho(aux)
      aux.setPai(node)
      self.match(261, aux)
      self.pilha.empilha(aux)
    else:
      if self.lookahead.tipo == 262:
        aux = no(token.Token("literais", -13, 1))
        node.addFilho(aux)
        aux.setPai(node)
        self.match(262, aux)
        self.pilha.empilha(aux)
      else:
        if self.lookahead.tipo == 256:
          aux = no(token.Token("literais", -13, 1))
          node.addFilho(aux)
          aux.setPai(node)
          self.match(256, aux)
          self.pilha.empilha(aux)

  def declaracao_variaveis(self, node): ## declaracao_variaveis -> tipo_primitivo 264 (("," 264)*| ("[" literais "]")*)*";";
    aux = no(token.Token("declaracao_variaveis", -14, 1))
    node.addFilho(aux)
    aux.setPai(node)
    self.tipo_primitivo(aux)
    self.Tabela_de_Simbolos.register(self.lookahead.valor.lower(), self.bufferTipo)
    self.match(264, aux)
    while self.lookahead.tipo == 44 or self.lookahead.tipo == 91:
      if self.lookahead.tipo == 44:
        self.match(44, aux)
        self.Tabela_de_Simbolos.register(self.lookahead.valor.lower(), self.bufferTipo)
        self.match(264, aux)
      else:
        self.match(91, aux)
        self.literais(aux)
        self.match(93, aux)
    self.match(59, aux)
    self.pilha.empilha(aux)

  def Add(self, node): ## Add - > "|" expressao Add | "&" expressao  Add | ("=") expressao Add | (">"|">="|"<"|"<="|"=="|"!=") expressao Add
  # | ("+" | "-") expressao Add | ("/"|"*"|"%") expressao Add | lambda;
    flag = 0
    aux = None
    if self.lookahead.tipo == 124: # "|"
      aux = no(token.Token("Add", -15, 1))
      node.addFilho(aux)
      aux.setPai(node)
      flag = 10
      self.match(124, aux)
    else:
      if self.lookahead.tipo == 38: # "&"
        aux = no(token.Token("Add", -15, 1))
        node.addFilho(aux)
        aux.setPai(node)
        flag = 10
        self.match(38, aux)
      else:
        if self.lookahead.tipo == 61: # ("=")
          aux = no(token.Token("Add", -15, 1))
          node.addFilho(aux)
          aux.setPai(node)
          flag = 10
          self.match(61, aux)
        else:
          if self.lookahead.tipo == 62 or self.lookahead.tipo == 257 or self.lookahead.tipo == 60 or self.lookahead.tipo == 258 or self.lookahead.tipo == 259 or self.lookahead.tipo == 260:
          # (">"|">="|"<"|"<="|"=="|"!=")
            aux = no(token.Token("Add", -15, 1))
            node.addFilho(aux)
            aux.setPai(node)
            flag = 10
            if self.lookahead.tipo == 62:
              self.match(62, aux)
            else:
              if self.lookahead.tipo == 257:
                self.match(257, aux)
              else:
                if self.lookahead.tipo == 60:
                  self.match(60, aux)
                else:
                  if self.lookahead.tipo == 258:
                    self.match(258, aux)
                  else:
                    if self.lookahead.tipo == 259:
                     self.match(259, aux)
                    else:
                      if self.lookahead.tipo == 260:
                        self.match(260, aux)
          else:
            if self.lookahead.tipo == 43 or self.lookahead.tipo == 45: # ("+" | "-")
              aux = no(token.Token("Add", -15, 1))
              node.addFilho(aux)
              aux.setPai(node)
              flag = 10
              if self.lookahead.tipo == 43:
                if self.Tabela_de_Simbolos.getReg(self.lookahead.valor.lower()) == None:
                    self.Tabela_de_Simbolos.register(self.lookahead.valor.lower(), "sum")
                self.match(43, aux)
              else:
                if self.Tabela_de_Simbolos.getReg(self.lookahead.valor.lower()) == None:
                    self.Tabela_de_Simbolos.register(self.lookahead.valor.lower(), "sub")
                self.match(45, aux)
            else:
              if self.lookahead.tipo == 47 or self.lookahead.tipo == 42 or self.lookahead.tipo == 37: # ("/"|"*"|"%")
                aux = no(token.Token("Add", -15, 1))
                node.addFilho(aux)
                aux.setPai(node)
                flag = 10
                if self.lookahead.tipo == 47:
                  if self.Tabela_de_Simbolos.getReg(self.lookahead.valor.lower()) == None:
                    self.Tabela_de_Simbolos.register(self.lookahead.valor.lower(), "div")
                  self.match(47, aux)
                else:
                  if self.lookahead.tipo == 42:
                    if self.Tabela_de_Simbolos.getReg(self.lookahead.valor.lower()) == None:
                      self.Tabela_de_Simbolos.register(self.lookahead.valor.lower(), "mult")
                    self.match(42, aux)
                  else:
                    if self.Tabela_de_Simbolos.getReg(self.lookahead.valor.lower()) == None:
                      self.Tabela_de_Simbolos.register(self.lookahead.valor.lower(), "rest")
                    self.match(37, aux)

    if flag == 10: # expressao Add
      self.expressao(aux)
      self.Add(aux)
    else: # Lambda
      return
    self.pilha.empilha(aux)

  def termo(self, node): ## termo -> funcao_chamar | lvalue | literais | "(" expressao ")";
    if self.lookahead.tipo == 40:
      aux = no(token.Token("termo", -16, 1))
      node.addFilho(aux)
      aux.setPai(node)
      self.match(40, aux)
      self.expressao(aux)
      self.match(41, aux)
      self.pilha.empilha(aux)
    else:
      aux = no(token.Token("termo", -16, 1))
      node.addFilho(aux)
      aux.setPai(node)
      if self.lookahead.tipo == 264:
        if self.funcao_chamar(aux) == -1:
          self.lvalue(aux, 1)
          self.pilha.empilha(aux)
          return
        else:
          self.pilha.empilha(aux)
          return
      self.literais(aux)
      self.pilha.empilha(aux)

  def expressao(self, node): ## expressao - > ("+"|"-"|"!")? termo Add;
    aux = no(token.Token("expressao", -17, 1))
    node.addFilho(aux)
    aux.setPai(node)
    if self.lookahead.tipo == 43:
      if self.Tabela_de_Simbolos.getReg(self.lookahead.valor.lower()) == None:
        self.Tabela_de_Simbolos.register(self.lookahead.valor.lower(), "sum")
      self.match(43, aux)
    else:
      if self.lookahead.tipo == 45:
        if self.Tabela_de_Simbolos.getReg(self.lookahead.valor.lower()) == None:
          self.Tabela_de_Simbolos.register(self.lookahead.valor.lower(), "sub")
        self.match(45, aux)
      else:
        if self.lookahead.tipo == 33:
          if self.Tabela_de_Simbolos.getReg(self.lookahead.valor.lower()) == None:
            self.Tabela_de_Simbolos.register(self.lookahead.valor.lower(), "not")
          self.match(33, aux)
    self.termo(aux)
    self.Add(aux)
    self.pilha.empilha(aux)

  def funcao_declaracao_variaveis(self, node): ## funcao_declaracao_variaveis -> "{" (declaracao_variaveis)*;
    if self.lookahead.tipo == 123:
      aux = no(token.Token("funcao_declaracao_variaveis", -18, 1))
      node.addFilho(aux)
      aux.setPai(node)
      self.match(123, aux)
      if self.lookahead.tipo == 263 and (self.lookahead.valor.lower() == "inteiro" or self.lookahead.valor.lower() == "flut" or self.lookahead.valor.lower() == "cadeia"):
        while self.lookahead.tipo == 263 and (self.lookahead.valor.lower() == "inteiro" or self.lookahead.valor.lower() == "flut" or self.lookahead.valor.lower() == "cadeia"):
          self.declaracao_variaveis(aux)
        self.pilha.empilha(aux)
      return 1

  def declaracao_variaveis_bloco(self, node): ## declaracao_variaveis_bloco -> 263 123  declaracao_variaveis* 125;
    if self.lookahead.tipo == 263:
      aux = no(token.Token("declaracao_variaveis_bloco", -19, 1))
      node.addFilho(aux)
      aux.setPai(node)
      self.match(263, aux)
      self.match(123, aux)
      while self.lookahead.tipo != 125:
        self.declaracao_variaveis(aux)
      self.match(125, aux)
      self.pilha.empilha(aux)
    else:
      return

  def linha_bloco(self, node, number=0): ## linha_bloco -> 123 (linha_lista)* 125;
    aux = no(token.Token("linha_bloco", -20, 1))
    node.addFilho(aux)
    aux.setPai(node)
    if number == 0:
      self.match(123, aux)
    while self.lookahead.tipo != 125:
      self.linha_lista(aux)
    self.match(125, aux)
    self.pilha.empilha(aux)

  def funcao_declaracao(self, node): # funcao_declaracao ->  "função" tipo_primitivo 264 "(" funcao_parametros? ")" funcao_declaracao_variaveis linha_bloco;
    #print(self.lookahead.valor.lower())
    if self.lookahead.tipo == 263:
      aux = no(token.Token("funcao_declaracao", -21, 1))
      node.addFilho(aux)
      aux.setPai(node)
      self.match(263, aux)
      self.tipo_primitivo(aux)
      self.Tabela_de_Simbolos.register(self.lookahead.valor.lower(), self.bufferTipo+":func")
      TabAux = TabelaDeSimbolos(self.lookahead.valor.lower())
      self.Tabela_de_Simbolos.setFilha(TabAux)
      TabAux.setPai(self.Tabela_de_Simbolos)
      self.Tabela_de_Simbolos = TabAux
      self.match(264, aux)
      self.match(40, aux)
      if self.lookahead.tipo != 41:
        self.funcao_parametros(aux)
      self.match(41, aux)
      self.linha_bloco(aux, self.funcao_declaracao_variaveis(aux))
      self.pilha.empilha(aux)
      self.Tabela_de_Simbolos = self.Tabela_de_Simbolos.prox_tabela

  def declaracao_algoritmo(self): # declaracao_algoritmo -> 263 123 (declaracao_variaveis_bloco)? linha_bloco (funcao_declaracao)* 125;
    aux = no(token.Token("declaracao_algoritmo", -22, 1))
    if self.lookahead.tipo == 263:
      self.match(263, aux)
      self.match(123, aux)
      self.declaracao_variaveis_bloco(aux)
      self.linha_bloco(aux)
      while self.lookahead.tipo != 125:
        self.funcao_declaracao(aux)
      self.match(125, aux)
      self.pilha.empilha(aux)

    self.arvore.Raiz = aux