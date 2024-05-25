# Compilador-CPortugol
Trabalho obrigatório da Disciplina de Compiladores 2024/01 ministrada pela professora Anna Paula

# 1. Introdução:
Este repositório contém a implementação de um compilador feito para compilar uma linguagem nomeada pelos criadores como CPortugol. Neste documento, você encontrará todo o embasamento teórico utilizado para a construção do compilador e algumas especificações acerca do CPortugol. O objetivo aqui é apresentar um trabalho final para a disciplina citada anteriormente. Porém, também tem-se como objetivo secundário o compartilhamento de recursos teóricos e práticos para trabalhos futuros ou melhor, a contribuição intelectual dos autores do repositório para quem puder e quiser utilizar o que for disponibilizado aqui.

## 1.1 Linguagem utilizada:
A linguagem utilizada no desenvolvimento deste projeto foi a linguagem python, cuja documentação pode ser encontrada nas referências deste trabalho. Portanto, utiliza-se o Python para reconhecer CPortugol.

## 1.2 Porquê o nome da linguagem é CPortugol:
O nome da linguagem foi derivado de C (da linguagem C) unido com Portugol (linguagem de programação esturturada na língua portuguesa), logo, ficou nomeada como CPortugol, sendo filha direta do GPortugol mas com a diferença de utilizar os delimitadores da linguagem C com o fim de facilitar a conversão de paradigmas do Portugol para C por parte dos estudantes de Lógica de Programação. O GPortugol foi criado por Thiago Silva como uma linguagem (ou pseudo-linguagem) para que se inicie em lógica de programação de forma mais fácil. Sua documentação se encontra nas referências do trabalho, bem como na pasta nomeada como Referências, neste repositório.

# 2. Analisador Léxico:
## 2.1 O que faz um analisador léxico:
Um analisador léxico de um compilador pode ser descrito, em sua forma mais simples, como um autômato, pois seu objetivo é reconhecer as entradas no compilador (código objeto) e transformar cada entrada em um token. Um token é a menor parte de um código, ou seja, é uma palavra, um sinal, uma pontuação ou um delimitador. Portanto, um analisador léxico serve para reconhecer e transmitir cada parte do código para o nível abaixo de si. Neste caso, o nível abaixo do analisador léxico é o analisador sintático, e depois dele vem o analisador semântico. Estes 3 analisadores compõe a parte do Front-end do compilador, conforme a imagem abaixo:
![image](https://github.com/LuFi-1227/Compilador-CPortugol/assets/129668645/838381c8-5c10-4952-a993-b33d458253dc)

Portanto, a entrada do Analisador Sintático é o código fonte e a saída são uma sequência de Tokens provenientes deste código fonte com o objetivo de facilitar a compilação do código-objeto.Para que isto ocorra, o analisador léxico deve fazer 3 coisas:
1. Ignorar espaços;
2. <>
3. 

## 2.2 Convenções deste Analisador Léxico:
### 2.2.1 Tabela de palavras reservadas:
### 2.2.2 Tabela de símbolos:

## 2.3 Autômato léxico CPortugol:
O autômato utilizado na construção do compilador deste repositório é o seguinte autômato:
<automato>
### 2.3.1 Ignorando espaços:

# 3. Analisador Sintático:
# 4. Analisador Semântico:
# 5. Linguagem CPortugol:
# Referências:
- [Documentação Python]()
- [Documentação GPortugol](https://lapolli.pro.br/escolas/unicid/tecProg/laboratorio/portugol/portugol.pdf)
- [Resumo do livro de compiladores (livro do dragão)](https://github.com/ufpb-computacao/compiladores-livro/blob/master/livro/capitulos/1-introducao.asc)
