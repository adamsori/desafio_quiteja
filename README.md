# Descrição do problema

Crie um script python que:

- descompacte o arquivo dados.zip;
- leia ambos arquivos descompactados (origem-dados.csv e tipos.csv);
  Com o arquivo (origem-dados.csv)
- dos dados carregados do arquivo (origem-dados.csv), filtre apenas os dados identificados como "CRÍTICO" na coluna status;
- ordene o resultado filtrado pelo campo created_at;
- inclua um novo campo "nome_tipo" que deverá ser preenchido baseado nos dados carregados do arquivo tipos.csv;
- gere um arquivo (insert-dados.sql) com os inserts (SQL) dos dados gerados nos passos anteriores (considere o nome da tabela como dados_finais e o nome das colunas que constam no arquivo csv);
- com base na estrutura desta tabela, monte uma query que retorne, por dia, a quantidade de itens agrupadas pelo tipo;

### IMPORTANTE:

- no diretório onde o script será executado estarão apenas o seu script python e o arquivo zipado;
- o arquivo a ser gerado (insert-dados.sql) deverá ser salvo no mesmo diretório;
- a organização do código e do arquivo gerado serão avaliados;

**Questões extras:**

1.  Você vê alguma relação entre o status "CRÍTICO" e algum outro dado?

    - Após analisar os arquivos origem-dados.csv e tipos.csv não consegui determinar uma relação direta entre o status 'CRÍTICO' e outro dado específico. Concluo que a relação entre o status 'CRÍTICO' e outros dados pode depender do contexto do sistema ou domínio em que esses dados estão sendo utilizados.
    - Para realizar uma análise mais profunda e verificar se há alguma correlação, e que pode ter passada despercebida através da minha primeira analise, eu utilizei o pandas para calcular a correlação entre o status 'CRÍTICO' e outras variáveis, buscando uma relação linear entre elas. Utilizei os coeficientes de Pearson e Spearman. Obtive os seguintes resultados:

          Pearson        created_at  product_code  customer_code      tipo  status_id
          created_at       1.000000      0.084010       0.117045  0.089375  -0.004484
          product_code     0.084010      1.000000       0.378207 -0.079466   0.010125
          customer_code    0.117045      0.378207       1.000000 -0.106777  -0.115688
          tipo             0.089375     -0.079466      -0.106777  1.000000  -0.052989
          status_id       -0.004484      0.010125      -0.115688 -0.052989   1.000000

      Possível correlação entre customer_code e product_code de 38%. Desconsiderei valores menores que 0.37.

          Spearman       created_at  product_code  customer_code      tipo  status_id
          created_at       1.000000      0.163277       0.001826 -0.044123   0.030329
          product_code     0.163277      1.000000       0.421374 -0.109699  -0.070821
          customer_code    0.001826      0.421374       1.000000 -0.133337  -0.150702
          tipo            -0.044123     -0.109699      -0.133337  1.000000  -0.062014
          status_id        0.030329     -0.070821      -0.150702 -0.062014   1.000000

      Possível correlação entre customer_code e product_code de 42%. Desconsiderei valores menores que 0.42.

2.  Você consegue identificar alguma outra relação?
    Não consigo identificar outra relação.
