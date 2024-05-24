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