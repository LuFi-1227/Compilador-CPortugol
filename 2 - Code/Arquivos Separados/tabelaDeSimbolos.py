class TabelaDeSimbolos():
  def __init__(self, ident):
    self.ident = ident.lower()
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
      if ident == tabela.ident:
        return tabela

  def dictToString(self):
    for d in self.dicionario:
      print(str(d) + ":" + str(self.dicionario[d]))

  def toString(self):
    print(self.ident+"{")
    self.dictToString()
    for filho in self.tabela_filha:
      filho.toString()
    print("}")
