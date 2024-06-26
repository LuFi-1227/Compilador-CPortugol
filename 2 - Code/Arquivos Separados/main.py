from sintatico import parser
from semantico import semantic
import os
import sys

try:
  if (sys.argv[1]):
    P = parser(sys.argv[1])
  else:
    P = parser('testefail1000.cp')
except FileNotFoundError:
  print("Arquivo não encontrado!")
  resposta = input("Deseja carregar o arquivo de Hello World? [S/n]")
  if resposta != 'n' and resposta != 'no' and resposta != 'nao' and resposta != 'not' and resposta != 'não': 
    with open('HelloWorld.cp', 'w') as file:
      file.writelines("""
      algoritmo{
        variaveis{ //Abre chaves para as variáveis
          inteiro cont;
          flut teste;
          cadeia caractere;
        }

        { //Abre chaves para o código
          escreval("Ola mundo!");
          escreval("Qual e o seu nome?");
          leia(caractere);
          escreval("Seja bem vindo, %s", caractere);
        }
      }""")
      file.close()
      #P.Tabela_de_Simbolos.toString()# __ testa a tabela
      #P.pilha.esvazia() ___ Testa a pilha
    P = parser(r'HelloWorld.cp')
  else:
    exit()
#P.Tabela_de_Simbolos.toString()
#P.arvore.toString()

S = semantic(P.Tabela_de_Simbolos, P.arvore)

try:
  open('main.c', 'r').close()
  os.system('gcc main.c -o main.exe')
  os.system('main.exe')
  os.remove('main.exe')
except:
  os.system('gcc compillated.c -o main.exe')
  os.system('main.exe')

try:
  open(r'HelloWorld.cp').close()
  resposta = input("Deseja remover  o arquivo HelloWorld?[S/n]")
  if resposta != 'n' and resposta != 'no' and resposta != 'nao' and resposta != 'not' and resposta != 'não': 
    os.remove('HelloWorld.cp')
except FileNotFoundError:
  pass

try:
  resposta = input("Deseja remover o arquivo main.c?[S/n]")
  open(r'main.c').close()
  if resposta != 'n' and resposta != 'no' and resposta != 'nao' and resposta != 'not' and resposta != 'não': 
    os.remove('main.c')
except:
  pass