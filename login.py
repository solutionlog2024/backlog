import streamlit as st
import pandas as pd
import unicodedata
from datetime import datetime
import plotly.express as px

# Definindo credenciais
usuarios = {
    "operacao_melitta": "melitta123",
    "operacao_droetker": "droetker123@"
}

# Inicializa o estado de sessão
if "logado" not in st.session_state:
    st.session_state.logado = False

# Configurações da página
st.set_page_config(page_title='📊 Análise Operação - Solution', layout="wide")


# Aplica CSS para deixar o banner fixo
st.markdown("""
    <style>
        .banner {
            position: fixed;
            top: 0;
            left: 0;
            width: 10%;
            z-index: 9999;
            background-color: white;
            padding: 10px 0;
        }
        .block-container {
            padding-top: 40px; /* Deixa espaço para o banner */
        }
    </style>
""", unsafe_allow_html=True)

# Cria o banner com a classe personalizada
st.markdown('<div class="banner">', unsafe_allow_html=True)
st.image('gpt01.png', use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)



# Atualiza o CSS personalizado para tema DARK
st.markdown("""
    <style>
        /* Fundo geral da aplicação */
        .stApp {
            background-color: #DAE5D9; /* Fundo escuro sólido */
            color: Black; /* Cor do texto */
            font-family: 'Arial', sans-serif;
        }

        /* Títulos e subtítulos */
        h1, h2, h3, h4, h5, h6 {
            color: black; /* Títulos em branco */
        }

        /* Textos e rótulos */
        label, .stMarkdown, div.css-1n76uvr, div.css-16huue1 {
            color: Black; /* Rótulos e textos em branco */
        }

        /* Botões */
        .stButton button {
            background: linear-gradient(135deg, #4caf50, #388e3c);
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            font-size: 0.9rem;
            border-radius: 8px;
            cursor: pointer;
            transition: background 0.3s ease;
        }

        .stButton button:hover {
            background: linear-gradient(135deg, #388e3c, #2e7d32);
        }

        /* Campos de entrada */
        input, select, textarea {
            background-color: #1e1e1e; /* Fundo escuro */
            color: white; /* Texto branco */
            border: 1px solid #90caf9;
            border-radius: 8px;
            padding: 0.5rem;
        }

        input:focus, select:focus, textarea:focus {
            border-color: #2196f3;
            outline: none;
        }

        /* Tabelas */
        .stDataFrame {
            border: 1px solid #90caf9;
            border-radius: 8px;
            overflow: hidden;
        }

        /* Gráficos */
        .plotly-chart {
            margin-top: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        }

        /* Rodapé */
        .footer {
            text-align: center;
            margin-top: 20px;
            font-size: 0.9rem;
            color: white; /* Letras brancas */
        }

        .footer caption {
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Função para tela de login
def tela_login():
    st.markdown('<h2>Login do Sistema</h2>', unsafe_allow_html=True)

    usuario = st.text_input("Usuário", key="usuario_input")
    senha = st.text_input("Senha", type="password", key="senha_input")

    if st.button("Entrar"):
        if usuario in usuarios and usuarios[usuario] == senha:
            st.success("Login realizado com sucesso!")
            st.session_state.logado = True
            st.session_state.usuario = usuario
            st.session_state.senha = senha
            st.rerun()
        else:
            st.error("Usuário ou senha incorretos.")

    st.markdown('</div>', unsafe_allow_html=True)

# Função para tela principal
def tela_backlog():
    st.title("Backlog 📦")
    st.write(f"Bem-vindo, **{st.session_state.usuario}**!")

    # URLs das planilhas
    url_melitta = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vRb6p983tl1uDwwBOKYCh60bdz41wxE1v8RwwRTRvEGZ6CP9MmEjNjtt6E2e0WQRPfXEDzo32MT_JD8/pubhtml'
    url_droetker = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQjFUi6NFR9F-HZGkdl_eXjbLlZRfc52naCrZOcOOqXwCBmLTYMCyLnJRwr4TlZcw8rTNMoFNelCVfg/pubhtml'

    # ____________________________________________________________MELITTA_______________________________________________________
    if st.session_state.usuario == "operacao_melitta":
        # Lê a tabela bruta
        melitta_raw = pd.read_html(url_melitta)[0]
        # Define a primeira linha como cabeçalho
        melitta_raw.columns = melitta_raw.iloc[0]
        # Remove a primeira linha (que agora está no cabeçalho) e reseta o índice
        melitta = melitta_raw[1:].reset_index(drop=True)
        melitta = melitta.dropna(how='all')
        melitta = melitta.drop(columns=melitta.columns[-1])        
        
        # Eliminando os acentos e caracteres deixando limpo
        melitta.columns = [
            unicodedata.normalize('NFKD', str(col)).encode('ASCII', 'ignore').decode('utf-8')
            for col in melitta.columns
        ]
        
        # Exibe o dataframe formatado
        melitta.rename(columns=lambda x: x.strip(), inplace=True)  # Remove espaços extras
        
        # Verificar se a coluna existe antes de renomear
        if 'Status da Separacao' in melitta.columns:
            melitta.rename(columns={'Satus da SeparaAAo': 'Status Separacao'}, inplace=True)
        elif 'Satus_da_SeparaAAo' in melitta.columns:
            melitta.rename(columns={'Satus_da_SeparaAAo': 'Status Separacao'}, inplace=True)
        elif 'Satus da SeparaAAo' in melitta.columns:
            melitta.rename(columns={'Satus da SeparaAAo': 'Status Separacao'}, inplace=True)
        
        # Converter coluna para float antes de qualquer filtro
        melitta['Faturado (Kg)'] = melitta['Faturado (Kg)'].astype(str).str.replace('.', '').str.replace(',', '.').astype(float)
        
        st.subheader("Backlog - Melitta")
        
        # Criar filtro por data e aplicá-lo ao dataframe
        selected_dates = st.multiselect(
            "Selecione uma data para filtrar:", 
            options=melitta['Data'].unique(), 
        )
        
        # Aplica o filtro de data se o usuário selecionou alguma data
        if selected_dates:
            filtered_melitta = melitta[melitta['Data'].isin(selected_dates)]
        else:
            filtered_melitta = melitta  # Se nenhuma data selecionada, usa o dataframe completo
           
        # Filtro por UF
        ufs = ["Todas"] + list(filtered_melitta['UF'].unique())  # Adiciona a opção "Todas" no início
        uf_filtro = st.selectbox(
            "Selecione uma UF para filtrar:",
            options=ufs,
            index=0  # Define "Todas" como padrão
        )

        # Filtra o dataframe com base na UF selecionada
        if uf_filtro != "Todas":
            filtered_melitta = filtered_melitta[filtered_melitta['UF'] == uf_filtro]

        # Filtro por Status Separação
        status_separacao = ["Todas"] + list(filtered_melitta['Status Separacao'].unique())  # Adiciona a opção "Todas" no início
        status_filtro = st.selectbox(
            "Selecione um Status de Separação:",
            options=status_separacao,
            index=0  # Define "Todas" como padrão
        )

        # Filtra o dataframe com base no Status de Separação selecionado
        if status_filtro != "Todas":
            filtered_melitta = filtered_melitta[filtered_melitta['Status Separacao'] == status_filtro]

        # Filtro por Status de Carregamento
        status_carregamento = ["Todas"] + list(filtered_melitta['Status de Carregamento'].unique())  # Adiciona a opção "Todas" no início
        status_carregamento_filtro = st.selectbox(
            "Selecione um Status de Carregamento:",
            options=status_carregamento,
            index=0  # Define "Todas" como padrão
        )

        # Filtra o dataframe com base no Status de Carregamento selecionado
        if status_carregamento_filtro != "Todas":
            filtered_melitta = filtered_melitta[filtered_melitta['Status de Carregamento'] == status_carregamento_filtro]

        # Filtro por Transportadora
        transportadoras = ["Todas"] + list(filtered_melitta['Transportadora'].unique())  # Adiciona a opção "Todas" no início
        transportadora_filtro = st.selectbox(
            "Selecione uma Transportadora:",
            options=transportadoras,
            index=0  # Define "Todas" como padrão
        )

        # Filtra o dataframe com base na Transportadora selecionada
        if transportadora_filtro != "Todas":
            filtered_melitta = filtered_melitta[filtered_melitta['Transportadora'] == transportadora_filtro]

        # Exibe o dataframe filtrado
        st.dataframe(filtered_melitta, use_container_width=True)

        # Converte o dataframe filtrado para CSV
        csv = filtered_melitta.to_csv(index=False).encode('utf-8')

        # Adiciona o botão de download
        st.download_button(
            label="📥 Baixar Dados Filtrados",
            data=csv,
            file_name='dados_filtrados.csv',
            mime='text/csv'
        )

        # Resumo do Carregamento por Status de Carregamento
        st.subheader("Atualizado em " + datetime.now().strftime("%y-%m-%d %H:%M:%S"))
        st.header("🚚 Resumo Operacional por Status")
        
        # Aplicar o mesmo filtro para todos os dataframes e gráficos
        # Agrupar por Status de Carregamento usando o dataframe filtrado
        df_resumo = filtered_melitta.groupby('Status de Carregamento', as_index=False).agg({'Faturado (Kg)': 'sum'})
        df_separacao = filtered_melitta.groupby('Status Separacao', as_index=False).agg({'Faturado (Kg)': 'sum'})
        df_transportadora = filtered_melitta.groupby('Transportadora', as_index=False).agg({'Faturado (Kg)': 'sum'})
        
        st.dataframe(df_separacao, use_container_width=True)
        st.dataframe(df_resumo, use_container_width=True)
        st.dataframe(df_transportadora, use_container_width=True)
        

        # Criando um gráfico de Barras para Transportadora usando dados filtrados
        fig = px.bar(df_transportadora, x='Transportadora', y='Faturado (Kg)', title='Resumo por Transportadora')
        fig.update_layout(xaxis_title='Transportadora', yaxis_title='Faturado (Kg)')
        st.plotly_chart(fig)

    # ____________________________________________________________DR. OETKER_______________________________________________________
    elif st.session_state.usuario == "operacao_droetker":
        st.subheader("Backlog - Dr. Oetker")

        # Lê a tabela da URL
        oetker_raw = pd.read_html(url_droetker)[0]

        # Remove colunas totalmente vazias antes de definir o cabeçalho
        oetker_raw = oetker_raw.dropna(axis=1, how='all')

        # Define a primeira linha como cabeçalho
        oetker_raw.columns = oetker_raw.iloc[0]
        oetker = oetker_raw[1:].reset_index(drop=True)

        # Remove colunas totalmente vazias novamente, se ainda existirem
        oetker = oetker.dropna(axis=1, how='all')

        # Remove linhas totalmente vazias
        oetker = oetker.dropna(how='all')

        # Remove colunas duplicadas
        oetker = oetker.loc[:, ~oetker.columns.duplicated()]

        # Limpa nomes das colunas (remove acentos e espaços)
        oetker.columns = [
            unicodedata.normalize('NFKD', str(col)).encode('ASCII', 'ignore').decode('utf-8').strip()
            for col in oetker.columns
        ]

        # Realizando filtros por data planejamento
        filtros = st.multiselect(
            "Selecione uma data para filtrar:", 
            options=oetker['Data Planejamento'].unique(), 
        )

        # Aplica o filtro de data se o usuário selecionou alguma data
        if filtros:
            filtered_oetker = oetker[oetker['Data Planejamento'].isin(filtros)]  # Corrigido para usar 'filtros'
        else:
            filtered_oetker = oetker  # Se nenhuma data selecionada, usa o dataframe completo
            

        # Exemplo de substituição de valores incorretos
        filtered_oetker['UF'] = filtered_oetker['UF'].replace({
            "mestre": "SP",
            "Educação Fisica": "RJ",
            "enfermeira registrada": "MG"
        })

        # Adiciona a opção "Todas" no início da lista de UFs
        ufs = ["Todas"] + list(filtered_oetker['UF'].unique())

        # Filtro por UF
        uf_filtro = st.selectbox(
            "Selecione uma UF para filtrar:",
            options=ufs,
            index=0  # Define "Todas" como padrão
        )

        # Filtro por Status de Separação
        status_filtro = st.selectbox(
            "Selecione um Status de Separação:",
            options=["Todas"] + list(filtered_oetker['Status SeparaAAo'].unique()),
            index=0  # Define "Todas" como padrão
        )

        # Filtro por Status de Carregamento
        status_carregamento_filtro = st.selectbox(
            "Selecione um Status de Carregamento:",
            options=["Todas"] + list(filtered_oetker['Status Carregaento'].unique()),
            index=0  # Define "Todas" como padrão
        )

        # Filtra o dataframe com base na UF selecionada
        if uf_filtro != "Todas":
            filtered_oetker = filtered_oetker[filtered_oetker['UF'] == uf_filtro]

        # Filtra o dataframe com base no Status de Separação selecionado
        if status_filtro != "Todas":
            filtered_oetker = filtered_oetker[filtered_oetker['Status SeparaAAo'] == status_filtro]

        # Filtra o dataframe com base no Status de Carregamento selecionado
        if status_carregamento_filtro != "Todas":
            filtered_oetker = filtered_oetker[filtered_oetker['Status Carregaento'] == status_carregamento_filtro]

        # Exibe o dataframe filtrado
        st.dataframe(filtered_oetker, use_container_width=True)

        # Cria colunas para o botão de download e o contador de registros
        col1, col2 = st.columns([3, 1])  # Define a largura relativa das colunas

        # Botão de download na primeira coluna
        with col1:
            csv = filtered_oetker.to_csv(index=False).encode('utf-8')  # Converte o dataframe para CSV
            st.download_button(
                label="📥 Baixar Dados Filtrados",
                data=csv,
                file_name='dados_filtrados.csv',
                mime='text/csv'
            )

        # Contador de registros na segunda coluna
        with col2:
            st.metric(label="Registros Filtrados", value=len(filtered_oetker))

        # Total Finalizados
        st.subheader("Resumo Operacional Separação - Dr. Oetker")
        
        # Converte a coluna 'Qtde Volumes' para float, se necessário
        filtered_oetker['Qtde Volumes'] = pd.to_numeric(filtered_oetker['Qtde Volumes'], errors='coerce')
        
        # Corrige a codificação da coluna 'Status SeparaAAo'
        if 'Status SeparaAAo' in filtered_oetker.columns:
            filtered_oetker['Status SeparaAAo'] = filtered_oetker['Status SeparaAAo'].str.encode('latin1').str.decode('utf-8')
            
            # Filtra os dados para "finalizado" e "pendente separação"
            filtered_finalizados = filtered_oetker[filtered_oetker['Status SeparaAAo'].str.lower() == 'finalizado']
            filtered_pendente = filtered_oetker[filtered_oetker['Status SeparaAAo'].str.lower() == 'pendente separação']
            coleta_finalizada = filtered_oetker[filtered_oetker['Status Carregaento'].str.lower() == 'finalizado']
            coleta_pendente = filtered_oetker[filtered_oetker['Status Carregaento'].str.lower() == 'pendente coleta']

            # Calcula os totais
            total_finalizados = filtered_finalizados['Qtde Volumes'].sum()
            total_pendente = filtered_pendente['Qtde Volumes'].sum()
            finalizada_coleta = coleta_finalizada['Qtde Volumes'].sum()
            pendente_coleta = coleta_pendente['Qtde Volumes'].sum()
            total_planejado=filtered_oetker['Qtde Volumes'].sum()
            tx_separacao= (total_finalizados / total_planejado) * 100 if total_planejado > 0 else 0
            
            # Exibe os totais formatados
            col1, col2, col3, col4, col5,col6 = st.columns(6)
            col1.button(f"Total Planejado: {total_planejado:.2f} CX", key="Total Planejado")
            col2.button(f"Sep. Finalizada: {total_finalizados:.2f} CX", key="button_finalizados")
            col3.button(f"Sep. Pendente: {total_pendente:.2f} CX", key="button_pendente")
            col4.button(f"Coleta Finalizada: {finalizada_coleta:.2f} CX", key="coleta_finalizada")
            col5.button(f"Coleta Pendente: {pendente_coleta:.2f} CX", key="coleta_Pendente")
            col6.button(f"Taxa de Separação: {tx_separacao:.2f} %", key="% Taxa de Separação")

#crie um gráfico de barras da coluna UF e a quantidade separada e inclua o rótulos de dados
            fig = px.bar(filtered_oetker, x='UF', y="Qtde Volumes", title='Quantidade Separada por UF')
            st.plotly_chart(fig, use_container_width=True)


#Crie um gráfico de pizza com a taxa de acordo com cada status de separação
            fig = px.pie(filtered_oetker, names='Status SeparaAAo', values='Qtde Volumes', title='Taxa de Separação por Status')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("A coluna 'Status SeparaAAo' não está presente no dataframe filtrado.")
        # Resumo do Carregamento por Status de Carregamento
        
        if 'Status Carregaento' in filtered_oetker.columns:
            filtered_finalizados = filtered_oetker[filtered_oetker['Status Carregaento'].str.lower() == 'finalizado']
            filtered_pendente = filtered_oetker[filtered_oetker['Status Carregaento'].str.lower() == 'pendente coleta']
            coleta_finalizada = filtered_oetker[filtered_oetker['Status Carregaento'].str.lower() == 'finalizado']
            coleta_pendente = filtered_oetker[filtered_oetker['Status Carregaento'].str.lower() == 'pendente coleta']

            # Calcula os totais
            total_finalizados = filtered_finalizados['Qtde Volumes'].sum()
            total_pendente = filtered_pendente['Qtde Volumes'].sum()
            finalizada_coleta = coleta_finalizada['Qtde Volumes'].sum()
            pendente_coleta = coleta_pendente['Qtde Volumes'].sum()
            total_planejado=filtered_oetker['Qtde Volumes'].sum()
            tx_separacao= (total_finalizados / total_planejado) * 100 if total_planejado > 0 else 0
            
            
# Exibição condicional
if st.session_state.logado:
    tela_backlog()
else:
    tela_login()

st.markdown("---")
if st.button("Sair"):
    st.session_state.logado = False
    for key in ["usuario", "senha"]:    
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()
# Rodapé com cor preta
st.markdown("""
    <style>
        .footer {
            text-align: center;
            margin-top: 20px;
            font-size: 0.9rem;
            color: white; /* Letras brancas */
            background-color: black; /* Fundo preto */
            padding: 10px; /* Espaçamento interno */
            border-radius: 8px; /* Bordas arredondadas */
        }
        .footer hr {
            border: 1px solid white; /* Linha branca */
        }
    </style>
    <div class="footer">
        <hr>
        <caption>Desenvolvido por Williams Rodrigues • © 2025</caption>
    </div>
""", unsafe_allow_html=True)