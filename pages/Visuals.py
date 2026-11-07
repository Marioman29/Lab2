# This creates the page for displaying data visualizations.

import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visuals",
    page_icon="📈",
)

# PAGE TITLE
st.title("Data Visualizations 📈")


# PART 1: GRAPHS FROM data.json
whdate = pd.read_json("data.json")
states = whdate["Waffle Houses per State"].keys().tolist()
numbs = whdate["Waffle Houses per State"].tolist()
dee = whdate.keys()


st.header("The number of Waffle House locations per State")
st.write("Here is a breakdown of all the waffle house locations in each state. Enter a state name to find the specific amount. If there are no waffle houses in the state it will return that there are none")
whdata = pd.DataFrame({
    "State": states,
    "value": numbs
})

selected = st.text_input("Select a state")

colors = [
    "gold" if state.lower() == selected.lower() else "lightblue"
    for state in whdata["State"]
]

pull = [
    0.2 if state.lower() == selected.lower() else 0
    for state in whdata["State"]
]

fig = px.pie(
    whdata,
    names="State",
    values="value"
)

fig.update_traces(
    marker=dict(
        colors=colors,
        line=dict(color="white",width=2)),
    pull=pull
)

st.plotly_chart(fig, use_container_width=True)

# Optional feedback

if selected:
    if selected.lower() in [state.lower() for state in states]:
        st.success(f"{selected} highlighted!")
    else:
        st.warning(f"There are no Waffle Houses in {selected}")
st.subheader("Waffle House Locations by State (Bar Chart)")

bar_chart = alt.Chart(whdata).mark_bar().encode(
    x=alt.X("State:N", sort="-y"),
    y="value:Q",
    color=alt.condition(
        alt.datum.State == selected,
        alt.value("gold"),
        alt.value("steelblue")
    ),
    tooltip=["State", "value"]
).properties(
    height=500
)

st.altair_chart(bar_chart, use_container_width=True)       
# PART 2: GRAPHS FROM data.csv
st.header("Genres by songs:")
st.write("On the survey page you can input some values of genres of songs that you listen to and how many songs of each genre you like.")
data = pd.read_csv('date.csv')
if len(data) > 3:
    st.bar_chart(data,x = "Genre",y = "Songs")
st.subheader("Genre Data Pie Chart")

min_value = st.number_input(
    "Show only entries with values greater than or equal to:",
    min_value=0,
    value=0,
    step=1
)

filtered_data = data[data["Songs"] >= min_value]

if not filtered_data.empty:
    anime_fig = px.pie(
        filtered_data,
        names="Genre",
        values="Songs",
        title=f"Genres with {min_value}+ Songs"
    )

    st.plotly_chart(anime_fig, use_container_width=True)
else:
    st.warning("No data matches that value.")



