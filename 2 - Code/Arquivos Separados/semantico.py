from error import error
from pilha import Pilha
from token import Token
from no import no

class semantic():
  def __init__(self, table, arvore):
    self.incluir = ["stdio.h", "stdlib.h", "string.h"]
    self.arquivoC = open('compillated.c', 'w+')
    self.Tabela_de_Simbolos = table
    self.flagPrint = 0
    self.flagScanf = 0
    self.printArgs = 0
    self.arvore = arvore
    self.error = error()
    self.pilha = Pilha()
    self.analiseSemantica()
    with open('compillated.c', 'r') as file:
      line = file.readline()
      while line:
        self.arquivoC.write(line)
        line = file.readline()
      file.close()
    self.arquivoC.close()

  def analiseSemantica(self):
    RAIZ = self.arvore.Raiz
    if RAIZ.token.tipo != -22:
      self.error.error(300)
      return -1
    self.declaracaoAlgoritmo(RAIZ)

  def termo(self,node): ## -> funcao_chamar | lvalue | literais | "(" expressao ")";
    bufferVet = None
    for filhos in node.filhos:
      if filhos.token.tipo<0:
        if filhos.token.tipo == -17:#expressao
          bufferVet = self.expressao(filhos, 0)
        elif filhos.token.tipo == -12:#funcao_chamar
          bufferVet = self.funcaoChamar(filhos)
        elif filhos.token.tipo == -1:#lvalue
          bufferVet = self.lvalue(filhos, 0)
        elif  filhos.token.tipo == -13:#literais
          bufferVet = self.literais(filhos)
    return bufferVet

  def tipoDado(self, dado):
    if dado == "inteiro" or dado == 261:
      return 261
    if dado == "flut" or dado == 262:
      return 262
    if dado == "cadeia" or dado == 256:
      return 256

  def Add(self, node): ## - > "|" expressao Add | "&" expressao  Add | ("=") expressao Add | (">"|">="|"<"|"<="|"=="|"!=") expressao Add | ("+" | "-") expressao Add | ("/"|"*"|"%") expressao Add | lambda;
    buffer = None
    buffer2 = None
    for filhos in node.filhos:
      if filhos.token.tipo < 0:
        if filhos.token.tipo == -15:#Add
          if buffer == None:
            buffer = self.Add(filhos)
          else:
            if buffer != None and buffer2 == None:
              buffer2 = self.Add(filhos)
        elif filhos.token.tipo == -17:#expressao
          if buffer == None:
            buffer = self.expressao(filhos, 0)
          else:
            if buffer != None and buffer2 == None:
              buffer2 = self.expressao(filhos, 0)
      else:
        if filhos.token.valor == "|" or filhos.token.valor == "&":
          if filhos.token.valor == "|":
            self.arquivoC.write("||")
          else:
            self.arquivoC.write("&&")
        else:
          self.arquivoC.write(filhos.token.valor)
    if buffer !=None or buffer2 != None:
      if self.tipoDado(buffer) == self.tipoDado(buffer2):
        return buffer
      else:
        if buffer == None and buffer2 != None:
          return buffer2
        else:
          if buffer != None and buffer2 == None:
            return buffer
        self.error.error(305)

  def expressao(self,node, number=0): ## expressao - > ("+"|"-"|"!")? (termo) (Add);
    buffer1 = None
    buffer2 = None
    for filhos in node.filhos: ##Se number == 0, quer dizer que fará comparação de tipos, se igual a 1, verificará se o tipo de retorno condiz com a função.
      if filhos.token.tipo < 0:
        if filhos.token.tipo == -15:#Add
          if buffer1 == None:
            buffer1 = self.Add(filhos)
          else:
            if buffer1 != None and buffer2 == None:
              buffer2 = self.Add(filhos)
        elif filhos.token.tipo == -16:#termo
          if buffer1 == None:
            buffer1 = self.termo(filhos)
          else:
            if buffer1 != None and buffer2 == None:
              buffer2 = self.termo(filhos)
      else:
        self.arquivoC.write(filhos.token.valor)
    if buffer1 != None and buffer2 != None:
      if number == 0:
        if self.tipoDado(buffer1) == self.tipoDado(buffer2):
          return buffer1
        else:
          if buffer1 == None and buffer2 != None:
            return buffer2
          else:
            if buffer1 != None and buffer2 == None:
              return buffer1
          print("Buffer1"+str(buffer1) + "Buffer2"+str(buffer2))
          self.error.error(305)
      else:
        if self.pilha.topo != None:
          if buffer1 != None:
            if self.tipoDado(buffer1) == self.tipoDado(self.pilha.topo.token.valor):
              self.pilha.pop()
              return buffer1
            else:
              print("Buffer"+str(self.tipoDado(buffer1))+ "Topo"+str(self.tipoDado(self.pilha.topo.token.valor)))
              self.error.error(306)
          else:
            if buffer2 != None:
              if self.tipoDado(buffer2) == self.tipoDado(self.pilha.topo.token.valor):
                self.pilha.pop()
                return buffer1
            else:
              print("Buffer"+str(self.tipoDado(buffer2))+ "Topo"+str(self.tipoDado(self.pilha.topo.token.valor)))
              self.error.error(306)

  def lvalue(self,node, number=0): ## -> 264 ("[" expressao "]")*; #Se number == 1, quer dizer que a linha atribuição requisita comparação de tipos
    for filhos in node.filhos:
      if number == 1:
        if filhos.token.tipo == -17:#expressao
          self.expressao(filhos, 1)
        if filhos.token.tipo == 264:
          self.arquivoC.write(filhos.token.valor)
          return self.Tabela_de_Simbolos.getReg(filhos.token.valor.lower())
      else:
        if filhos.token.tipo == -17:#expressao
          self.expressao(filhos, 1)
        if filhos.token.tipo == 264:
          if self.flagScanf == 1:
            if self.tipoDado(self.Tabela_de_Simbolos.getReg(filhos.token.valor.lower())) == 256:
              self.arquivoC.write('FILE *A = fopen("StringColeta.txt", "w"); if(A==NULL){print("Falha na execução do programa quanto a atribuição de cadeia de caracteres"); return;}else{char teclado[BUFSIZ]; setbuf(stdin, teclado); fgets(teclado, BUFSIZ, stdin); fputs(teclado, A);}')
            elif self.tipoDado(self.Tabela_de_Simbolos.getReg(filhos.token.valor.lower())) == 261:
              self.arquivoC.write('"%d", &'+filhos.token.valor)
            elif self.tipoDado(self.Tabela_de_Simbolos.getReg(filhos.token.valor.lower())) == 262:
              self.arquivoC.write('"%f", &'+filhos.token.valor)
            else:
              self.error.error(308)
            self.flagScanf = 0
          else:
            self.arquivoC.write(filhos.token.valor)

  def declaracaoVariaveisBloco(self, node): ## -> 263 123  declaracao_variaveis* 125;
    for filhos in node.filhos:
      if filhos.token.tipo < 0:
        if filhos.token.tipo == -14:#declaracao_variaveis
          self.declaracaoVariaveis(filhos)

  def tipoPrimitivo(self, node): ##  -> 263;
    bufferTipo = ""
    for filhos in node.filhos:
      if filhos.token.valor == "inteiro":
        bufferTipo = "int"
      elif filhos.token.valor == "flut":
        bufferTipo = "float"
      elif filhos.token.valor == "cadeia":
        bufferTipo = "char*"
      self.arquivoC.write(bufferTipo+" ")
      return filhos.token.valor

  def linhaAtribuicao(self,node): ## -> (lvalue) "=" (expressao) ";";
    for filhos in node.filhos:
      if filhos.token.tipo < 0:
        if filhos.token.tipo == -1:#lvalue
          self.lvalue(filhos, 1)
        elif filhos.token.tipo == -17:#expressao
          self.expressao(filhos, 1)
      else:
          self.arquivoC.write(filhos.token.valor)

  def funcaoArgumentos(self, node, number=0): ## -> (expressao) ("," expressao)*;
    cont = 0
    for filhos in node.filhos:
      if filhos.token.tipo < 0:
        if filhos.token.tipo == -17:#expressao
          self.expressao(filhos)
          cont += 1
      else:
        self.arquivoC.write(filhos.token.valor)
    if number == 1:
      if self.flagPrint == 1:
        self.flagPrint = 0
        if(self.printArgs != cont-1) and cont-1 != 0:
          print("Args da string"+str(self.printArgs)+"Contagem"+str(cont-1))
          self.error.error(307)
        self.printArgs = 0
      if self.flagScanf == 1:
        self.flagScanf = 0

    else:
      if cont != self.Tabela_de_Simbolos.getReg("numPam"):
        self.error.error(304)

  def funcaoChamar(self,node): ## -> 264 "(" (funcao_argumentos?) ")";
    NomeBuffer = ""
    flagEscreval = 0
    flag = 0
    for filhos in node.filhos:
      if filhos.token.tipo < 0:
        if filhos.token.tipo == -11:#funcao_argumentos
          if NomeBuffer != "escreva" and NomeBuffer != "leia" and NomeBuffer != "escreval":
            self.funcaoArgumentos(filhos)
          else:
            self.funcaoArgumentos(filhos, 1)
      else:
        if filhos.token.tipo==264:
          NomeBuffer = filhos.token.valor
          if NomeBuffer != "escreva" and NomeBuffer != "leia" and NomeBuffer != "escreval":
            self.Tabela_de_Simbolos = self.Tabela_de_Simbolos.getTab(NomeBuffer.lower())
            self.arquivoC.write(filhos.token.valor)
            flag = 1
          else:
            if NomeBuffer == "escreva" or NomeBuffer == "escreval":
              if NomeBuffer == "escreval":
                flagEscreval = 1
              self.arquivoC.write("printf(")
              self.flagPrint = 1
            else:
              self.arquivoC.write("scanf(")
              self.flagScanf = 1
    if flag ==1:
      self.Tabela_de_Simbolos = self.Tabela_de_Simbolos.prox_tabela
      return self.Tabela_de_Simbolos.getReg(NomeBuffer)

    self.arquivoC.write(")")
    if flagEscreval == 1:
      self.arquivoC.write(';printf("\\n")')

  def linhaRetorno(self,node): ## -> ("retorne") (expressao?) (";");
    for filhos in node.filhos:
      if filhos.token.tipo < 0:
        if filhos.token.tipo == -17:#expressao
          self.expressao(filhos, 1)
      else:
        if filhos.token.tipo==263:
          self.arquivoC.write("return ")
        else:
          self.arquivoC.write(filhos.token.valor)

  def linhaSe(self,node): ## -> ("se" )(expressao) (123) (linha_lista) (125) ("senão" 123 linha_lista 125)?;
    for filhos in node.filhos:
      if filhos.token.tipo < 0:
        if filhos.token.tipo == -17:#expressao
          self.expressao(filhos)
          self.arquivoC.write(")")
        elif filhos.token.tipo == -2:#linha_lista
          self.linhaLista(filhos)
      else:
        if filhos.token.tipo==263:
          if filhos.token.valor.lower() == "se":
            self.arquivoC.write("if(")
          else:
            self.arquivoC.write("else")
        else:
          self.arquivoC.write(filhos.token.valor)

  def linhaEnquanto(self,node):## -> "enquanto" 40 (expressao) 41 123 (linha_lista) 125;
    for filhos in node.filhos:
      if filhos.token.tipo < 0:
        if filhos.token.tipo == -17:#expressao
          self.expressao(filhos)
        elif filhos.token.tipo == -2:#linha_lista
          self.linhaLista(filhos)
      else:
        if filhos.token.tipo==263:
          self.arquivoC.write("while")
        else:
          self.arquivoC.write(filhos.token.valor)


  def linhaPara(self,node):## -> ("para") (40) (linhaAtribuicao) (59) (expressao) (59) (linha_atribuicao) (41) (123) (linha_lista) (125);
    for filhos in node.filhos:
      if filhos.token.tipo < 0:
        if filhos.token.tipo == -3:#linha_atribuicao
          self.linhaAtribuicao(filhos)
        elif filhos.token.tipo == -17:#expressao
          self.expressao(filhos)
        elif filhos.token.tipo == -2:#linha_lista
          self.linhaLista(filhos)
      else:
        if filhos.token.tipo==263:
          self.arquivoC.write("for")
        else:
          self.arquivoC.write(filhos.token.valor)

  def linhaLista(self,node):## -> linha_atribuicao | funcao_chamar ";"| linha_retorno | linha_se | linha_enquanto | linha_para;
    for filhos in node.filhos:
      if filhos.token.tipo < 0:
        if filhos.token.tipo == -3:#linha_atribuicao
          self.linhaAtribuicao(filhos)
        elif filhos.token.tipo == -4:#linha_se
          self.linhaSe(filhos)
        elif filhos.token.tipo == -5:#linha_para
          self.linhaPara(filhos)
        elif filhos.token.tipo == -6:#linha_retorno
          self.linhaRetorno(filhos)
        elif filhos.token.tipo == -7:#linha_enquanto
          self.linhaEnquanto(filhos)
        elif filhos.token.tipo == -12:#funcao_chamar
          self.funcaoChamar(filhos)
      else:
        if filhos.token.tipo==59:
          self.arquivoC.write(filhos.token.valor)

  def linhaBloco(self, node): ## -> 123 (linha_lista)* 125;
    for filhos in node.filhos:
      if filhos.token.tipo < 0:
        if filhos.token.tipo == -2:#linha_lista
          self.linhaLista(filhos)
      else:
        if filhos.token.tipo==123:
          pass
        else:
          self.arquivoC.write(filhos.token.valor)

  def funcaoParametro(self, node): ## -> tipo_primitivo 264;
    bufferTipo = ""
    for filhos in node.filhos:
      if filhos.token.tipo < 0:
        if filhos.token.tipo == -8:#tipo_primitivo
          bufferTipo = self.tipoPrimitivo(filhos)
      else:
        if filhos.token.tipo==264:
          if self.Tabela_de_Simbolos.getReg(filhos.token.valor.lower()) != bufferTipo:
            self.error.error(301)
          else:
            self.arquivoC.write(filhos.token.valor)

  def funcaoParametros(self, node): ## -> funcao_parametro (<44> funcao_parametro)*;
    for filhos in node.filhos:
      if filhos.token.tipo < 0:
        if filhos.token.tipo == -9:#funcao_parametro
          self.funcaoParametro(filhos)
      else:
        self.arquivoC.write(filhos.token.valor)
    self.arquivoC.write(')')

  def literais(self, node, number=0): # -> 261 | 262 | 256;
    if number == 2: # QUer dizer que veio da função declaração variáveis
      for filhos in node.filhos:
        if filhos.token.tipo == 261:
          self.arquivoC.write(str(filhos.token.valor))
          return filhos.token.valor
        else:
          self.error.error(302)
    else:
      for filhos in node.filhos:
        if filhos.token.tipo == 261 or filhos.token.tipo == 262 or filhos.token.tipo == 256:
          if filhos.token.tipo == 256:
            if self.flagPrint == 1:
              for i in range(len(filhos.token.valor)):
                if filhos.token.valor[i] == '%':
                  if filhos.token.valor[i+1] == 'i' or filhos.token.valor[i+1] == 'c' or filhos.token.valor[i+1] == 'f' or filhos.token.valor[i+1] == 's' or filhos.token.valor[i+1] == 'd':
                    self.printArgs += 1
                    if filhos.token.valor[i+1] == 'i':
                      filhos.token.valor[i+1] = 'd'
                    elif filhos.token.valor[i+1] == 'c':
                      filhos.token.valor[i+1] = 's'
          self.arquivoC.write(str(filhos.token.valor))
          return filhos.token.tipo
        else:
          self.error.error(303)

  def returnPrimitive(self, tipo):
    if tipo == 261:
      return 0
    elif tipo == 262:
      return 0.0
    elif tipo == 256:
      return ""

  def declaracaoVariaveis(self, node): #-> tipo_primitivo 264 (("," 264)*| ("[" literais "]")*)*";";
    bufferTipo = ""
    bufferVar = ""
    bufferVet = []
    for filhos in node.filhos:
      if filhos.token.tipo < 0:
        if filhos.token.tipo == -8:#tipo_primitivo
          bufferTipo = self.tipoPrimitivo(filhos)
        elif  filhos.token.tipo == -13:#literais
          bufferVet.append(self.literais(filhos, 2))
      else:
        if filhos.token.tipo==264:
          bufferVar = filhos.token.valor.lower()
          if self.Tabela_de_Simbolos.getReg(filhos.token.valor.lower()) != bufferTipo:
            self.error.error(301)
          else:
            self.pilha.empilha(no(Token(bufferTipo+":"+filhos.token.valor.lower(), 0, 1)))
          self.arquivoC.write(filhos.token.valor)
        else:
          if filhos.token.tipo==44 or filhos.token.tipo==59:
            if len(bufferVet)==0:
              self.Tabela_de_Simbolos.register(bufferVar, {
                  "type":"var",
                  "tipo": bufferTipo,
                  "valor": self.returnPrimitive(bufferTipo)
              })
            else:
              if len(bufferVet)==1:
                self.Tabela_de_Simbolos.register(bufferVar, {
                  "type":"vetor",
                  "tipo": bufferTipo,
                  "valorMax": bufferVet[0],
                  "valor": self.returnPrimitive(bufferTipo)
                })
              elif  len(bufferVet)>1:
                var = {
                        "type":"matriz",
                        "tipo": bufferTipo,
                        "valor": self.returnPrimitive(bufferTipo)
                      }
                for number in bufferVet:
                  var += {"valorMax"+number: number}
                self.Tabela_de_Simbolos.register(bufferVar, var)
          self.arquivoC.write(filhos.token.valor)

  def funcaoDeclaracaoVariaveis(self, node): #-> "{" (declaracao_variaveis)*;
    for filhos in node.filhos:
      if filhos.token.tipo < 0:
        if filhos.token.tipo == -14:#declaracao_variaveis
          self.declaracaoVariaveis(filhos)
      else:
        if filhos.token.tipo<255:
          if filhos.token.tipo==123:
            self.arquivoC.write(filhos.token.valor)

  def funcaoDeclaracao(self, node): #->  263 tipo_primitivo 264 "(" funcao_parametros? ")" funcao_declaracao_variaveis linha_bloco;
    flag = False
    bufferTipo = ""
    for filhos in node.filhos:
      if filhos.token.tipo < 0:
        if filhos.token.tipo == -8:#tipo_primitivo
          bufferTipo = self.tipoPrimitivo(filhos)
        elif filhos.token.tipo == -10:#funcao_parametros
          self.funcaoParametros(filhos)
          flag = True
        elif filhos.token.tipo == -18:#funcao_declaracao_variaveis
          if not flag:
            self.arquivoC.write(')')
            flag = True
          self.funcaoDeclaracaoVariaveis(filhos)
        elif filhos.token.tipo == -20:#linha_bloco
          if not flag:
            self.arquivoC.write(')')
            flag = True
          self.linhaBloco(filhos)
      else:
        if filhos.token.tipo==263:
          pass
        elif filhos.token.tipo==264 or filhos.token.tipo==29 or filhos.token.tipo==28:
          if filhos.token.tipo==264:
            #print("Função"+filhos.token.valor)
            if self.tipoDado(self.Tabela_de_Simbolos.getReg(filhos.token.valor)) != self.tipoDado(bufferTipo):
              self.error.error(301)
            else:
              self.pilha.empilha(no(Token(bufferTipo, 1, 1)))
            self.Tabela_de_Simbolos = self.Tabela_de_Simbolos.getTab(filhos.token.valor)
          self.arquivoC.write(filhos.token.valor+'(')

  def declaracaoAlgoritmo(self, node): #-> 263 123 (declaracao_variaveis_bloco)? linha_bloco (funcao_declaracao)* 125;
    self.arquivoC.write("void main()")
    flag = False
    for filhos in node.filhos:
      if filhos.token.tipo < 0:
        if filhos.token.tipo == -19:#declaracao_variaveis_bloco
          self.declaracaoVariaveisBloco(filhos)
        elif filhos.token.tipo == -20:#linha_bloco
          self.linhaBloco(filhos)
        elif filhos.token.tipo == -21:#funcao_declaracao
          if not flag:
            self.arquivoC.close()
            self.arquivoC = open('main.c', 'w+')
            for include in self.incluir:
              self.arquivoC.write("#include<"+include+">\n")
            flag = True
          self.funcaoDeclaracao(filhos)
          self.Tabela_de_Simbolos = self.Tabela_de_Simbolos.prox_tabela
      else:
        if filhos.token.tipo<255:
          if filhos.token.tipo==123:
            self.arquivoC.write(filhos.token.valor)