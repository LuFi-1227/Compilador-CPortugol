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

palavrasReservadas = ['se', 'senao', 'para', 'enquanto', 'funçao', 'inteiro', 'flut', 'variaveis', 'algoritmo', 'cadeia', 'retorne']
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
    self.tipo = self.classifier(valor, tipo)
    self.valor = valor

  def toString(self):
    print("<"+str(self.tipo)+","+str(self.valor)+">")

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
        #print(self.linhaAtual)
      return token
    return 1

  def seOperador(self, caractere):
    if '=<>|&!"/'.find(caractere) != -1:
      return 1
    else:
      if '+-*/()[]%{},;'.find(caractere) != -1:
        return 0
      return -1

class error():
  def __init__(self):
    self.errors = {
        "59" : "Ponto e vírgula não colocado",
        "40" : "Parenteses não abertos",
        "41" : "Parenteses não fechados",
        "91" : "Colchetes não abertos",
        "93" : "Colchetes não fechados",
        "123": "Chaves não foram abertas",
        "125" : "Chaves não foram fechadas",
        "256" : "Esperava-se uma String",
        "257" : "Esperava-se um maior ou igual (>=)",
        "258" : "Esperava-se um menor ou igual (<=)",
        "259" : "Esperava-se um operador de comparação (==)",
        "260" : "Esperava-se um operador de diferença (!=)",
        "261" : "Esperava-se um inteiro escrito corretamente",
        "262" : "Esperava-se um número decimal escrito corretamente",
        "263" : "Esperava-se uma palavra reservada escrita corretamente",
        "264" : "Nome de variável não aceito"
    }

  def error(self, number):
    print(self.errors[str(number)])

class no():
  def __init__(self, token, proximo=None):
    self.token = token
    self.prox = proximo
    self.pai = None
    self.filhos = []

  def setPai(self, pai):
    self.pai = pai

  def addFilho(self, filho):
    self.filhos.append(filho)

  def toString(self):
    print(self.token.valor)

class Pilha():
  def __init__(self):
    self.tamanho = 0
    self.topo = None

  def vazio(self):
    if self.topo == None:
      return 1
    return 0

  def empilha(self, no):
    no.prox = self.topo
    self.topo = no
    self.tamanho +=1

  def pop(self, number=1):
    for n in range(number):
      if not self.vazio():
        aux = self.topo
        print(aux.valor)
        self.topo = aux.prox
        self.tamanho -= 1
        return aux;
      else:
        print("Pilha vazia")
        return -1

  def esvazia(self):
    while not self.vazio():
      self.pop()

class Arvore():
  def __init__(self):
    self.Raiz = None

  def Terminal(self, aux , prefixo=""):
    ponteiro = ""
    segmento = ""
    if aux.pai == None:
      print(aux.token.valor)
    else:
      if aux.pai != None and aux.pai.filhos[-1] != aux:
        ponteiro = "├── ";
        segmento = "│   ";
      else:
        ponteiro = "└── ";
        segmento = "    ";

    print(prefixo + ponteiro + str(aux.token.valor))

    N_prefixo = prefixo + segmento

    for nos in aux.filhos:
        self.Terminal(nos, N_prefixo)

  def toString(self):
    self.Terminal(self.Raiz)

class TabelaDeSimbolos():
  def __init__(self, ident):
    self.ident = ident
    self.prox_tabela = None
    self.tabela_filha = []
    self.dicionario = dict()

  def register(self, chave, tipo):
    self.dicionario.setdefault(chave, tipo)

  def getReg(self, chave):
    return self.dicionario.get(chave)

  def setFilha(self, novaTabela):
    self.tabela_filha.append(novaTabela)

  def setPai(self, tabela):
    self.prox_tabela = tabela

  def getTab(self,ident):
    for tabela in self.tabela_filha:
      if ident == self.tabela_filha.ident:
        return self.tabela_filha

  def dictToString(self):
    for d in self.dicionario:
      print(d + ":" + self.dicionario[d])

  def toString(self):
    print("{")
    self.dictToString()
    for filho in self.tabela_filha:
      filho.toString()
    print("}")

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
    aux = no(Token("lvalue", -1, 1))
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
      aux = no(Token("linha_lista", -2, 1))
      node.addFilho(aux)
      aux.setPai(node)
      self.linha_para(aux)
      self.pilha.empilha(aux)
    else:
      if self.lookahead.valor.lower() == "enquanto":
        aux = no(Token("linha_lista", -2, 1))
        node.addFilho(aux)
        aux.setPai(node)
        self.linha_enquanto(aux)
        self.pilha.empilha(aux)
      else:
        if self.lookahead.valor.lower() == "se":
          aux = no(Token("linha_lista", -2, 1))
          node.addFilho(aux)
          aux.setPai(node)
          self.linha_se(aux)
          self.pilha.empilha(aux)
        else:
          if self.lookahead.valor.lower() == "retorne":
            aux = no(Token("linha_lista", -2, 1))
            node.addFilho(aux)
            aux.setPai(node)
            self.linha_retorno(aux)
            self.pilha.empilha(aux)
          else:
            if self.lookahead.tipo == 264:
              aux = no(Token("linha_lista", -2, 1))
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
    aux = no(Token("linha_atribuicao", -3, 1))
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
      aux = no(Token("linha_se", -4, 1))
      node.addFilho(aux)
      aux.setPai(node)
      self.match(263, aux)
      self.expressao(aux)
      self.match(123, aux)
      self.linha_lista(aux)
      self.match(125, aux)
      self.pilha.empilha(aux)
    if self.lookahead.tipo == 263 and self.lookahead.valor.lower() == "senao":
      aux = no(Token("linha_se", -4, 1))
      node.addFilho(aux)
      aux.setPai(node)
      self.match(263, aux)
      self.match(123, aux)
      self.linha_lista(aux)
      self.match(125, aux)
      self.pilha.empilha(aux)

  def linha_para(self, node): ## linha_para -> "para" 40 linha_atribuicao 59 expressao 59 linha_atribuicao 41 123 linha_lista 125;
    if self.lookahead.tipo == 263:
      aux = no(Token("linha_para", -5, 1))
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
      aux = no(Token("linha_retorno", -6, 1))
      node.addFilho(aux)
      aux.setPai(node)
      self.match(263, aux)
      if self.lookahead.tipo != 59:
        self.expressao(aux)
      self.match(59, aux)
      self.pilha.empilha(aux)

  def linha_enquanto(self, node): ## linha_enquanto -> "enquanto" 40 expressao 41 123 linha_lista 125;
    if self.lookahead.tipo == 263:
      aux = no(Token("linha_enquanto", -7, 1))
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
      aux = no(Token("tipo_primitivo", -8, 1))
      node.addFilho(aux)
      aux.setPai(node)
      self.bufferTipo = self.lookahead.valor.lower()
      self.match(263, aux)
      self.pilha.empilha(aux)

  def funcao_parametro(self, node): ## funcao_parametro -> tipo_primitivo 264;
    aux = no(Token("funcao_parametro", -9, 1))
    node.addFilho(aux)
    aux.setPai(node)
    self.tipo_primitivo(aux)
    self.Tabela_de_Simbolos.register(self.lookahead.valor.lower(), self.bufferTipo)
    self.match(264, aux)
    self.pilha.empilha(aux)

  def funcao_parametros(self, node): ## funcao_parametros -> funcao_parametro (<44> funcao_parametro)*;
    aux = no(Token("funcao_parametros", -10, 1))
    node.addFilho(aux)
    aux.setPai(node)
    self.funcao_parametro(aux)
    while self.lookahead.tipo == 44:
      self.match(44, aux)
      self.funcao_parametro(aux)
    self.pilha.empilha(aux)

  def funcao_argumentos(self, node): ## funcao_argumentos -> expressao ("," expressao)*;     _____ Quando chama a função
    aux = no(Token("funcao_argumentos", -11, 1))
    node.addFilho(aux)
    aux.setPai(node)
    self.expressao(aux)
    while self.lookahead.tipo == 44:
      self.match(44, aux)
      self.expressao(aux)
    self.pilha.empilha(aux)

  def funcao_chamar(self, node): ## funcao_chamar -> 264 "(" funcao_argumentos? ")";
    if self.lookahead.tipo == 264:
      aux = no(Token("funcao_chamar", -12, 1))
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
      aux = no(Token("literais", -13, 1))
      node.addFilho(aux)
      aux.setPai(node)
      self.match(261, aux)
      self.pilha.empilha(aux)
    else:
      if self.lookahead.tipo == 262:
        aux = no(Token("literais", -13, 1))
        node.addFilho(aux)
        aux.setPai(node)
        self.match(262, aux)
        self.pilha.empilha(aux)
      else:
        if self.lookahead.tipo == 256:
          aux = no(Token("literais", -13, 1))
          node.addFilho(aux)
          aux.setPai(node)
          self.match(256, aux)
          self.pilha.empilha(aux)

  def declaracao_variaveis(self, node): ## declaracao_variaveis -> tipo_primitivo 264 (("," 264)*| ("[" literais "]")*)*";";
    aux = no(Token("declaracao_variaveis", -14, 1))
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
      aux = no(Token("Add", -15, 1))
      node.addFilho(aux)
      aux.setPai(node)
      flag = 10
      self.match(124, aux)
    else:
      if self.lookahead.tipo == 38: # "&"
        aux = no(Token("Add", -15, 1))
        node.addFilho(aux)
        aux.setPai(node)
        flag = 10
        self.match(38, aux)
      else:
        if self.lookahead.tipo == 61: # ("=")
          aux = no(Token("Add", -15, 1))
          node.addFilho(aux)
          aux.setPai(node)
          flag = 10
          self.match(61, aux)
        else:
          if self.lookahead.tipo == 62 or self.lookahead.tipo == 257 or self.lookahead.tipo == 60 or self.lookahead.tipo == 258 or self.lookahead.tipo == 259 or self.lookahead.tipo == 260:
          # (">"|">="|"<"|"<="|"=="|"!=")
            aux = no(Token("Add", -15, 1))
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
              aux = no(Token("Add", -15, 1))
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
                aux = no(Token("Add", -15, 1))
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
      aux = no(Token("termo", -16, 1))
      node.addFilho(aux)
      aux.setPai(node)
      self.match(40, aux)
      self.expressao(aux)
      self.match(41, aux)
      self.pilha.empilha(aux)
    else:
      aux = no(Token("termo", -16, 1))
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
    aux = no(Token("expressao", -17, 1))
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
      aux = no(Token("funcao_declaracao_variaveis", -18, 1))
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
      aux = no(Token("declaracao_variaveis_bloco", -19, 1))
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
    aux = no(Token("linha_bloco", -20, 1))
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
      aux = no(Token("funcao_declaracao", -21, 1))
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
    aux = no(Token("declaracao_algoritmo", -22, 1))
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

try:
  P = parser(r'tt.cp')
except FileNotFoundError:
  with open('tt.cp', 'w') as file:
    file.writelines("""
    algoritmo{
      variaveis{
        inteiro i, j, k;
        inteiro cont;
        flut doubK, doubj;
        flut teste;
        cadeia String1, String2;
        cadeia caractere;
      }
      {
        enquanto(i <= 10){
          escreva("iteraçao", i);
          i = i + 1;
          j = j + 2;
        }

        para(k = 0; k<10; k = k + 1){
          Se(k == 2){
            escreval("Rodou");
          }senao{
            escreval("Teste");
          }
        }
      }

      funçao inteiro teste0(inteiro i, flut k){
          i = i+1;
          k = k+2;
          escreval("inteiro" + i + "flutuante" + k);
      }

      funçao cadeia teste2(){
          inteiro i;
          flut k;
          i = 10;
          k = 20;
          retorne("inteiro"+ i+ "flutuante"+ k);
      }
    }""")
    file.close()
    # P.Tabela_de_Simbolos.toString() __ testa a tabela
    P = parser(r'tt.cp')

P.arvore.toString()