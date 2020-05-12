#!/usr/bin/python
import pandas as pd
import plotly as py
import plotly.graph_objs as go
py.offline.init_notebook_mode(connected=True)
from plotly.subplots import make_subplots

def readNetworkData(path):
    entropy=[]
    frameData=[]
    with open(path) as file:
        print("read file {0}".format(path))
        frameLines= []
        entropiaLine = ''
        for i, line in enumerate(file):
            if(line.find('Entropia')!=-1):
                en = parseEntropia(line)
            elif(line.find('(')!=-1):
                frameLines.append(parseType(line))
            elif(line.find('frames')!=-1):
                frameLines = parseFrame(line,frameLines)
                frameData = frameData + frameLines
                frameLines=[]
                entropiaLine = ''
                entropy.append(en)
    dfEntropy = pd.DataFrame.from_dict(entropy)
    dfEntropy.columns=['value']
    return pd.DataFrame.from_dict(frameData),dfEntropy
            
def parseEntropia(line):
    return float(line.split(':')[2])

#example of line
# ('UNICAST', 2048) : 0.99942 --- Info:  0.00084
def parseType(line):
    itemType,itemSize = line[line.find('(')+1:line.find(')')].split(', ')
    subs1 = line[line.find(')')+4:]
    value = float(subs1.split('---')[0])
    info= float(subs1.split('---')[1].split(':')[1])
    return {
        'type':itemType,'size':itemSize,'value':value,'info':info       
    }

def parseFrame(line,frameLines):
    frameNumber = int(line.split(' ')[0])
    for frame in frameLines:
        frame.update({'frame':frameNumber})
    
    return frameLines
def drawPiePercentage(df):
    fig = go.Figure(data=[go.Pie(labels=df['type'], values=df['value'])])
    fig.write_html('pie.html', auto_open=True)

def drawProtocols(df):
    df['protocol']= df.apply(addProtocolName,axis=1)
    ipv4=0
    others=0
    woIPV4= df[df['protocol']!='IPV4']
    for index,row in df.iterrows():
        if(row['protocol']=='IPV4'):
            ipv4+=row['value']
        else:
            others+=row['value']

    fig = make_subplots(rows=1, cols=2,specs=[[{"type": "pie"}, {"type": "bar"}]])
    fig.add_trace(go.Pie(values=[ipv4,others],labels=['IPV4','OTHERS']), 1,1)
    fig.add_trace(go.Bar(y=woIPV4['value'],x=woIPV4['protocol'],showlegend=False),1,2)
    fig.write_html('protocols.html', auto_open=True)
    
    
def drawEntropy(df):
    fig = go.Figure(data=[go.Scatter(y=df['value'])])
    tickXfont = dict(
        font=dict(
            family="Courier New",
            size=14,
            color="#2a3f5f"),
        text='frame'
    )
    xaxis=dict(
        nticks=40,
        tickfont=dict(size=10,family='Courier New'),
        ticks='outside',
        title=tickXfont,
        exponentformat="power",
        showticklabels=True,
        type="linear",
        visible=True,
        rangemode="normal",
        color="#444",
        showexponent="all",
        separatethousands=False,
        ticklen=5,
        tickwidth=1,
        tickcolor="#444",
        linewidth=1,
        gridcolor="#EBF0F8",
        linecolor='#C5CED9',
        gridwidth=1,
        zerolinecolor="#EBF0F8",
        zerolinewidth=2,
        zeroline=True,
        automargin=True,
        layer="above traces",
        fixedrange=False,
        constrain="range",
        constraintoward="center"
    )
    fig.update_layout(xaxis=xaxis,title='Evolucion entropia', yaxis_title="valor entropia",xaxis_title='frame',plot_bgcolor='#FFF' )
    fig.write_html('entropy.html', auto_open=True)
    
def getLastRecord(df):
    last= df[df['frame']==df['frame'].max()].copy()
    last['protocol']=last.apply(addProtocolName,axis=1)
    return last

def addProtocolName(c):
    if c['type'].find('UNICAST')!=1 and int(c['size']) == 2048:
        return 'IPV4'
    elif c['type'].find('BROADCAST')!=1 and int(c['size']) == 2054:
        return 'ARP'
    elif c['type'].find('UNICAST')!=1 and int(c['size']) == 34525:
        return 'IPV6'
    elif c['type'].find('UNICAST')!=1 and int(c['size']) == 35130:
        return 'IEEE 1905'
    elif c['type'].find('UNICAST')!=1 and int(c['size']) == 35020:
        return 'LLDP'
    else:
        return 'N/A'