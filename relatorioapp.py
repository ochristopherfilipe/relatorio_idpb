import requests
import pandas as pd
import streamlit as st
from datetime import datetime


# Definir o título da página
st.title('Relatório Semanal da Célula')

# Função para obter dados da célula usando a API
def obter_dados_celula(numero_celula):
    url = f'https://apiidpb.pythonanywhere.com/celulas/celula/{numero_celula}'
    response = requests.get(url)

    if response.status_code == 200:
        dados = response.json()

        if dados:
            st.write(f'O número da célula é {numero_celula}')
            st.write(f'A coordenação é {dados[0]["Coordenacao"]}')
            
            nomes_lideres = [lider["Nome"] for lider in dados]
            st.write(f'O nome do líder ou líderes é: {", ".join(nomes_lideres)}')
        else:
            st.warning(f'Nenhum dado encontrado para a célula {numero_celula}')
    else:
        st.error(f'Erro ao acessar a API. Código de status: {response.status_code}')

# Solicitar ao usuário o número da célula
st.subheader('Faça Login:')
numero_celula = st.text_input('(na verdade insira o número da celula, mas no deploy oficial vai ser a tela de login)')
if st.button('Entrar'):
    obter_dados_celula(numero_celula)
st.write('Usei uma API somente nessa primeira parte, pra funcionar o resto do codigo eu criei um banco de dados csv de acordo com as informações que pediremos')
st.markdown('---')

# Leitura do arquivo CSV para um DataFrame
nome_arquivo_csv = 'dados_igreja.csv'
df = pd.read_csv(nome_arquivo_csv)

# Simulação da interação do líder
data_relatorio = st.text_input('Informe a data do relatório (YYYY-MM-DD):')
conversao = st.checkbox('Houve conversão?')
evento = st.checkbox('Foi um evento?')

# Criar um novo DataFrame chamado lista_presenca se não existir
if 'lista_presenca' not in globals() or not isinstance(pd.DataFrame):
    lista_presenca = pd.DataFrame(columns=['Data Relatório', 'Conversão', 'Evento', 'NomeCompleto', 'Presente'])

# Verificar se a entrada do usuário não está vazia antes de converter para datetime
if data_relatorio:
    novo_registro_relatorio = {
        'Data Relatório': datetime.strptime(data_relatorio, '%Y-%m-%d').date(),
        'Conversão': conversao,
        'Evento': evento
    }

    # Adicionar informações do relatório ao DataFrame lista_presenca
    lista_presenca = pd.concat([lista_presenca, pd.DataFrame([novo_registro_relatorio])], ignore_index=True)
else:
    st.warning('A data do relatório não pode estar vazia.')

st.subheader('Marque os membros presentes:')
# Iterar sobre os nomes do DataFrame original
for nome in df['NomeCompleto']:
    # Verificar se o nome já existe no DataFrame lista_presenca
    if not lista_presenca['NomeCompleto'].isin([nome]).any():
        presente = st.checkbox(f'{nome}')
        # Adicionar novo registro ao DataFrame lista_presenca usando o método loc
        lista_presenca.loc[len(lista_presenca)] = [data_relatorio, conversao, evento, nome, presente]
    else:
        st.warning(f'{nome} já foi marcado(a) na lista de presença. Pulando para o próximo.')

# Exibir o DataFrame final
st.markdown('---')
st.subheader('Esse seria o banco de dados SQL Server etc...')
st.write(lista_presenca)
st.write('Obs.: O tratamento de dados vou fazer no Power BI')
