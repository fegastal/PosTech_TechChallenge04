import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import xgboost as xgb
import openpyxl
import plotly.graph_objects as go
import subprocess

# Instalar a biblioteca tabulate
subprocess.run(["pip", "install", "tabulate"])

st.set_page_config(layout= 'wide')

def formata_numero(valor, prefixo = ''):
	for unidade in ['', 'mil']:
		if valor <1000:
			return f'{prefixo} {valor:.2f} {unidade}'
		valor /= 1000
	return f'{prefixo} {valor:.2f} milhões'

st.title('ANÁLISE DE PREÇOS | PETRÓLEO BRENT')

## Visualizacao no streamlit e criacao de abas
aba1, aba2, aba3, aba4, aba5 = st.tabs(['Objetivo', 'Análises Iniciais', 'Previsão para 31/12/2024', 'Análise no BI', 'Considerações Finais'])

with aba1:
	coluna1, coluna2 = st.columns(2)
	with coluna1:
		st.write("""
		**O PROBLEMA**

		Nossa equipe da DMGB VINTAGE ANALYTICS foi contratada para analisar os dados de preço do petróleo brent, que pode ser encontrado no site do ipea. Essa base de dados histórica envolve duas colunas: data e preço (em dólares).

		Um grande cliente do segmento pediu para que a nossa consultoria desenvolvesse um dashboard interativo e que gere insights relevantes para tomada de decisão. Além disso, solicitaram que fosse desenvolvido um modelo de Machine Learning para fazer o forecasting do preço do petróleo.

		Com isso, o objetivo desse produto é:

		1. **Dashboard Interativo**
			- Criar um dashboard interativo com ferramentas à sua escolha.

		2. **Storytelling**
			- Nosso dashboard deve fazer parte de um storytelling que traga insights relevantes sobre a variação do preço do petróleo, como situações geopolíticas, crises econômicas, demanda global por energia e etc. Isso pode te ajudar com seu modelo. Trazer pelo menos 4 insights neste desafio.

		3. **Deploy em produção**
			- Criar um plano para fazer o deploy em produção do modelo, com as ferramentas que são necessárias.

		4. **MVP com Streamlit**
			- Fazer um MVP do modelo em produção utilizando o Streamlit.
		""")
	with coluna2:
		# Carregar a imagem a partir do caminho do arquivo
		caminho_imagem = 'site_ipea.png'
		imagem = st.image(caminho_imagem, caption='Imagem referente ao site do ipea, disponível em http://www.ipeadata.gov.br/ExibeSerie.aspx?module=m&serid=1650971490&oper=view', use_column_width=False, width=600)

with aba2:
	coluna1, coluna2 = st.columns(2)
	with coluna1:
				# Planilha - salvei no nosso git
		dados = pd.read_excel('base_brent.xlsx', parse_dates=['date'])

		# Definir altura máxima desejada para a tabela
		altura_maxima = 4

		# Exibir a tabela no Streamlit com barra de rolagem
		st.table(dados.style.set_table_styles([{
			'selector': 'div',
			'props': [('max-height', f'{altura_maxima}px'), ('overflow-y', 'auto')]
		}]))
	with coluna2:
		# Defina o intervalo de tempo desejado (por exemplo, de '2022-01-01' a '2022-12-31')
		data_inicio = '2014-01-16'
		data_fim = '2024-01-16'

		# Filtrar o DataFrame para o intervalo de tempo especificado
		dados_intervalo = dados[(dados['date'] >= data_inicio) & (dados['date'] <= data_fim)]

		st.write("""
		**ANÁLISES INICIAIS**

		Com base na tabela ao lado (Data e Preço) gerada em .xlsx a partir do site do ipea (http://www.ipeadata.gov.br/ExibeSerie.aspx?module=m&serid=1650971490&oper=view), podemos tirar alguns insights a partir da análise do menor preço e do maior preço em um intervalo de 10 anos (2014 à 2024), além da média do preço nesse período de tempo, a média do preço do por ano, bem como as medianas. A partir dessa análise estatística, podemos concluir sobre os resultados de acordo com o contexto político, social e econômico vivido durante estes anos.
		""")

		coluna1, coluna2 = st.columns(2)
		with coluna1:
			# Encontrar o menor preço
			menor_preco = dados_intervalo['price'].min()

			# Exibir o menor preço
			st.metric('**Menor Preço** para em 10 anos (16-01-2014 à 16-01-2024):', formata_numero(menor_preco))

			st.write("""
			1. **Pandemia de COVID-19:**
			- A pandemia de COVID-19 teve um impacto significativo na demanda global por petróleo, pois as medidas de lockdown foram implementadas em muitos países para conter a propagação do vírus. A redução na atividade econômica resultou em uma queda acentuada na demanda por combustíveis, afetando negativamente os preços do petróleo.

			2. **Disputas entre Arábia Saudita e Rússia:**
			- Em março de 2020, a Arábia Saudita e a Rússia não conseguiram chegar a um acordo sobre os cortes na produção de petróleo para estabilizar os preços. A Arábia Saudita anunciou uma estratégia de aumentar a produção e oferecer descontos significativos para ganhar participação de mercado. Essa decisão contribuiu para um excesso de oferta global em um momento em que a demanda estava caindo.

			3. **Colapso dos Preços do Petróleo:**
			- Em meados de abril de 2020, os preços do petróleo atingiram níveis historicamente baixos. O contrato futuro de petróleo dos EUA (WTI) para entrega em maio chegou a entrar em território negativo, significando que os traders estavam dispostos a pagar para se livrarem dos contratos devido à falta de capacidade de armazenamento físico.

			4. **Acordo da OPEP+:**
			- Em resposta à crise, a OPEP+ (que inclui membros da OPEP e outros países produtores de petróleo, como a Rússia) concordou em implementar cortes significativos na produção para equilibrar o mercado e estabilizar os preços.
			""")

		with coluna2:
			# Encontrar o maior preço
			maior_preco = dados_intervalo['price'].max()

			# Exibir o maior preço
			st.metric('**Maior Preço** em 10 anos (16-01-2014 à 16-01-2024):', formata_numero(maior_preco))

			st.write("""
			1. **Crise Financeira Global:**
			- O colapso do banco de investimento Lehman Brothers em setembro de 2008 desencadeou uma crise financeira global. A crise resultou em uma recessão econômica e uma redução acentuada na demanda por commodities, incluindo petróleo.

			2. **Desvalorização do Dólar:**
			- A desvalorização do dólar americano em relação a outras moedas também influenciou os preços do petróleo. Como o petróleo é negociado internacionalmente em dólares, uma queda no valor do dólar pode resultar em preços mais altos do petróleo.

			3. **Decisões da OPEP:**
			- A Organização dos Países Exportadores de Petróleo (OPEP) teve que lidar com a queda na demanda e a pressão sobre os preços. Em resposta, a OPEP implementou cortes na produção para equilibrar a oferta e a demanda.

			4. **Decisões da OPEP:**
			- Esse é o principal fator. Do lado da demanda, estamos vendo uma reativação da economia e da mobilidade após o impacto da covid-19, então após termos experimentado a maior queda registrada no ano passado na demanda por petróleo, este ano nós provavelmente registraremos o maior aumento", afirma.

			5. **Pressões inflacionárias:**
			- A rápida recuperação da demanda após a paralisação da atividade causada pela pandemia levou a uma situação econômica complexa. Os problemas na cadeia de abastecimento e o aumento dos preços das matérias-primas estão levando a uma relativa escassez de certos tipos de produtos, o que alimenta as pressões inflacionárias O aumento do preço do petróleo bruto se soma a tudo isso.
			""")

		# Calcular o preço médio
		preco_medio = dados_intervalo['price'].mean()

		# Exibir o preço médio
		st.metric('**Preço Médio** em 10 anos (16-01-2014 à 16-01-2024):', formata_numero(preco_medio))

		# Criar uma coluna 'ano' com o ano correspondente a cada data
		dados_intervalo['ano'] = dados_intervalo['date'].dt.year

		# Calcular a média do preço por ano
		media_por_ano = dados_intervalo.groupby('ano')['price'].mean().reset_index()

		# Criar o gráfico de colunas
		fig, ax = plt.subplots()
		ax.bar(media_por_ano['ano'], media_por_ano['price'], color='blue')
		ax.set_xlabel('Ano', fontsize=6)
		ax.set_ylabel('Preço', fontsize=6)
		ax.set_title('Média do Preço por Ano', fontsize=8)

		# Exibir o gráfico no Streamlit
		st.pyplot(fig)

		# Ajustar a largura usando CSS
		st.markdown(
			"""
			<style>
				.stImage {
					max-width: 100%;
					width: 100px;
					height: auto;
				}
			</style>
			""",
			unsafe_allow_html=True
		)

		# Exibir a tabela
		st.table(media_por_ano)

		st.write("""
		Analisando-se o gráfico de colunas e a tabela acima, é possível destacar alguns pontos:

		1. **Variação de Preços:**
		- Os preços do petróleo mostram uma considerável variação ao longo dos anos, refletindo as dinâmicas do mercado global de energia.

		2. **Tendências Anuais:**
		- Algumas tendências podem ser identificadas, como a queda acentuada em 2016, a recuperação nos anos subsequentes e uma oscilação notável de 2020 a 2022.

		3. **Impacto de Eventos:**
		- Mudanças significativas nos preços podem ser influenciadas por eventos econômicos, políticos e ambientais em escala global.

		4. **Ano Atual (2024):**
		- O preço médio projetado para 2024 é de $78.13, indicando uma perspectiva estável em comparação com os anos anteriores.

		5. **Contexto Econômico:**
		- O contexto econômico global e fatores geopolíticos desempenham um papel crucial na determinação dos preços do petróleo, e esses dados podem ser úteis para análises mais aprofundadas.
		""")

		# Calcular a mediana do preço
		preco_mediana = dados_intervalo['price'].median()

		# Exibir a mediana do preço
		st.metric('**Mediana do preço** em 10 anos (16-01-2014 à 16-01-2024):', formata_numero(preco_mediana))

		# Calcular a mediana do preço por ano
		mediana_por_ano = dados_intervalo.groupby('ano')['price'].median().reset_index()

		# Criar o gráfico de colunas
		fig, ax = plt.subplots()
		ax.bar(mediana_por_ano['ano'], mediana_por_ano['price'], color='blue')
		ax.set_xlabel('Ano', fontsize=6)
		ax.set_ylabel('Preço', fontsize=6)
		ax.set_title('Mediana do Preço por Ano', fontsize=8)

		# Exibir o gráfico no Streamlit
		st.pyplot(fig)

		# Ajustar a largura usando CSS
		st.markdown(
			"""
			<style>
				.stImage {
					max-width: 100%;
					width: 100px;
					height: auto;
				}
			</style>
			""",
			unsafe_allow_html=True
		)

		# Exibir a tabela
		st.table(mediana_por_ano)

		st.write("""
		Analisando-se o gráfico de colunas e a tabela acima, é possível destacar alguns pontos:

		1. **Estabilidade de Tendências:**
		- Os valores medianos são geralmente menos sensíveis a extremos do que as médias, refletindo uma medida mais estável da centralidade dos preços.

		2. **Padrões Anuais:**
		- As variações anuais apresentam semelhanças com a tabela de médias, indicando que os anos de maior ou menor mediana são consistentes com períodos de maiores ou menores preços médios.

		3. **Variação Moderada:**
		- A mediana tende a suavizar a influência de valores extremos, proporcionando uma visão mais equilibrada da distribuição dos preços.

		4. **Ano Atual (2024):**
		- A mediana para 2024 é de $78.31, ligeiramente superior à média, sugerindo uma distribuição de preços que favorece valores mais altos.
		""")

with aba3:
	coluna1, coluna2 = st.columns(2)
	with coluna1:
		st.write("""
		Nossa equipe implementou com sucesso um modelo de Machine Learning baseado no algoritmo XGBoost para prever os preços futuros de um produto específico, utilizando dados históricos como base. Este avançado modelo de regressão foi treinado e avaliado utilizando técnicas modernas de aprendizado de máquina, proporcionando uma análise preditiva robusta.

		**Resultados Obtidos:**
		1. **Mean Squared Error (MSE):** 9.88
		- O MSE é uma medida que quantifica a diferença média quadrática entre as previsões do modelo e os valores reais. Quanto menor o MSE, melhor o modelo se ajusta aos dados de teste. Neste caso, o MSE de 9.88 indica uma adequação razoável do modelo aos dados de teste.

		2. **Previsão para 31/12/2024:** 77.01
		- O modelo prevê que o preço para o dia 31/12/2024 será aproximadamente 77.01, com base nos padrões identificados nos dados históricos. Este é o resultado específico da previsão para a data escolhida.

		**Conclusão:**
		O código utiliza um modelo de regressão XGBoost para prever os preços futuros com base em padrões identificados nos dados históricos. A avaliação do modelo, indicada pelo MSE, sugere uma adequação razoável. A previsão específica para 31/12/2024 é de um preço em torno de 77.01, conforme estimado pelo modelo. Esses resultados fornecem insights valiosos para análise e tomada de decisões futuras relacionadas aos preços do produto.
		Em resumo, nossa equipe desenvolveu e implementou com sucesso um modelo preditivo utilizando técnicas avançadas de Machine Learning. Os resultados obtidos sugerem uma capacidade promissora de prever os preços futuros, o que pode ser instrumental para análises e tomadas de decisões futuras relacionadas ao produto em questão. Estes insights contribuem significativamente para estratégias de negócios informadas e embasadas em dados, fortalecendo a eficácia das operações da nossa equipe.
	""")

	with coluna2:
		### A PARTIR DAQUI É O TECH CHALLENGE
		# Planilha - salvei no nosso git
		dados = pd.read_excel('base_brent.xlsx', parse_dates=['date'])

		# Nem precisava, pq está correto, mas fiz por boa prática
		dados.sort_values(by='date', inplace=True)

		# Nem precisava, pq está correto, mas fiz por boa prática
		dados['ano'] = dados['date'].dt.year
		dados['mes'] = dados['date'].dt.month
		dados['dia_da_semana'] = dados['date'].dt.dayofweek

		# Dividir os dados em conjuntos de treinamento e teste
		X = dados[['ano', 'mes', 'dia_da_semana']]
		# Utilizar 'price' como o nome da coluna de destino
		y = dados['price']

		# Escolhi último dia da amostrar como data de corte para treinamento/teste
		data_corte = pd.to_datetime('2024-01-16')  # Substitua pela data desejada

		# Dividir os dados em treinamento e teste
		X_train = X[dados['date'] < data_corte]
		y_train = y[dados['date'] < data_corte]
		X_test = X[dados['date'] >= data_corte]
		y_test = y[dados['date'] >= data_corte]

		# modelo XGBoost com ajustes nos parâmetros - mesmo que usamos no passado
		modelo = xgb.XGBRegressor(
			objective='reg:squarederror',
			n_estimators=300,  # número de estimadores
			learning_rate=0.05,  # Ajuste a taxa de aprendizado
			max_depth=6,  # Ajuste a profundidade máxima da árvore
		)
		modelo.fit(X_train, y_train)

		# Preços para 31 de dezembro de 2024
		data_dez_2024 = pd.DataFrame({'ano': [2024], 'mes': [12], 'dia_da_semana': [3]})  # Assumindo quinta-feira (dia 3) para 31 de dezembro
		previsao_dez_2024 = modelo.predict(data_dez_2024)

		# Exibir o preço histórico dos últimos 10 anos (usei um tempo que acho suficiente)
		historico_10_anos = dados[dados['date'] >= (dados['date'].max() - pd.DateOffset(years=10))]

		# Criar um gráfico de linha com o histórico
		fig = px.line(historico_10_anos, x='date', y='price', labels={'price': 'Histórico dos últimos 10 anos'})

		# Adicionar um ponto vermelho para a previsão em 31/12/2024
		fig.add_trace(
			go.Scatter(
				x=[pd.to_datetime('2024-12-31')],
				y=[previsao_dez_2024],
				mode='markers',
				marker=dict(color='red', size=10),
				name='Previsão para 31/12/2024'
			)
		)

		# Atualizar os rótulos dos eixos
		fig.update_layout(xaxis_title='Data', yaxis_title='Preço')

		# Exibir o gráfico no Streamlit
		st.plotly_chart(fig)

		# Carregar a imagem a partir do caminho do arquivo
		caminho_imagem = 'imagem_grafico.png'
		imagem = st.image(caminho_imagem, caption='Outra versão do gráfico acima com a previsão para 31/12/2024. Desenvolvido em https://github.com/fegastal/PosTech-DataAnalytics_TechChallenge/blob/main/Modulo04v01.ipynb', use_column_width=False, width=600)

		# Exibir valor exato da previsão
		#st.write(f'Previsão para 31/12/2024: {previsao_dez_2024[0]}')
		st.metric('Previsão para 31/12/2024', formata_numero(previsao_dez_2024[0]))

		# Avaliar o desempenho do modelo
		mse = mean_squared_error(y_test, previsao_dez_2024)
		#print(f'Mean Squared Error: {mse}')
		#st.write(f'Mean Squared Error: {mse}')
		st.metric('Mean Squared Error', formata_numero(mse))

		# Alternativamente, você pode exibir uma imagem diretamente a partir de uma URL
		# url_imagem = 'https://exemplo.com/imagem.jpg'
		# imagem = st.image(url_imagem, caption='Legenda Opcional', use_column_width=True)

with aba4:
	st.write("Nossa equipe da DMGB VINTAGE ANALYTICS também desenvolveu diversas análises utilizando a ferramenta BI. Você pode conferir o arquivo .pbix em https://github.com/fegastal/PosTech_TechChallenge04")

	# Carregar a imagem a partir do caminho do arquivo
	caminho_imagem = 'analise_bi.jpeg'
	imagem = st.image(caminho_imagem, caption='Análise da tabela no BI. É possível baixar o arquivo .pbix em https://github.com/fegastal/PosTech_TechChallenge04', use_column_width=True, width=1000)

with aba5:
    st.write("""
		Ao longo dessa interação, nossa equipe demonstrou uma abordagem abrangente e eficiente para análise de dados e desenvolvimento de modelos preditivos, destacando a capacidade de extrair insights valiosos a partir de conjuntos complexos de informações. Aqui estão algumas considerações finais sobre o trabalho realizado:

		1. **Exploração e Processamento de Dados:**
		- Utilizamos a linguagem Python e diversas bibliotecas, incluindo Pandas, Matplotlib e Streamlit, para manipular e visualizar dados.
		- Realizamos análises estatísticas e exploratórias, compreendendo o comportamento dos preços ao longo do tempo.

		2. **Modelagem Preditiva com XGBoost:**
		- Implementamos um modelo de Machine Learning robusto, baseado no algoritmo XGBoost, para prever os preços futuros do produto.
		- Ajustamos parâmetros e treinamos o modelo, assegurando uma adequada generalização aos dados de teste.

		3. **Avaliação do Modelo e Resultados:**
		- Utilizamos métricas como Mean Squared Error (MSE) para avaliar a performance do modelo.
		- Os resultados indicaram uma adaptação satisfatória aos dados históricos, com um MSE de 9.88.

		4. **Visualização e Comunicação de Resultados:**
		- Implementamos visualizações gráficas interativas usando a biblioteca Streamlit.
		- Comunicamos efetivamente os resultados, incluindo a previsão específica para 31/12/2024.

		5. **Recomendações e Próximos Passos:**
		- Recomendamos a integração contínua de dados atualizados para manter a relevância do modelo.
		- Futuros trabalhos podem explorar a expansão do modelo para incluir mais variáveis preditoras, refinando ainda mais as previsões.

		Essa jornada reflete nosso compromisso com a excelência na análise de dados e na aplicação de técnicas de Machine Learning para impulsionar decisões informadas. Estamos confiantes de que os resultados obtidos servirão como uma base sólida para estratégias futuras, fornecendo uma vantagem competitiva por meio de insights precisos e orientados por dados.
		""")