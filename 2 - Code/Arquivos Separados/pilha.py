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
        print(aux.token.valor)
        self.topo = aux.prox
        self.tamanho -= 1
        return aux;
      else:
        print("Pilha vazia")
        return -1

  def esvazia(self):
    while not self.vazio():
      self.pop()
