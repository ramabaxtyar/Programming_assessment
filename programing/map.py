from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px

app = Flask(__name__)

file_path = 'C:/Users/ramab/Downloads/programing/1976-2020-president.csv'
data = pd.read_csv(file_path)

def preprocess_data(data):
    data['year'] = data['year'].astype(str)
    data['candidatevotes'] = data['candidatevotes'].astype(int)
    data['totalvotes'] = data['totalvotes'].astype(int)
    return data


data = preprocess_data(data)
unique_years = sorted(data['year'].unique())


def get_winner(data, year):
    data_year = data[data['year'] == year]
    winner_states = data_year.groupby('state_po').apply(lambda x: x.loc[x['candidatevotes'].idxmax()])
    winner = winner_states['candidate'].value_counts().idxmax()
    winner_party = winner_states[winner_states['candidate'] == winner]['party_simplified'].iloc[0]
    states_won = winner_states['candidate'].value_counts().max()
    return winner, winner_party, states_won

def create_states_pie_chart(data, year):
    data_year = data[data['year'] == year]
    winner_states = data_year.groupby('state_po').apply(lambda x: x.loc[x['candidatevotes'].idxmax()])
    top_candidates = winner_states['candidate'].value_counts().head(2)
    fig = px.pie(top_candidates, names=top_candidates.index, values=top_candidates.values, 
                 title=f'States Won Distribution by Candidate in {year}')
    return fig


def create_states_choropleth(data, year):
    data_year = data[data['year'] == year]
    winner_states = data_year.groupby('state_po').apply(lambda x: x.loc[x['candidatevotes'].idxmax()])
    top_candidates = winner_states['candidate'].value_counts().head(5).index
    data_top = winner_states[winner_states['candidate'].isin(top_candidates)]
    fig = px.choropleth(data_top, 
                        locations='state_po', 
                        locationmode="USA-states", 
                        color='candidate',
                        hover_name='state_po',
                        labels={'candidate': 'Top Candidates'},
                        title=f'Top 2 Candidates by State Won in {year}',
                        scope="usa",
                        )
    fig.update_geos(showcountries=False, showcoastlines=False, projection_type="albers usa")
    fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
    return fig

@app.route('/', methods=['GET', 'POST'])
def home():
    year = request.args.get('year')
    chart_type = request.args.get('chart_type')
    plot_div = None
    winner_name, winner_party, states_won = None, None, None
    if request.method == 'POST':
        year = request.form['year']
        chart_type = request.form['chart_type']
        winner_name, winner_party, states_won = get_winner(data, year)
        if chart_type == 'plot':
            plot_div = create_states_pie_chart(data, year).to_html(full_html=False, default_height=600, default_width=1000)
        elif chart_type == 'map':
            plot_div = create_states_choropleth(data, year).to_html(full_html=False, default_height=600, default_width=1000)
    return render_template('index1.html', year=year, years=unique_years, plot_div=plot_div, chart_type=chart_type, winner=winner_name, winner_party=winner_party, states_won=states_won)

if __name__ == '__main__':
    app.run(debug=True)
