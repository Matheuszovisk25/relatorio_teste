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
        

def pag2():
    st.title("Equipamentos")

    tab1, tab2 = st.tabs(["Equipamentos em Uso", "Equipamentos em estoque"])

    with tab1:
        with st.expander("📍 Restaurante"):
            st.image("images/antena_roteador_restaurante.jpeg", caption="Access Point Ubiquiti AC Mesh instalado no restaurante", width=300)
            st.markdown("""
            - Modelo: **Ubiquiti Unifi AC Mesh UAP-AC-M-BR**  
            - Frequência Dual Band: **2.4GHz / 5GHz**  
            - Padrão Wi-Fi: **802.11ac (Wi-Fi 5)**  
            - Porta Ethernet: **Gigabit (10/100/1000 Mbps)**  
            - Instalação com **antenas externas destacáveis**  
            - Alimentação via **PoE 24V**  
            - Equipamento atualmente em uso, porém:  
                - Apresenta **desgaste físico visível**    
                - Cobertura e desempenho **limitados em horários de pico**  
                - Sem controle de acesso avançado, dificultando gerenciamento. (Controlador Unifi)

            ⚠️ *Apesar de ainda funcional, o equipamento apresenta sinais de obsolescência e já não atende plenamente aos padrões atuais de conectividade exigidos por hóspedes e operação interna.*
        
            """)

            st.text("") 
            
            st.image("images/ubitique_u7_outdoor.jpeg", caption="Access Point Ubiquiti UniFi U7 Pro Outdoor instalado na fachada", width=300)
            st.markdown("""
            - Modelo: **Ubiquiti UniFi U7 Pro Outdoor**  
            - Frequência Tri-Band: **2.4GHz / 5GHz / 6GHz (Wi-Fi 7)**  
            - Padrão Wi-Fi: **802.11be (Wi-Fi 7)**  
            - Velocidade de até **9.3 Gbps agregados**  
            - Portas Ethernet: **1x 2.5GbE (com PoE++)**  
            - Ideal para ambientes **outdoor com alta densidade de usuários**  
            - Suporte nativo a **UniFi Network Controller**  

            ✅ *Excelente desempenho mesmo em áreas abertas com múltiplos usuários conectados simultaneamente, mantendo estabilidade e alta velocidade.*
    
            """)
            st.text("")
            
            st.image("images/switch_tp_link.jpeg", caption="Switch TP-Link TL-SG1005P com 4 portas PoE+", width=300)
            st.markdown("""
            - Modelo: **TP-Link TL-SG1005P**  
            - Tipo: **Switch Gigabit não gerenciável (Desktop)**  
            - Total de portas: **5 portas RJ45 (10/100/1000 Mbps)**  
            - Portas PoE: **4 portas PoE+ (IEEE 802.3af/at)**  
            - Potência PoE total: **até 65W**  
            - Plug and Play: **Sem necessidade de configuração**  
            - Utilizado para alimentar Access Points e câmeras IP  
            - Equipamento em **perfeito estado de funcionamento**

            ✅ *Responsável por fornecer conectividade para até 4 equipamentos: 2 antenas UniFi U7, 1 impressora fiscal e 1 módulo SAT, atendendo bem às necessidades atuais da pousada.*
                        
            ⚠️ *Não possui integração com o UniFi Controller, o que limita o gerenciamento centralizado dos access points conectados.*
            """)

            st.text("")
            st.image("images/g250w_gertec.jpeg", caption="Impressora térmica Gertec G250W instalada na cozinha", width=300)
            st.markdown("""
            - Modelo: **Gertec G250W**  
            - Tipo: **Impressora térmica de pedidos**  
            - Interface: **USB + Wi-Fi (802.11b/g/n)**  
            - Largura do papel: **80 mm**  
            - Velocidade de impressão: **até 250 mm/s**  
            - Ideal para **ambientes de cozinha e atendimento rápido**  
            - Compatível com **comandas, pedidos e integração com sistemas PDV**  
            - Instalada estrategicamente próxima ao fogão para agilidade operacional

            ✅ *Atende bem ao fluxo da cozinha, com impressão rápida e conectividade sem fio, evitando cabos em excesso no ambiente de preparo.*
            
            ⚠️ *Devido à proximidade com fontes de calor e gordura, recomenda-se limpeza periódica para garantir durabilidade e evitar falhas.*
            """)

            st.text("")

            st.image("images/tanca_tp650.jpeg", caption="Impressora térmica Tanca TP-650 instalada no bar", width=300)
            st.markdown("""
            - Modelo: **Tanca TP-650**  
            - Tipo: **Impressora térmica de recibos e comandas**  
            - Interface: **USB / Serial / Ethernet (dependendo da versão)**  
            - Largura do papel: **80 mm**  
            - Velocidade de impressão: **até 250 mm/s**  
            - Indicada para **ambientes de atendimento com alto volume de impressão**  
            - Utilizada para impressão de pedidos no bar, conectada diretamente ao sistema PDV  
            - Instalada em nicho de madeira para melhor organização do espaço

            ✅ *Equipamento robusto, com boa performance mesmo em horários de pico, essencial para agilidade no atendimento do bar.*

            ⚠️ *Devido à exposição contínua à umidade e poeira, recomenda-se higienização frequente e verificação do estado da guilhotina térmica.*
            """)

            st.text("")

            st.image("images/u6 _long_1.jpeg", caption="Access Point UniFi 6 Long Range instalado na área interna (estrutura de madeira)", width=300)
            st.image("images/u6_long_2.jpeg", caption="Access Point UniFi 6 Long Range instalado na área interna (cobertura metálica)", width=300)
            st.markdown("""
            - Modelo: **Ubiquiti UniFi 6 Long Range (U6-LR)**  
            - Frequência Dual Band: **2.4GHz / 5GHz**  
            - Padrão Wi-Fi: **802.11ax (Wi-Fi 6)**  
            - Portas Ethernet: **1x Gigabit com suporte PoE**  
            - Alimentação: **PoE 802.3af/at (via switch TP-Link)**  
            - Alcance estendido para **ambientes internos de maior profundidade**  
            - Instalações posicionadas estrategicamente para cobrir o salão, cozinha e região do bar

            ✅ *Mantém sinal forte e estável em áreas amplas, mesmo em momentos de alta demanda.*
            """)
            st.text("")

            st.image("images/fonte_48v.jpeg", caption="Fontes PoE de 48V utilizadas para alimentação das antenas UniFi U6", width=300)
            st.markdown("""
            - Equipamento: **Fontes PoE 48V - Ubiquiti**  
            - Quantidade: **2 unidades**  
            - Padrão PoE: **802.3af/at compatível**  
            - Tensão de saída: **48V DC**  
            - Potência suficiente para alimentar **Access Points UniFi 6 Long Range (U6-LR)**  
            - Instalação fixa sob superfície de madeira, com boa organização dos cabos

            ✅ *Alternativa prática e econômica ao uso de switch PoE dedicado, mantendo estabilidade na alimentação das antenas.*
            
            """)

            st.image("images/conversor.jpeg", caption="Conversor de mídia CFO-NK1000 para fibra óptica instalado sob bancada", width=300)
            st.markdown("""
            - Equipamento: **Conversor de Mídia Ethernet para Fibra Óptica**  
            - Modelo: **CFO-NK1000**  
            - Interfaces:  
                - **1x Porta RJ45 10/100/1000 Mbps (Ethernet)**  
                - **1x Porta SC/UPC para fibra monomodo (TX/RX)**  
            - Compatibilidade: **IEEE 802.3u/ab (Fast e Gigabit Ethernet)**  
            - Distância suportada: **até 20 km via fibra monomodo (dependendo do módulo)**  
            - Alimentação: **Fonte externa 5V DC**

            ✅ *Responsável por integrar a conexão de fibra óptica à rede cabeada da pousada, garantindo alta velocidade e baixa latência.*

            """)
            st.text("")

            st.image("images/pc_2.jpeg", caption="Notebook secundario do restaurante com sistema Desbravador em execução", width=300)
            st.image("images/pc2_config.jpeg", caption="Configurações técnicas do notebook (DxDiag - Windows 11)", width=300)
            st.markdown("""
            - Equipamento: **Notebook ASUS VivoBook X515EA**  
            - Nome do dispositivo: **KLM-PIZZA**  
            - Sistema operacional: **Windows 11 Home Single Language 64 bits**  
            - Processador: **Intel Core i3-1115G4 (11ª Geração) @ 3.00GHz**  
            - Memória RAM: **4 GB**  
            - Armazenamento: **HDD/SATA com partição ativa e uso elevado de paginação**  
            - Tela: **15,6” com teclado numérico lateral**  
            - Utilização: **Execução do sistema Desbravador para controle de mesas, comandas e pedidos**  
            - Local: **Balcão principal do bar**

            ✅ *Executa o sistema PDV de forma funcional e atende à operação básica diária do restaurante.*

            ⚠️ *Memória RAM limitada para multitarefas. Recomendado upgrade para 8 GB para maior fluidez e estabilidade, especialmente em horários de pico.*
            """)
            st.text("")

            st.image("images/pc_principal_bar.jpeg", caption="Notebook HP utilizado no bar com sistema Desbravador", width=300)
            st.image("images/config_pc_principal.jpeg", caption="Configurações técnicas do notebook (DxDiag - Windows 11)", width=300)
            st.markdown("""
            - Equipamento: **Notebook HP 240 G8**  
            - Nome do dispositivo: **KLM-RESTO1**  
            - Sistema operacional: **Windows 11 Home Single Language 64 bits**  
            - Processador: **Intel Core i3-1125G4 (11ª Geração) @ 2.00GHz**  
            - Memória RAM: **8 GB**  
            - Utilização: **Sistema Desbravador para gestão de comandas e controle de mesas do bar**  
            - Local: **Balcão do bar, com integração à impressora térmica Tanca TP-650**

            ✅ *Máquina com desempenho sólido para operação contínua do sistema PDV e multitarefa moderada.*

            """)

    with st.expander("📍 Sushi Bar / Pizzaria"):
        st.image("images/tanca_tpg650_sushi.jpeg", caption="Impressora térmica Tanca TPG-650 instalada no Sushi Bar / Pizzaria", width=300)
        st.markdown("""
        - Modelo: **Tanca TPG-650**  
        - Tipo: **Impressora térmica para comandas**  
        - Interface: **USB / Serial / Ethernet (conforme versão)**  
        - Largura do papel: **80 mm**  
        - Velocidade de impressão: **até 250 mm/s**  
        - Aplicação: **Impressão de pedidos enviados pelo sistema PDV Desbravador**  
        - Local: **Balcão do Sushi Bar / Pizzaria**

        ✅ Equipamento robusto, com boa performance mesmo em horários de pico, essencial para agilidade no atendimento do bar.
                    
        """)

        st.text("")


        st.image("images/computador_sushi_bar.jpeg", caption="Notebook Acer utilizado no Sushi Bar / Pizzaria com sistema Desbravador", width=300)
        st.image("images/configuracoes_pc_sushibar.jpeg", caption="Configurações do notebook (DxDiag - Windows 11)", width=300)
        st.markdown("""
        - Equipamento: **Notebook Acer Aspire A315-510P**  
        - Nome do dispositivo: **KLM-REST02**  
        - Sistema operacional: **Windows 11 Home Single Language 64 bits**  
        - Processador: **Intel Core i3-N305 (8 núcleos) @ 1.8GHz**  
        - Memória RAM: **8 GB**  
        - Utilização: **Sistema Desbravador para envio de pedidos ao setor de cozinha e controle de mesas**  
        - Local: **Balcão de atendimento do Sushi Bar / Pizzaria**

        ✅ *Máquina atualizada, com bom desempenho para uso contínuo em atendimento, mesmo em picos de movimento.*

        """)

        st.text("")


        st.image("images/conversor_pizza_sushi.jpeg", caption="Conversor de mídia Exbom CFO-NK1000 instalado no Sushi Bar / Pizzaria", width=300)
        st.markdown("""
        - Equipamento: **Conversor de Mídia Ethernet para Fibra Óptica**  
        - Modelo: **Exbom CFO-NK1000**  
        - Interfaces:  
            - **1x Porta RJ45 10/100/1000 Mbps (Ethernet)**  
            - **1x Porta SC/UPC para fibra monomodo (TX/RX)**  
        - Protocolo: **IEEE 802.3u/ab**  
        - Distância suportada: **até 20 km via fibra monomodo**  
        - Local: **Fixado em parede no setor do Sushi Bar / Pizzaria**

        ✅ *Permite a extensão da rede principal até a pizzaria via fibra óptica, com performance confiável.*

        """)

        st.text("")

        st.image("images/roteador_intelbras_pizzasushi.jpeg", caption="Roteador Intelbras instalado no setor Sushi Bar / Pizzaria", width=300)
        st.markdown("""
        - Equipamento: **Roteador sem fio Intelbras**  
        - Frequência: **Provavelmente Dual Band (2.4GHz / 5GHz)**  
        - Antenas: **4 antenas externas fixas**  
        - Aplicação: **Distribuição local de Wi-Fi para dispositivos internos**  
        - Alimentação: **Fonte padrão 12V**  
        - Conectado via cabo ao **conversor de fibra óptica** local  
        - Local: **Instalado em altura elevada sobre viga metálica**

        ✅ *Fornece conectividade local para PDVs, impressoras e eventuais dispositivos móveis no ambiente do Sushi Bar.*

        ⚠️ *Não gerenciado centralmente via controladora. Recomendado upgrade para Access Point Unifi caso deseje padronização e gerenciamento integrado da rede.*
        """)

        st.image("images/tanca_tp650_pizzaria.jpeg", caption="Impressora térmica Tanca TP-650 utilizada na área de preparo da pizzaria", width=300)
        st.markdown("""
        - Modelo: **Tanca TP-650**  
        - Tipo: **Impressora térmica para comandas de cozinha**  
        - Interface: **USB / Serial / Ethernet (dependendo da configuração)**  
        - Largura do papel: **80 mm**  
        - Velocidade de impressão: **até 250 mm/s**  
        - Local: **Balcão de preparo da pizzaria**

        ✅ *Equipamento essencial para recebimento ágil de pedidos do sistema PDV Desbravador, otimizando o tempo de preparo.*

        ⚠️ *Apresenta sinais visíveis de acúmulo de gordura e poeira. Recomendado processo de higienização periódica para evitar travamentos e falhas de impressão.*
        """)

st.sidebar.title("📌 Menu")
pagina = st.sidebar.radio("Navegue entre as seções:", ["Análise de Rede", "Equipamentos"])

if pagina == "Análise de Rede":
    pag1()
elif pagina == "Equipamentos":
    pag2()
