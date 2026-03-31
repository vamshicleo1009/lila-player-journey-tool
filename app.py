import streamlit as st
import pandas as pd
import pyarrow.parquet as pq
import os
import plotly.graph_objects as go
import base64

st.set_page_config(layout="wide")

st.title("LILA Black Player Journey Visualization Tool")

DATA_FOLDERS=[
"February_10",
"February_11",
"February_12",
"February_13",
"February_14"
]

MAP_CONFIG={
"AmbroseValley":{
"scale":900,
"origin_x":-370,
"origin_z":-473,
"image":"minimaps/AmbroseValley_Minimap.png"
},

"GrandRift":{
"scale":581,
"origin_x":-290,
"origin_z":-290,
"image":"minimaps/GrandRift_Minimap.png"
},

"Lockdown":{
"scale":1000,
"origin_x":-500,
"origin_z":-500,
"image":"minimaps/Lockdown_Minimap.jpg"
}
}

@st.cache_data
def load_day(folder):

    frames=[]

    for f in os.listdir(folder):

        path=os.path.join(folder,f)

        try:

            table=pq.read_table(path)

            df=table.to_pandas()

            df['event']=df['event'].apply(
            lambda x:x.decode('utf-8') if isinstance(x,bytes) else x
            )

            frames.append(df)

        except:
            pass

    return pd.concat(frames,ignore_index=True)


# SIDEBAR FILTERS

day=st.sidebar.selectbox("Select Day",DATA_FOLDERS)

df=load_day(day)

map_choice=st.sidebar.selectbox(
"Map",
sorted(df['map_id'].unique())
)

df=df[df['map_id']==map_choice]

match_choice=st.sidebar.selectbox(
"Match",
df['match_id'].unique()
)

df=df[df['match_id']==match_choice]

config=MAP_CONFIG[map_choice]


# BOT DETECTION (simple logic)

human_ids=set(
df[
df['event'].isin(["Position","Loot"])
]['user_id']
)

df['is_bot']=~df['user_id'].isin(human_ids)


# SIDEBAR LEGEND

st.sidebar.markdown("---")
st.sidebar.markdown("### Marker legend")

st.sidebar.markdown("● Human player")
st.sidebar.markdown("✖ Bot")

st.sidebar.markdown("Blue = Position")
st.sidebar.markdown("Yellow = Loot")
st.sidebar.markdown("Red = Bot kill")
st.sidebar.markdown("Purple = Storm death")


# TIMELINE

if 'timestamp' in df.columns:

    min_time=int(df['timestamp'].min())
    max_time=int(df['timestamp'].max())

    time_range=st.sidebar.slider(
    "Timeline",
    min_time,
    max_time,
    (min_time,max_time)
    )

    df=df[
    (df['timestamp']>=time_range[0]) &
    (df['timestamp']<=time_range[1])
    ]


# PLAYBACK

if len(df)>0:

    playback=st.sidebar.slider(
    "Playback progress",
    0,
    len(df)-1,
    len(df)-1
    )

    df=df.iloc[:playback+1]


# HEATMAP

show_heatmap=st.sidebar.checkbox("Show heatmap")


# COORDINATE CONVERSION

def convert(x,z):

    u=(x-config["origin_x"])/config["scale"]

    v=(z-config["origin_z"])/config["scale"]

    px=u*1024

    py=(1-v)*1024

    return px,py


if len(df)>0:

    df[['px','py']]=df.apply(
    lambda r:pd.Series(convert(r['x'],r['z'])),
    axis=1
    )


# LOAD MAP IMAGE

def get_base64(path):

    with open(path,"rb") as f:

        return base64.b64encode(
        f.read()
        ).decode()


img_base64=get_base64(config["image"])


# VISUALIZATION

st.subheader("Match visualization")

fig=go.Figure()


# MAP BACKGROUND

fig.add_layout_image(

dict(

source="data:image/png;base64,"+img_base64,

xref="x",

yref="y",

x=0,

y=1024,

sizex=1024,

sizey=1024,

sizing="stretch",

layer="below"

)

)


# HEATMAP

if show_heatmap and len(df)>0:

    fig.add_trace(

    go.Histogram2d(

        x=df['px'],

        y=df['py'],

        colorscale="Hot",

        opacity=0.45,

        showscale=False

    )

    )


# EVENT COLORS

event_colors={

"Position":"blue",

"Loot":"yellow",

"BotKilled":"red",

"KilledByStorm":"purple"

}


# EVENT MARKERS

for event in df['event'].unique():

    temp=df[df['event']==event]

    color=event_colors.get(event,"cyan")

    fig.add_trace(

    go.Scatter(

        x=temp['px'],

        y=temp['py'],

        mode='markers',

        name=event,

        text=temp['user_id'],

        marker=dict(

            size=temp['is_bot'].map({
            True:9,
            False:6
            }),

            color=color,

            symbol=temp['is_bot'].map({
            True:'x',
            False:'circle'
            })

        ),

        hovertemplate=
        "User:%{text}<br>"+
        "Event:"+event+
        "<br>X:%{x}<br>Y:%{y}"

    )

    )


fig.update_xaxes(

range=[0,1024],

title="X Position",

showgrid=False

)

fig.update_yaxes(

range=[0,1024],

title="Y Position",

showgrid=False

)


fig.update_layout(

height=750,

plot_bgcolor='rgba(0,0,0,0)',

paper_bgcolor='rgba(0,0,0,0)',

legend_title="Events"

)


st.plotly_chart(

fig,

use_container_width=True

)


# SUMMARY

st.subheader("Match Summary")

col1,col2,col3=st.columns(3)

col1.metric(
"Players",
df['user_id'].nunique()
)

col2.metric(
"Events",
len(df)
)

col3.metric(
"Event types",
df['event'].nunique()
)


# EVENT TABLE

st.subheader("Event counts")

event_counts=df['event'].value_counts().reset_index()

event_counts.columns=["Event","Count"]

st.dataframe(
event_counts,
use_container_width=True
)