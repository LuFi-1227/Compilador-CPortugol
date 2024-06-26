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
        a = 2; // Tentativa de Usar variavel não declarada!
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

      funcao inteiro teste0(inteiro i, flut k){
            inteiro t;
          i = i+1;
          k = k-2*3;
          t = 4*5; 
          escreval("inteiro %d, flutuante %f", i, k);
      }
    }