[English Version](README.EN.md)

# Trabalho Prático 1 - Compiladores - 2024-2

Trabalho prático da disciplina Compiladores do curso de Ciência da Computação da Pontifícia Universidade Católica de Minas Gerais.

## Enunciado

### **Grafo de Fluxo de Controle (CFG)**

Otimizadores e seres humanos não enxergam um programa de computador da mesma maneira. Seres humanos estão mais interessados no código fonte. Porém, código fonte é extremamente diferente
de código de máquina. Além disso, sob um ponto de vista de engenharia, é apropriado que exista uma maneira comum de representar programas que seja pertinente à várias linguagens e arquiteturas.
Nesse sentido, o otimizador precisa trabalhar com uma representação intermediária do programa.

Usualmente, compiladores representam programas como [_Grafos de Fluxo de Controle_.](https://en.wikipedia.org/wiki/Control-flow_graph)

Um CFG é um grafo direto em que os nós são _blocos básicos_. Existe uma aresta que vai do bloco básico B1 ao bloco básico B2 se a execução do programa pode fluir de B1 até B2.

Veja por exemplo o código abaixo, que calcula o fatorial de um número, e seu respectivo CFG.

```
int fact ( int n) {
    int ans = 1 ;
    while (n > 1 ) {
        ans *= n ;
        n--;
    }
    return ans ;
}
```

No trabalho prático desta disciplina, trabalharemos com um arcabouço de compilação chamado LLVM (Low Level Virtual Machine). Apesar do nome, o LLVM é bem mais que uma máquina virtual de baixo nível: é um compilador e um otimizador de programas C e C++. Tem um ecossistema e uma comunidade ativa de engenheiros de compiladores que trabalham para criar novos passes e otimizações para tornar o código objeto mais eficiente.

Na Figura 2 vemos o pipeline do LLVM. O front-end ([_clang_](https://clang.llvm.org/)) transforma código C em bytecode (representação intermediária). O otimizador ([_opt_](https://llvm.org/docs/CommandGuide/opt.html)) trabalha sobre a representação intermediária, realizando passes, ou otimizações, como Propagação de Constantes, Eliminação de Código Morto, entre outras. Note que o otimizador executa várias otimizações em uma ordem arbitrária, pois é NP-Difícil determinar a sequência ótima de otimizações. Note também que, por esta razão, a saı́da do otimizador está sempre no mesmo formato da entrada, pois o código pode passar por ele infinitas vezes. O opt possui 3 níveis de agressividade, sendo o nível O3 aquele com passes e transformações mais agressivas, que podem modificar a semântica do seu programa drasticamente.

Infelizmente, não é tão trivial identificar quais passes são executados nos níveis O1, O2 e O3 do clang. [_Neste arquivo_](https://github.com/llvm-mirror/llvm/blob/master/lib/Transforms/IPO/PassManagerBuilder.cpp) é possível notar que várias transformações são adicionadas ao pipeline dependendo da variável **OptLevel**.

Por fim, após aplicadas as otimizações, o compilador estático (llc) transforma o bytecode em código de máquina para diversas arquiteturas, além de realizar otimizações dependentes de máquina (Alocação de Registradores, por exemplo).

#### **Requisitos do trabalho.**

Você deverá escrever um script em **bash** ou **python** que recebe como entrada um código fonte C (fonte.c) e produz, na saı́da, imagens no formato PNG (**main.png**, **foo.png**, ...) que representam os Grafos de Fluxo de Controle para as funções contidas no arquivo fonte.

No arquivo **cfg.zip** você vai encontrar uma pasta **src** contendo alguns programas. Você deve gerar os CFG’s para cada um dos programas contidos na pasta.

Além disso, você deve gerar também versões diferentes do CFG para cada nível de otimização do clang. Portanto, para cada código fonte, você deve gerar 4 versões de CFG: um CFG para o nível de otimização O1, outro CFG para o nível O2, e outro CFG para o nível O3. Lembrando que pode haver mais de um CFG por arquivo, uma vez que os grafos são por função e não por módulo.

Por fim, você deve observar os grafos gerados e explicar pelo menos 2 transformações ocorridas em níveis de otimização diferentes.

#### O que deve ser entregue:

Você deve entregar um arquivo .zip contendo:

1. Um script **gen_cfg.sh** ou **gen_cfg.py** que recebe como primeiro argumento um programa escrito em C e gera, como saı́da, imagens PNG representando o grafo de fluxo de controle deste programa em três níveis de otimização diferentes (O1, O2 e O3). [10 pts].
2. As imagens dos CFG’s para todos os programas contidos na pasta **src/singlesource/**, nos três níveis de otimização diferentes. [1 pt].
3. Os arquivos _.digraph_ de todos os CFG’s dos programas contidos na pasta **src/**, nos três níveis de otimização diferentes [1 pts]
4. Um PDF descrevendo **duas ou mais** transformações que são possíveis notar ao analisar o CFG de um mesmo programa após níveis de otimização diferentes. [3 pts].

#### **Considerações finais && Dicas**

1. Uma vez que você tenha o clang instalado, você pode gerar um arquivo da representação intermediária legível com a flag **-emit-llvm**.
2. Existe um passe que compila a representação intermediária para o formato **.dot**. Você consegue achar esse passe? Tente usar o comando **opt --help** para listar todos os passes possíveis.
3. A ferramenta [graphviz](https://graphviz.org/) é o software ideal para lidar com arquivos **.dot**.
4. Veja os exemplos que já tem CFG’s formados **infinity.c** & **fact.c**.
5. **Atenção!** Se a representação intermediária tiver a flag **optnone** a ferramenta opt irá ignorar quaisquer tentativas de rodar algum passe, incluindo os de geração de arquivos .dot.
6. Caso algum dos programa não compile, explique no pdf submetido qual problema houve na compilação do mesmo.
7. **Atenção!** Há mais de um arquivo .c na pasta **singlesource/**

#### **Referências**

[1] Grafos de Fluxo de Controle: https://en.wikipedia.org/wiki/Control-flow graph

[2] clang: https://clang.llvm.org/

[3] opt: https://llvm.org/docs/CommandGuide/opt.html

[4] Graphviz: https://graphviz.org/

Bom trabalho!

## Código-fonte

O código-fonte do programa desenvolvido, na linguagem de programação Python, está disponível em [gen_cfg.py](gen_cfg.py).

## Arquivos PNG

Os arquivos PNG gerados, a partir do programa desenvolvido, estão localizados em [imagens_cfg](docs/imagens_cfg).

## Arquivos Digraph

Os arquivos Digraph gerados estão em [arquivos_.digraph](docs/arquivos_.digraph).

## Relatório

O relatório desenvolvido está disponível em [Relatorio.pdf](docs/relatorio/Relatorio.pdf).