import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go


def dataframe(data):
    df = pd.read_excel(data)
    df['hora'] = pd.to_datetime(df['hora'], format='%H:%M:%S')
    return df

def pag1():
    st.title("Comparando as redes Antiga/Nova")

    st.write("A infraestrutura de rede da pousada apresentava diversos problemas que impactavam diretamente na experiência dos hóspedes e na operação interna. Entre os principais desafios estavam a baixa velocidade de conexão, instabilidade frequente, cobertura de sinal limitada e uma estrutura defasada, sem gerenciamento eficiente ou segurança adequada.")
    st.write("Com a chegada da nossa empresa, foi iniciado um processo de modernização completo da rede. Implementamos uma nova infraestrutura de internet, com equipamentos de alto desempenho, distribuição de sinal Wi-Fi otimizada para todas as áreas da pousada. O objetivo foi garantir uma conexão estável, rápida e segura, atendendo tanto às demandas operacionais quanto à expectativa dos hóspedes por uma internet de qualidade.")

    st.title("Metodologia")
    st.write("Foram conduzidos testes de velocidade, registrando a taxa de download em Mbps. Os dados foram coletados por um Script e analisados para identificar oscilações na conexão e eventuais gargalos que impactavam a experiência dos usuários.")

    codigo = '''
import speedtest
import pandas as pd
import time
from datetime import datetime

arquivo_excel = "testes_velocidade4.xlsx"
resultados = []

st = speedtest.Speedtest()
st.get_best_server()

print("Iniciando os testes de velocidade...")

def testar_velocidade():
    download = st.download() / 1_000_000  
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Teste realizado: {timestamp} - Download: {download:.2f} Mbps")
    return {"Timestamp": timestamp, "Download (Mbps)": download}

for i in range(20):
    resultados.append(testar_velocidade())
    time.sleep(1)  

df = pd.DataFrame(resultados)
df.to_excel(arquivo_excel, index=False)

print(f"Testes concluídos! Resultados salvos em '{arquivo_excel}'.")
'''

    with st.expander("🔍 Ver código do teste de velocidade"):
        st.code(codigo, language='python')

    st.title("Velocidade Recomendada de Internet por Tipo de Uso")

    st.markdown("""
Este quadro apresenta estimativas de velocidades ideais de internet (em Mbps) para diferentes tipos de uso. """) 

    dados = {
    "Uso": [
        "Navegação profissional e demandas diárias",
        "Transmissão de vídeo em HD",
        "Transmissão de vídeo em 4K",
        "Streaming de música",
        "Videochamadas individuais"
    ],
    "Velocidade Recomendada (Mbps)": [
        "15 - 25",
        "25",
        "100",
        "5",
        "25"
    ],
    "Observações": [
        "Inclui navegação, e-mails, documentos e sistemas online",
        "Netflix, YouTube e outros em qualidade HD",
        "Para streaming de altíssima qualidade sem travar",
        "Spotify, Deezer ou similares",
        "Zoom, Meet ou Teams com boa estabilidade de vídeo"
    ]
}
    with st.expander("Tabela de velocidades ideais"):
        ideal = pd.DataFrame(dados)

        st.dataframe(ideal)

    tab1, tab2 = st.tabs(["Rede antiga", "Rede nova"])

    with tab1:
        st.title("Rede antiga")
        st.write("Este relatório apresenta a análise do desempenho da internet utilizada anteriormente na pousada, com base em testes realizados para avaliar a estabilidade e a qualidade da conexão antes das melhorias implementadas na infraestrutura de rede.")

        df_antigo = dataframe("testes_velocidade4.xlsx")
        media = df_antigo["Download (Mbps)"].mean()

        fig = px.line(
            df_antigo,
            x='hora',
            y='Download (Mbps)',
            title='Variação da Velocidade de Download - Rede Antiga',
            markers=True,
            labels={'hora': 'Horário', 'Download (Mbps)': 'Velocidade (Mbps)'},
        )

        fig.add_hline(
            y=media,
            line_dash="dash",
            line_color="red",
        )

        fig.update_layout(
            xaxis_tickformat='%H:%M:%S', 
            xaxis_title='Horário',
            yaxis_title='Velocidade (Mbps)',
        )

        st.plotly_chart(fig, use_container_width=True)
        st.metric(label="📊 Média de Download (Rede Antiga)", value=f"{media:.2f} Mbps")

        st.subheader("Análise Técnica – Rede Anterior")

        st.markdown("""
        A estrutura de rede anteriormente utilizada na pousada apresentava sérias limitações técnicas que comprometiam tanto a operação interna quanto a experiência dos hóspedes. A seguir, destacam-se os principais pontos críticos identificados durante os testes de desempenho:
        """)

        st.markdown("#### Principais Problemas Detectados")

        st.markdown("""
        - **Baixa velocidade de conexão**  
        Em diversos momentos, a taxa de download ficou abaixo de níveis considerados aceitáveis para um ambiente de hospedagem, dificultando tarefas básicas como chamadas de vídeo, streaming ou acesso a plataformas corporativas.

        - **Oscilações constantes na conexão**  
        Os testes realizados evidenciaram uma variação significativa na velocidade de download ao longo do tempo, indicando instabilidade e ausência de controle de qualidade no fornecimento da banda.

        - **Cobertura Wi-Fi insuficiente**  
        O alcance do sinal era limitado, com áreas na pousada apresentando sinal fraco ou ausência total de conectividade.

        - **Equipamentos obsoletos e sem gerenciamento**  
        A infraestrutura era composta por dispositivos antigos, sem suporte a tecnologias modernas como Wi-Fi 5/6, e não havia nenhum tipo de controle centralizado, dificultando o monitoramento e a manutenção da rede.
        """)

        st.markdown("""
        Esse diagnóstico reforça a necessidade e urgência da modernização da infraestrutura, visando garantir estabilidade, desempenho e segurança compatíveis com os padrões atuais de conectividade.
        """)
    with tab2:
        st.title("Nova rede")  
        st.markdown("""Este relatório apresenta a análise do desempenho da nova infraestrutura de internet instalada na pousada, com base em testes realizados após a modernização de alguns pontos da rede.
                     O objetivo é avaliar os ganhos obtidos em termos de estabilidade, cobertura e velocidade de conexão, comparando com os resultados da rede anterior.""")  
        df_novo = dataframe("testes_velocidade2.xlsx")
        media_novo = df_novo['Download (Mbps)'].mean()

        fig = px.line(
            df_novo,
            x='hora',
            y='Download (Mbps)',
            title='Variação da Velocidade de Download - Rede Nova',
            markers=True,
            labels={'hora': 'Horário', 'Download (Mbps)': 'Velocidade (Mbps)'},
        )

        fig.add_hline(
            y=media_novo,
            line_dash="dash",
            line_color="red",
        )

        fig.update_layout(
            xaxis_tickformat='%H:%M:%S', 
            xaxis_title='Horário',
            yaxis_title='Velocidade (Mbps)',
        )

        st.plotly_chart(fig, use_container_width=True)
        st.metric(label="📊 Média de Download (Rede Nova)", value=f"{media_novo:.2f} Mbps")

        st.subheader("Análise Técnica – Nova Infraestrutura de Rede")

        st.markdown("""
A nova infraestrutura de rede foi implementada com o objetivo de solucionar os diversos problemas técnicos identificados anteriormente e elevar o padrão de conectividade da pousada. Após a modernização, foram realizados novos testes para validar os avanços obtidos em desempenho, estabilidade e cobertura.

#### Melhorias Observadas

- **Aumento significativo na velocidade de conexão**  
A nova infraestrutura permite taxas de download muito superiores às da rede anterior, garantindo uma navegação rápida e fluida, mesmo em horários de pico ou com múltiplos dispositivos conectados simultaneamente.

- **Melhoria na estabilidade e desempenho geral**  
Embora pequenas oscilações ainda possam ser observadas, a nova rede opera em um patamar significativamente superior ao anterior. Os testes mostram que a velocidade de download se mantém consistentemente acima de 100 Mbps, mesmo nos momentos de maior uso. Isso representa um avanço importante em confiabilidade para aplicações críticas, como sistemas internos, chamadas de vídeo e plataformas de gestão.

Esse novo cenário garante uma conectividade robusta, estável e segura, compatível com os padrões de exigência atuais e com a expectativa dos hóspedes por uma internet de qualidade.
""")

pg = st.navigation([pag1])
pg.run()