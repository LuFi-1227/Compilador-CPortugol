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

    print(prefixo + ponteiro + str(aux.token.valor)+":"+str(aux.token.tipo))

    N_prefixo = prefixo + segmento

    for nos in aux.filhos:
        self.Terminal(nos, N_prefixo)

  def toString(self):
    self.Terminal(self.Raiz)