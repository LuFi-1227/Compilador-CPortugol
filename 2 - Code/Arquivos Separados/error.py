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
        "264" : "Nome de variável não aceito",
        "300" : "Erro na memória, árvore sintática não está correta",
        "301" : "Erro de compilação ao salvar tipo de função",
        "302" : "Tentativa de criar um vetor com um número não inteiro de elementos",
        "303" : "Tentativa de um não literal se passar por um valor literal",
        "304" : "Tentativa de chamar função com o número errado de parâmetros",
        "305" : "Tipos de dados diferentes",
        "306" : "Tipo de retorno da função não condiz com tipo da função",
        "307" : "Numero de variáveis fornecidas no print não é condizente com o número de variáveis chamadas na String",
        "308" : "Tipo de variável não reconhecida no Scanf"
    }

  def error(self, number):
    if number < 300:
      print("Erro sintático:"+self.errors[str(number)])
    else:
      print("Erro semântico:"+self.errors[str(number)])
    exit()
