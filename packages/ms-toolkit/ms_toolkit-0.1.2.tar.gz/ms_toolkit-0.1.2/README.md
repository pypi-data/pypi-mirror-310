# ms_toolkit
Pacote para manipulação, limpeza e visualização de dados na sua versão (0.1.0)



# ms_toolkit

**ms_toolkit** é uma biblioteca Python leve e modular projetada para facilitar tarefas comuns no tratamento, limpeza, visualização e análise de dados. Este pacote oferece funções para carregar arquivos CSV, limpar dados, visualizar correlações e calcular estatísticas como média, mediana e moda, tudo em módulos bem organizados.

## Instalação

Para instalar a biblioteca, basta clonar este repositório ou usar o `pip` diretamente:

git clone https://github.com/usuario/ms_toolkit.git
##

# Ou, se você preferir, instale com pip (assumindo que o pacote foi publicado no PyPI):
- pip install ms_toolkit

## Funcionalidades
1. Carregamento de Dados
O módulo msdt fornece funções para carregar e manipular dados de arquivos CSV.

# Funções:
- ld(): Carrega um arquivo CSV para um DataFrame.

   from ms_toolkit import ld

  df = ld('arquivo.csv', sep=';')

##

# 2. Limpeza de Dados
- O módulo **msclg** oferece funções para tratar dados ausentes, duplicados e formatar as colunas.

## Funções:
dmv(): Remove valores ausentes de um DataFrame.
dr(): Remove valores duplicados de um DataFrame.
scn(): Padroniza os nomes das colunas (minúsculas e sem espaços).

from ms_toolkit import dmv, dr, scn

df_cleaned = dmv(df)
df_no_duplicates = dr(df_cleaned)
df_standardized = scn(df_no_duplicates)

##


# 3. Visualização de Dados
O módulo msvzt oferece uma função para gerar mapas de calor das correlações entre colunas de um DataFrame.

Função:
pltch(): Plota um mapa de calor da correlação entre as colunas numéricas do DataFrame.
from ms_toolkit import pltch

pltch(df)


##

# 4. Operações Estatísticas
O módulo msmt oferece funções para calcular a média, mediana e moda de listas ou arrays.

Funções:
msn(): Calcula a média.
mdn(): Calcula a mediana.
modc(): Calcula a moda.

##

from ms_toolkit import msn, mdn, modc

data = [1, 2, 2, 3, 4, 5]

media = msn(data)
mediana = mdn(data)
moda = modc(data)

print(f"Média: {media}")
print(f"Mediana: {mediana}")
print(f"Moda: {moda}")

##

# Testes
Para garantir que tudo esteja funcionando corretamente, você pode executar testes diretamente em seu Jupyter Notebook ou no Python:

from ms_toolkit import ld, dmv, pltch, msn, mdn, modc

# Teste de carregamento de CSV
df = ld('dados.csv', sep=';')

# Teste de limpeza de dados
df_cleaned = dmv(df)
df_no_duplicates = dr(df_cleaned)

# Teste de visualização de correlação
pltch(df)

# Teste de operações estatísticas
data = [1, 2, 2, 3, 4, 5, 5]
media = msn(data)
mediana = mdn(data)
moda = modc(data)

print(f"Média: {media}")
print(f"Mediana: {mediana}")
print(f"Moda: {moda}")

##

## Contribuição
Contribuições são bem-vindas! Se você deseja contribuir para este projeto, siga os passos abaixo:

Faça um fork deste repositório.
Crie uma nova branch (git checkout -b minha-feature).
Faça suas alterações e adicione os arquivos (git add .).
Faça o commit das suas alterações (git commit -m 'Adicionando uma nova feature').
Envie para o repositório remoto (git push origin minha-feature).
Abra um Pull Request.
Licença
Este projeto está licenciado sob a Licença MIT .








