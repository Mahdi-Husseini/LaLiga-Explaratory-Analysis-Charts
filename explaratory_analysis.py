import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import matplotlib.pyplot as plt
import mplcyberpunk as cp
import numpy as np
from PIL import Image
import pygwalker as pyg


st.set_page_config(
    page_title="LaLiga Explaratory Data Analysis",
    layout="wide"
)

matches = pd.read_csv('La-Liga-Stats-0.csv', encoding='utf-8')

# Use map with a lambda function to filter non-ASCII characters
def convert_to_ascii(x):
  if isinstance(x, str):  # Check if it's a string before encoding
    return x.encode('ascii', 'ignore').decode()  # Convert and ignore errors
  else:
    return x  # Return non-strings as they are

matches = matches.map(convert_to_ascii)  # Apply the function element-wise

image = Image.open('football.jpeg')

st.write("""
# LaLiga Half Season Explaratory Data Analysis 

This app represents different types of charts for stats from LaLiga

***""")

st.sidebar.header('W-d-L')
w = st.sidebar.checkbox('W')
d = st.sidebar.checkbox('D')
l = st.sidebar.checkbox('L')

st.dataframe(matches) # fig 1
st.write("***")

st.header('Points of each team') # Figure 2
plt.style.use('cyberpunk')

colors = ['C0', 'C1', 'C2', 'C3', 'C4', 'C5']


fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(matches['Squad'], matches['Pts'], color=colors, zorder=2)

cp.add_bar_gradient(bars=bars)
cp.add_underglow()

ax.set_xticks(matches['Squad'])
ax.set_xticklabels(matches['Squad'], rotation=90)
ax.set_yticks(np.arange(0, 55, 5))
ax.set_title('Points of each team in first half season in La-Liga')

st.pyplot(fig)

st.write('***')

st.header('Results of matches played per team') # figure 3

bar_height = 0.2

index = np.arange(len(matches['Squad']))

fig, ax = plt.subplots(figsize=(10, 6))

if w and d and l:
  ax.barh(index - bar_height, matches['W'], height=bar_height, label='Wins', color='C3')
  ax.barh(index, matches['D'], height=bar_height, label='Draws', color='gray')
  ax.barh(index + bar_height, matches['L'], height=bar_height, label='Losses', color='C4')
elif w and d:
  ax.barh(index - bar_height, matches['W'], height=bar_height, label='Wins', color='C3')
  ax.barh(index, matches['D'], height=bar_height, label='Draws', color='gray')
elif d and l:
  ax.barh(index, matches['D'], height=bar_height, label='Draws', color='gray')
  ax.barh(index + bar_height, matches['L'], height=bar_height, label='Losses', color='C4')
elif w and l:
  ax.barh(index - bar_height, matches['W'], height=bar_height, label='Wins', color='C3')
  ax.barh(index + bar_height, matches['L'], height=bar_height, label='Losses', color='C4')
elif w:
  ax.barh(index - bar_height, matches['W'], height=bar_height, label='Wins', color='C3')
elif d:
  ax.barh(index, matches['D'], height=bar_height, label='Draws', color='gray')
elif l:
  ax.barh(index + bar_height, matches['L'], height=bar_height, label='Losses', color='C4')
else:
  ax.barh(index - bar_height, matches['W'], height=bar_height, label='Wins', color='C3')
  ax.barh(index, matches['D'], height=bar_height, label='Draws', color='gray')
  ax.barh(index + bar_height, matches['L'], height=bar_height, label='Losses', color='C4')


ax.set_ylabel('Team')
ax.set_xlabel('Matches')
ax.set_title('Results of the Matches of Teams')
ax.set_yticks(index)
ax.set_yticklabels(matches['Squad'])
ax.legend()

st.pyplot(fig)

st.write('***')

perc = [(matches['W'][t] / matches['MP'][t]) * 100 for t in range(len(matches['Squad']))]    #fig 4


colors = ['C0', 'C1', 'C2', 'C3', 'C4', 'C5']


st.title('Winning Percentage Of Each Team')
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(matches['Squad'], perc, color=colors, zorder=2)
ax.set_xlabel('Team')
ax.set_ylabel('Win Percentage')
ax.set_xticks(matches['Squad'])
ax.set_xticklabels(matches['Squad'], rotation=90)
ax.set_yticks(np.arange(0, 85, 5))
ax.set_title('Win Percentage of Teams')

for bar in bars:
    cp.add_bar_gradient(bars=[bar])


st.pyplot(fig)

st.write('***')              #fig 5,6
st.title("Points for Each Team Over Weeks")
points = pd.read_csv('points.csv')
points.set_index('Week', inplace=True)
st.write(points)

selected_teams = st.sidebar.multiselect('Select Teams', list(points.columns), default=list(points.columns))


colors = ['blue', 'red', 'green', 'orange', 'purple', 'cyan',
          'yellow', 'magenta', 'lime', 'teal', 'pink', 'brown',
          'skyblue', 'lightcoral', 'lightgreen', 'gold', 'violet',
          'turquoise', 'salmon', 'lightsteelblue']


fig, ax = plt.subplots(figsize=(10, 6))


for team, color in zip(list(points.columns), colors):
    if team in selected_teams:
        ax.plot(points.index, points[team], label=team, color=color)


ax.set_xlabel('Week')
ax.set_ylabel('Points')
ax.set_xticks(np.arange(1, 20, 1))
ax.set_title('Trend of Points for Each Team Over Weeks')


ax.legend()


plt.style.use('cyberpunk')
cp.add_underglow()
cp.add_glow_effects()

st.pyplot(fig)

st.write('***')   



#fig 7,8
st.title("Goal_difference for Each Team Over Weeks")
goals = pd.read_csv('goals.csv')
goals.set_index('week', inplace=True)
st.write(goals)


colors = ['blue', 'red', 'green', 'orange', 'purple', 'cyan',
          'yellow', 'magenta', 'lime', 'teal', 'pink', 'brown',
          'skyblue', 'lightcoral', 'lightgreen', 'gold', 'violet',
          'turquoise', 'salmon', 'lightsteelblue']


fig, ax = plt.subplots(figsize=(10, 6))


for team, color in zip(list(goals.columns), colors):
    if team in selected_teams:
        ax.plot(goals.index, goals[team], label=team, color=color)


ax.set_xlabel('Week')
ax.set_ylabel('Goal-Difference')
ax.set_xticks(np.arange(1, 20, 1))
ax.set_title('Trend of Goal-Difference for Each Team Over Weeks')


ax.legend(loc = 'upper left')


plt.style.use('cyberpunk')
cp.add_underglow()
cp.add_glow_effects()

st.pyplot(fig)


#fig 9, 10
st.title("Goal-Acummulation for Each Team Over Weeks")
goals_count = pd.read_csv('goals_count.csv')
goals_count.set_index('week', inplace=True)
st.write(goals_count)


colors = ['blue', 'red', 'green', 'orange', 'purple', 'cyan',
          'yellow', 'magenta', 'lime', 'teal', 'pink', 'brown',
          'skyblue', 'lightcoral', 'lightgreen', 'gold', 'violet',
          'turquoise', 'salmon', 'lightsteelblue']


fig, ax = plt.subplots(figsize=(10, 6))


for team, color in zip(list(goals_count.columns), colors):
    if team in selected_teams:
        ax.plot(goals_count.index, goals_count[team], label=team, color=color)


ax.set_xlabel('Week')
ax.set_ylabel('Goal-Count')
ax.set_xticks(np.arange(1, 20, 1))
ax.set_title('Trend of Goal-Acummulation for Each Team Over Weeks')


ax.legend(loc = 'upper left')


plt.style.use('cyberpunk')
cp.add_underglow()
cp.add_glow_effects()

st.pyplot(fig)

st.write("***")

st.title("Free Dynamic Plotting")
pyg_html = pyg.to_html(matches)
 
# Embed the HTML into the Streamlit app
components.html(pyg_html, height=1000, scrolling=True)
