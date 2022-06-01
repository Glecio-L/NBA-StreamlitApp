# Import Libraries 
import streamlit as st
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns



st.set_page_config(layout='wide') 

## Definindo funções 

# WebScraping das estatísticas dos jogadores da nba
@st.cache(allow_output_mutation=True)  # Utilizando cache para otimizar a experiência do usuário
def get_data(ano):
    url = "https://www.basketball-reference.com/leagues/NBA_" + str(ano) + "_per_game.html"
    html = pd.read_html(url, header = 0)
    data = html[0]
    raw = data.drop(data[data.Age == 'Age'].index) #Deleta os cabeçalhos repetidos
    raw = raw.fillna(0)
    playerstats = raw.drop(['Rk'], axis = 1) #Elimina o RK, coluna id de jogador
    return playerstats


def get_unique_teams(df_data):
    playerswithoutTOT = df_data.drop(df_data.loc[df_data['Tm'] == 'TOT'].index)
    unique_teams = np.unique(playerswithoutTOT.Tm).tolist()
    return unique_teams


def filter_teams(df_data):
    df_filtered_team = pd.DataFrame()
    if all_teams_selected == 'Selecionar as franquias manualmente':
        df_filtered_team = df_data[df_data['Tm'].isin(selected_teams)]
        return df_filtered_team
    return df_data


def plot_age_team(df_data):
    sns.set(rc = {'figure.figsize':(10,4),
          'axes.facecolor':'#0e1117',
          'axes.edgecolor': '#0e1117',
          'axes.labelcolor': 'white',
          'figure.facecolor': '#0e1117',
          'patch.edgecolor': '#0e1117',
          'text.color': 'white',
          'xtick.color': 'white',
          'ytick.color': 'white',
          'grid.color': 'grey',
          'font.size' : 6,
          'axes.labelsize': 7,
          'xtick.labelsize': 6,
          'ytick.labelsize': 7})
    
    fig, ax = plt.subplots()
    ax = sns.barplot(y='team', x='Age', data=df_data ,palette="flare")
    ax.set(xlim=(20, 30), ylabel="",
       xlabel="Média de idade")
    st.pyplot(fig)

## SIDEBAR 

st.sidebar.header('Entrada de variáveis do usuário')

# Seleção do ano
selected_year = st.sidebar.selectbox('Ano', list(reversed(range(1950,2023))))

# Checkbox da Tabela
st.sidebar.subheader("Tabela")
tabela = st.sidebar.empty()    # placeholder que só vai ser carregado com o playerstats2

# Read data
playerstats = get_data(selected_year)
playerstats2 = playerstats.astype(str)


# Transform data
playerstats2['PTS'] = playerstats2['PTS'].astype('float')
playerstats2['AST'] = playerstats2['AST'].astype('float')
playerstats2['Age'] = playerstats2['Age'].astype('int')

## Filtros
# Seleção de franquia
# Sidebar - Team selection
unique_teams = get_unique_teams(playerstats2)
all_teams_selected = st.sidebar.selectbox('', ['Incluir todas as franquias disponíveis', 'Selecionar as franquias manualmente'])

if all_teams_selected == 'Selecionar as franquias manualmente':
    selected_teams = st.sidebar.multiselect('', unique_teams, default = unique_teams)

df_filtered_per_team = filter_teams(playerstats2)
df_filtered_per_team = df_filtered_per_team.drop(df_filtered_per_team.loc[df_filtered_per_team['Tm'] == 'TOT'].index)

################
##### MAIN #####
################
row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3 = st.columns((.1, 2.3, .1, 1.3, .1))
with row0_1:
    st.title('🏀 NBA Stats')
with row0_2:
    st.text("")
    st.subheader('Streamlit App by [Glecio Lucas](https://www.linkedin.com/in/glecio-lucas-7184ba18a/), [Higor Jose](https://www.linkedin.com/in/higorjos-melo/)')
row3_spacer1, row3_1, row3_spacer2 = st.columns((.1, 3.2, .1))
with row3_1:
    st.markdown('Olá todo mundo, esse App tem o objetivo de mostrar as estatísticas dos jogadores da maior liga de basquete do mundo  - NBA.')
    st.markdown('**Data source:** [Basketball-reference.com](https://www.basketball-reference.com/).')


st.subheader('Resumo dos dados por ano:')
col1, col2, col3, col4 = st.columns((.2, .2, .4, .4))

with col1:
    t = " Franquias"
    teams = len(np.unique(df_filtered_per_team.Tm).tolist())
    str_teams = "🏆" + str(teams) + t
    st.markdown(str_teams)

with col2:
    unique_player = len(np.unique(df_filtered_per_team.Player).tolist())
    str_player = "⛹" + str(unique_player) + " Jogadores"
    st.markdown(str_player)

with col3:
    top_scorer = str(''.join(df_filtered_per_team.Player[df_filtered_per_team['PTS'] == df_filtered_per_team['PTS'].max()]))
    str_scorer = "Mais pontos por partida: " + top_scorer
    st.markdown(str_scorer)

with col4:
    top_assist = str(''.join(df_filtered_per_team.Player[df_filtered_per_team['AST'] == df_filtered_per_team['AST'].max()]))
    str_assist = "Mais assistências por partida: " + top_assist
    st.markdown(str_assist)


# raw data (tabela) dependente do checkbox
if tabela.checkbox("Mostrar tabela de dados"):
    st.write(df_filtered_per_team)


## Visualizações 

## Análise da média de idade por time 

Age_team = playerstats2.groupby('Tm')[['Age']].mean().rename_axis('team').reset_index().sort_values("Age", ascending=False)

## Criando visualização

c1, c2 = st.columns((1, 1))

c1.subheader('Média de Idade por Franquia')

plot_age_team(Age_team)


## jogador vs jogador

df_filtered_per_team['PTS'] = df_filtered_per_team['PTS'].astype('string')
df_filtered_per_team['AST'] = df_filtered_per_team['AST'].astype('string')

row12_spacer1, row12_1, row12_spacer2 = st.columns((.2, 7.1, .2))

with row12_1:
    st.subheader('Player Comparison')
    
row13_spacer1, row13_1, row13_spacer2, row13_2, row13_spacer3, row13_3, row13_spacer4   = st.columns((.4, 2.1, .4, .4, .4, 2.1, .4))
with row13_1:
    
    player1 = st.selectbox('', np.unique(df_filtered_per_team.Player).tolist(), key = 'play1')
    stats1 = df_filtered_per_team.loc[df_filtered_per_team['Player'] == player1]
    
with row13_2:
    st.markdown(" ")
    st.markdown(" ")
    st.markdown(" ")
    s = '❌'
    st.markdown(s)
    
with row13_3:
    
    player2 = st.selectbox('', np.unique(df_filtered_per_team.Player).tolist(), key = 'play2')
    stats2 = df_filtered_per_team.loc[df_filtered_per_team['Player'] == player2]


row16_spacer1, row16_1, row16_2, row16_3, row16_4, row16_spacer2  = st.columns((.2, 1.5, 1.5, 1, 2, 0.5))
with row16_1:
    st.markdown("🗑 Points Per Game:")
    st.markdown("🎩 Assists Per Game:")
    st.markdown("🔙 Rebounds Per Game:")
    st.markdown("🔁 Steals Per Game:")
    st.markdown("😴 Turnovers Per Game:")
    st.markdown("🎯 3P%:")
    st.markdown("⚠ Personal Fouls:")
with row16_2:
    st.markdown(" "+str(''.join(stats1.PTS)))
    st.markdown(" "+str(''.join(stats1.AST)))
    st.markdown(" "+str(''.join(stats1.AST)))
    st.markdown(" "+str(''.join(stats1.STL)))
    st.markdown(" "+str(''.join(stats1.TOV)))
    st.markdown(" "+str(''.join(stats1['3P%'])))
    st.markdown(" "+str(''.join(stats1.PF)))
with row16_4:
    st.markdown(" "+str(''.join(stats2.PTS)))
    st.markdown(" "+str(''.join(stats2.AST)))
    st.markdown(" "+str(''.join(stats2.TRB)))
    st.markdown(" "+str(''.join(stats2.STL)))
    st.markdown(" "+str(''.join(stats2.TOV)))
    st.markdown(" "+str(''.join(stats2['3P%'])))
    st.markdown(" "+str(''.join(stats2.PF)))







