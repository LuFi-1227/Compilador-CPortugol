from sintatico import parser

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