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