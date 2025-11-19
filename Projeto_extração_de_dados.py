import camelot
import pandas as pd
import json
import streamlit as st
from io import StringIO

def coleta_de_dados_pessoias_Nome(tabela1):
    nome = str(tabela1.iloc[10, 0]).split()
    nome = ' '.join(nome[1:])
    return nome

def coleta_de_dados_pessoias_Data_Nascimento(tabela1):
    data_nascimento = str(tabela1.iloc[11, 0]).split()
    data_nascimento = data_nascimento[3]
    return data_nascimento

def coleta_de_dados_pessoias_Matricula(tabela1):
    matricula = str(tabela1.iloc[10, 1]).split()
    matricula = matricula[1]
    return matricula

def coleta_de_dados_pessoias_Primeiro_Eletivo(tabela2):
    if tabela2.iloc[5, 1] == 'ENADE':
        primeiro_ano_eletivo = tabela2.iloc[5, 0]
    else:
        primeiro_ano_eletivo = tabela2.iloc[6, 0]
    return primeiro_ano_eletivo

def coleta_de_dados_Componetes_Curriculares_ENADE(tabela2, tabela3):
    '''coleta de dados compontes curriculares:(tabela2, tabela3)
    ->Caso a verificação seja Verdadeira para 'ENADE' acontecera um laço que coletara as informações
    de forma relugar ate o ultimo regitro, onde ocorre uma quebra de regitro e o regirto fica divido
    entre a segunda e a terceira pagina, para isso o except IndexError existe pra coleta a regitro da que se encontra
    em uma unica linha na segunda pagina do pdf e no ultimo regitro do DataFrame
    ->No segundo laço, alguns regitros com: ESTAGIO I,apresenta suas informações somente em uma linha, para isso
    :param
    '''
    tabela2 = tabela2.drop([0, 1, 2, 3, 4, 5])
    tabela2 = tabela2.reset_index(drop=True)
    componentes_curriculares = []
    try:
        for i in range(0, len(tabela2), 3):
            componentes_curriculares.append({
                'Componente curricular': tabela2.iloc[i, 2],
                'CH': tabela2.iloc[i + 1, 3],
                'Media': tabela2.iloc[i + 1, 6]
            })
    except IndexError:
        componentes_curriculares.append({
            'Componente curricular': tabela2.iloc[i, 2],
            'CH': tabela2.iloc[i, 3],
            'Media': tabela2.iloc[i, 6]
        })
    tabela3 = tabela3.drop([0, 1, 2, 3, 4, 5])
    tabela3 = tabela3.reset_index(drop=True)
    i = 0
    while i < len(tabela3):
        if tabela3.iloc[i, 3] in ['ESTAGIO I', 'TRABALHO DE CONCLUSAO DE CURSO I',
                              'ATIVIDADES CURRICULARES COMPLEMENTARES I',
                              'ATIVIDADES CURRICULARES COMPLEMENTARES II', 'ATIVIDADES CURRICULARES COMPLEMENTARES III',
                              'ATIVIDADES COMPLEMENTARES IV', 'ESTAGIO II']:
            componentes_curriculares.append({
                'Componente curricular': tabela3.iloc[i, 3],
                'CH': tabela3.iloc[i, 4],
                'Media': tabela3.iloc[i, 7]
            })
            i += 1
        else:
            componentes_curriculares.append({
                'Componente curricular': tabela3.iloc[i, 3],
                'CH': tabela3.iloc[i + 1, 4],
                'Media': tabela3.iloc[i + 1, 7]
            })
            i += 3
    return componentes_curriculares

def coleta_de_dados_Componetes_Curriculares_NAO_ENADE(tabela2, tabela3):
    tabela2 = tabela2.drop([0, 1, 2, 3, 4])
    tabela2 = tabela2.reset_index(drop=True)
    componentes_curriculares = []
    for i in range(0, len(tabela2), 3):
        componentes_curriculares.append({
            'Componente curricular': tabela2.iloc[i, 2],
            'CH': tabela2.iloc[i + 1, 3],
            'Media': tabela2.iloc[i + 1, 6]
        })
    tabela3 = tabela3.drop([0, 1, 2, 3, 4])
    tabela3 = tabela3.reset_index(drop=True)
    i = 0
    while i < len(tabela3):
        if tabela3.iloc[i, 3] in ['ESTAGIO I', 'TRABALHO DE CONCLUSAO DE CURSO I',
                              'ATIVIDADES CURRICULARES COMPLEMENTARES I',
                              'ATIVIDADES CURRICULARES COMPLEMENTARES II', 'ATIVIDADES CURRICULARES COMPLEMENTARES III',
                              'ATIVIDADES COMPLEMENTARES IV', 'ESTAGIO II']:
            componentes_curriculares.append({
                'Componente curricular': tabela3.iloc[i, 3],
                'CH': tabela3.iloc[i, 4],
                'Media': tabela3.iloc[i, 7]
            })
            i += 1
        else:
            componentes_curriculares.append({
                'Componente curricular': tabela3.iloc[i, 3],
                'CH': tabela3.iloc[i + 1, 4],
                'Media': tabela3.iloc[i + 1, 7]
            })
            i += 3
    return componentes_curriculares




tables = st.file_uploader("Upload data", type='pdf')
tabelas = camelot.read_pdf(tables, pages='1,2,3', flavor='stream')
Primeira_tabela = tabelas[0].df
Segunda_tabela= tabelas[1].df
Terceira_tabela = tabelas[2].df

nome = coleta_de_dados_pessoias_Nome(Primeira_tabela)
data_nascimento = coleta_de_dados_pessoias_Data_Nascimento(Primeira_tabela)
matricula = coleta_de_dados_pessoias_Matricula(Primeira_tabela)
primeiro_ano_eletivo = coleta_de_dados_pessoias_Primeiro_Eletivo(Segunda_tabela)

dados_pessoais = [
    {'Nome': nome},
    {'Data de nascimento': data_nascimento},
    {'Matricula': matricula},
    {'Primeiro ano eletivo': primeiro_ano_eletivo}
]

# Essa proxima linha é feito uma verificação no DataFrame se na linha 5, coluna 1 se encontra um regitro
# com uma str 'ENADE'
if Segunda_tabela.iloc[5, 1] == 'ENADE':
    componentes_curriculares = coleta_de_dados_Componetes_Curriculares_ENADE(Segunda_tabela, Terceira_tabela)

else:
    componentes_curriculares = coleta_de_dados_Componetes_Curriculares_NAO_ENADE(Segunda_tabela, Terceira_tabela)


dados_coletados = {
    'dados pessoais': dados_pessoais, 'componentes curriculares': componentes_curriculares
}

output = json.dumps(dados_coletados, indent=4)
st.download_button(
    label="Download JSON",
    data=output,
    file_name="dados_coletados.json",
    icon=":material/download:",
)
