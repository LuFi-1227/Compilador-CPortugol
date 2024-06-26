from sintatico import parser
from semantico import semantic

try:
 P = parser(r'AA.cp')
except FileNotFoundError:
  with open('AA.cp', 'w') as file:
    file.writelines("""
    algoritmo{
      variaveis{ //Abre chaves para as variáveis
        inteiro cont;
        flut teste;
        cadeia caractere;
      }

      { //Abre chaves para o código
        escreval("Olá mundo!");
      }
    }""")
    file.close()
    #P.Tabela_de_Simbolos.toString()# __ testa a tabela
    # P.pilha.esvazia() ___ Testa a pilha
    P = parser(r'AA.cp')
#P.Tabela_de_Simbolos.toString()
#P.arvore.toString()

S = semantic(P.Tabela_de_Simbolos, P.arvore)

import os
try:
  open(r'compillated.c')
  os.remove('compillated.c')
except FileNotFoundError:
  pass

os.system('gcc main.c -o main.exe')
os.system('./main.exe')