import plotly.express as px

fig = px.scatter(x=[1, 2, 3], y=[4, 5, 6])
fig.write_image(
    "c:/temp/figure.png")

