algoritmo{
      variaveis{ //Abre chaves para as variáveis
        inteiro i, j, k;
        inteiro cont;
        flut doubK, doubj;
        flut teste;
        cadeia String1, String2;
        cadeia caractere;
      }

      { //Abre chaves para o código
        i = -1;
        enquanto(i <= 10){
          escreva("iteraçao %d", i);
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

      funcao cadeia teste0(inteiro i, flut k){//Retorno da função não condiz com o que foi declarado
          inteiro t;
          t = 1;
          retorne t;
      }
    }