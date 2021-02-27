from flask import Flask, render_template, request
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
import numpy as np
import pandas as pd
import altair as alt
from sklearn.cluster import KMeans 
import requests
import folium

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/largeplot')
def largealtair_plot():

    keyvalues=['balanc',
    'discount',
    'divers',
    'food',
    'free coff',
    'free lunch',
    'gym',
    'health',
    'ice cream',
    'incent',
    'pay',
    'perk',
    'rais',
    'sign bonus',
    'stock option',
    'stress',
    'student loan pay',
    'surf',
    'vacat',
    'women',
    'work environ',
    'work home']
    if not request.args.get("company"):           
      raise RuntimeError("Missing company name, go back and select company")

    comp = request.args.get('company')  #gets company name from index
    c = pd.read_csv('clusters.csv') 
    # c=c.drop(labels='cluster', axis=1) #old cluster only
    ##############################################################
    #
    #                  Normalize the data before running k-means
    #
    ##############################################################

    sample_size = pd.read_csv('li_samplesize.csv', header= None)
    sample_size = sample_size.rename(columns={0: "company", 1: "sample_size"})
    t = pd.merge(c, sample_size, how = "left", on = 'company')
    t=t.drop(t.columns[0], axis=1) #get rid of unamed
    t = t.set_index('company') #leave only numbers
    t = t.div(t.sample_size, axis=0)
    t = round(t*100,3)
    t = t.drop(labels='sample_size', axis=1) #remove column, we no longer need it
    n = t.reset_index()  #no index
# d=pd.read_csv('d.csv')
    d = n.set_index('company')  #index
    d = t.fillna(0)
    d = t.astype(float)
    
    #################################################
    #
    #  Dimensionality reduction and k-means
    #
    ################################################
    twod_pca = PCA(n_components=2)
    X_pca = twod_pca.fit_transform(d)
    #lets find the best number of clusters based on silhouete

    cluster_silhouete={}
    for n_clustersi in range(2, 10): #min between number of samples and features
        km1 = KMeans(n_clusters=n_clustersi)
        km1.fit(X_pca)
        # Predict the cluster for each data point
        preds1 = km1.predict(X_pca)
        # Calculate the mean silhouette coefficient for the number of clusters chosen
        score = silhouette_score(X_pca, preds1, metric='euclidean')
        cluster_silhouete[n_clustersi]= score.round(5)

     #order dict and maximize it
    sorted_cluster_stats=dict(sorted(cluster_silhouete.items(), key=lambda item: item[1], reverse=True))
    n_clusterso=list(sorted_cluster_stats.keys())[0] #redifine n clusters

    #we run the kmeans again with the prefered number of clusters 
    km = KMeans(n_clusters=n_clusterso, random_state=11).fit(X_pca)
    predsi = km.predict(X_pca)
    
    #and graph
    df_km = pd.DataFrame(data={'pca1':X_pca[:,0], 'pca2':X_pca [:,1], 'cluster':predsi, 'company':list(d.index)})
    # df_km=df_km.set_index('company')
    brush = alt.selection(type='interval')
    #graph centers
    centers = km.cluster_centers_
    labels = km.labels_
    sauce = [] #sauce is where the centers are stored, it is the source
    for i in range(len(centers)):
        sauce.append({"x": centers[:, 0][i], "y": centers[:, 1][i]})

    source=pd.DataFrame.from_records(sauce)
    #################
    #
    #And graph the clusters
    #
    ##############
    poin=alt.Chart(source).mark_point(
        color='black',
        size=100
    ).encode(
        x='x',
        y='y',
        # tooltip=['cluster center']
        )
    points = alt.Chart(df_km).mark_circle(size=60).encode(
        x='pca1:Q',
        y='pca2:Q',
        color = 'cluster:N',
        tooltip =['company:N'],
        shape = 'comp:N'
        ).properties(
        height = 350,
         width = 600
    ).interactive()

    json3 = (points +poin).to_json()
        
    #Do a little clustering map to compare averages

    # c['cluster']=labels #reseting the cluster labels
    d['cluster'] = labels

    # di2=c.set_index('company')
    # g=di2.groupby('cluster')
    g=d.groupby('cluster')

    m=g.mean()
    a=m.reset_index()
    m_long = a.melt(id_vars='cluster', value_vars=keyvalues)
    m_long=m_long.rename(columns={"value": "score", "variable": "keyword"})

    base2 = alt.Chart(m_long).mark_bar().encode(
        alt.X('cluster:N'),
        alt.Y('score:Q', title ='Score % '),
        color = alt.Color('score:Q',scale=alt.Scale(scheme='darkred')),
        opacity = alt.value(.7),
         tooltip =['score:Q']
    ).properties(
        height = 200,
        width = 200
    ).add_selection(
        brush).interactive()
  

   # A dropdown filter
    columns = keyvalues
    column_dropdown = alt.binding_select(options=columns)
    column_select = alt.selection_single(
        fields=['keyword'],
        on='doubleclick',
        clear=False, 
        bind=column_dropdown, 
        name='search',
        init={'keyword': 'balanc'}
    )
    filter_columns2 = base2.add_selection(
        column_select
    ).transform_filter(
        column_select)

    json4=filter_columns2.to_json()

    # get_clustered_companies_to compare_with
    ##################################
    #
    #List of companies inside cluster group
    #
    ################################
    try:
        number = d.loc[[comp],['cluster']].values[0][0]
    except:
        return render_template('error.html')	

    #number = d.loc[[comp],['cluster']].values[0][0]
    if number == 0:
        r = d.loc[d['cluster'] == 0]
    if number ==1:
        r = d.loc[d['cluster'] == 1]
    if number==2:
        r = d.loc[d['cluster'] == 2]
    if number==3:
        r = d.loc[d['cluster'] == 3]
    if number==4:
        r = d.loc[d['cluster'] == 4]
    if number==5:
        r = d.loc[d['cluster'] == 5]
    if number==6:
        r = d.loc[d['cluster'] == 6] 
    if number==7:
        r = d.loc[d['cluster'] == 7] 
    if number==8:
        r = d.loc[d['cluster'] == 8]  
    if number==9:
        r = d.loc[d['cluster'] == 9] 

    #########################
    #
    #Make a plot that compares all keyvalues of  all companies withing cluster
    #
    #############
    ri = list(r.index.values)
    ind = list(d.index)
    not_ri = []
    for item in ind:
        if item not in ri:
            not_ri.append(item)

    n = d.reset_index()
    filter_c = n[n.company.isin(ri)]
    c_num1 = len(n.groupby('cluster'))
    
    num = len(ri)
    if num < 30:
        height = 200
    if num>29 and num <200:
        height= 2200
    else:
        height = 3200
   
    c_long = filter_c.melt(id_vars='company', value_vars =keyvalues)
    c_long=c_long.rename(columns={"value": "score", "variable": "keyword"})
    base = alt.Chart(c_long).mark_bar().encode(
        alt.Y('company:N', title=' '),
        alt.X('score:Q', title='Score %'),
        color=alt.Color('score:Q',scale=alt.Scale(scheme='cividis')),
        opacity=alt.value(.7),
        tooltip=['score:Q']
    ).properties(
        height=height)
    rule = alt.Chart(c_long).mark_rule(color='red').encode(
    y='mean(score)')
    # A dropdown filter
    columns = list(c.columns.values[2:])
    column_dropdown = alt.binding_select(options=columns)
    column_select = alt.selection_single(
        fields = ['keyword'],
        on = 'doubleclick',
        clear = False, 
        bind = column_dropdown, 
        name = 'search',
        init = {'keyword': 'balanc'}
    )
    filter_columns = base.add_selection(
        column_select
    ).transform_filter(
        column_select
    ).interactive()
    json = (filter_columns).to_json()#filter_columns+rule).to_json()

    #######################################################
    #Company Profile (first graph on the plot page)
    ########################################################
    
    
    d2 = d.drop(labels = 'cluster', axis = 1)
    # d2=d2.set_index('company')
    tra = d2.T
    tra.reset_index(drop = False, inplace = True)
    tra_long = tra.melt(id_vars = 'index', value_vars=comp)
    tra_long =tra_long.rename(columns = {"value": "score", "variable": "keyword"})
    base = alt.Chart(tra_long).mark_bar().encode(
        alt.X('index:N',title = " "),
        alt.Y('score:Q', title ='Score % '),
        color = alt.Color('score:Q',scale = alt.Scale(scheme = 'darkgreen')),
        opacity = alt.value(.7),
        tooltip = ['score:Q']
    ).properties(
        height = 300,
        width = 550
    ).interactive()
    json2 = (base).to_json()

  
    #*********************************************************
    #
    #3 most important keywords to explore graph
    #
    #########################################
    db=n #changed from c
    brush = alt.selection(type='interval')

    keyword1 = request.args.get("keyword1")
    keyword2 = request.args.get("keyword2")
    keyword3 = request.args.get("keyword3")

    # keydict={'work-life balance':"balanc","free coffee":'free coff', 'gym':"gym"}

    points = alt.Chart(db).mark_point().encode(
        x = alt.X(keyword1),
        y = alt.Y(keyword2),
        color = alt.Color('company:N', legend=None),
        size = keyword3,
        tooltip = [keyword1,keyword2,keyword3,'pay', 'company']
    ).properties(
        height = 300,
        width = 500).add_selection(
        brush).interactive()
    json5 = points.to_json()
    
#*************************************************************************

#RECLUSTER GROUP
#need to relabel new dataFrame with new clusters

#************************************************************************
    
    #1. make new database d3 based on selections

    no_ind = n
    make_new = pd.DataFrame(no_ind['company']) #using company names
    if not request.args.getlist("features"):           
        raise RuntimeError("Must check at least two boxes, go back and select two boxes. Also make triplesure your company field is not blank.")
    features = request.args.getlist("features") #and features from index
    if len(features) < 2: #raise error
        return render_template('error2.html')    	
    for keys in features:
        make_new[keys] = no_ind[keys]

    #2. prepare data to be graphed
    d3 = make_new.set_index('company')
    tra = d3.T
    tra.reset_index(drop = False, inplace = True)
    tra_long = tra.melt(id_vars = 'index', value_vars = comp)
    tra_long = tra_long.rename(columns = {"value": "score", "variable": "keyword"})

    base = alt.Chart(tra_long).mark_bar().encode(
        alt.X('index:N',title = " "),#comp),
        alt.Y('score:Q', title ='Score % '),
        color = alt.Color('score:Q',scale = alt.Scale(scheme='darkgreen')),
        opacity = alt.value(.7),
        tooltip = ['score:Q']
    ).properties(
        height = 200,
        width = 300
    ).interactive()
    json7 = (base).to_json()

    twod_pca = PCA(n_components = 2)
    X_pca = twod_pca.fit_transform(d3)

    km1 = KMeans(n_clusters = 5, random_state = 1301).fit(d3)
    preds = km1.predict(d3)
    #get the best number of clusters
    cluster_silhouete = {}
    for n_clustersi in range(2, 10): #min between number of samples and features
        km1 = KMeans(n_clusters=n_clustersi)
        km1.fit(X_pca)
        # Predict the cluster for each data point
        preds1 = km1.predict(X_pca)

        # Calculate the mean silhouette coefficient for the number of clusters chosen
        score = silhouette_score(X_pca, preds1, metric='euclidean')
        cluster_silhouete[n_clustersi] = score.round(5)

     #order dict and maximize it
    sorted_cluster_stats = dict(sorted(cluster_silhouete.items(), key=lambda item: item[1], reverse=True))
    n_clusterso = list(sorted_cluster_stats.keys())[0] #redifine n clusters

    #we run the kmeans again with the prefered number of clusters 
    km = KMeans(n_clusters=n_clusterso, random_state=11).fit(X_pca)
    predsi = km.predict(X_pca)
    #and graph
    # df_km = pd.DataFrame(data={'pca1':X_pca[:,0], 'pca2':X_pca [:,1], 'cluster':predsi})
    df_km = pd.DataFrame(data = {'pca1':X_pca[:,0], 'pca2':X_pca [:,1], 'cluster':predsi, 'company':list(d.index)})
    # brush = alt.selection(type='interval')
    #graph centers
    centers=km.cluster_centers_
    labels2 = km.labels_
    # di=d.set_index('company')
    di = d
    di['cluster'] = labels2
    number2 = di.loc[[comp],['cluster']].values[0][0]
    if number2== 0:
        r= di.loc[di['cluster'] == 0]
    if number2 ==1:
        r= di.loc[di['cluster'] == 1]
    if number2 == 2:
        r= di.loc[di['cluster'] == 2]
    if number2 == 3:
        r= di.loc[di['cluster'] == 3]
    if number2 == 4:
        r= di.loc[di['cluster'] == 4]
    if number2 == 5:
        r= di.loc[di['cluster'] == 5]
    if number2 == 6:
        r= di.loc[di['cluster'] == 6]
    if number2 == 7:
        r= di.loc[di['cluster'] == 7] 
    if number2 == 8:
        r= di.loc[di['cluster'] == 8] 
    if number2 == 9:
        r= di.loc[di['cluster'] == 9] 

    c_num2 = len(di.groupby('cluster'))
    ri2 = list(r.index.values)
    ind = list(di.index)
    not_ri2 = []
    for item in ind:
        if item not in ri2:
            not_ri2.append(item)
    
    #get the sauce to graph the centers
    sauce = []
    for i in range(len(centers)):
        sauce.append({"x": centers[:, 0][i], "y": centers[:, 1][i]})

    source = pd.DataFrame.from_records(sauce)
    poin = alt.Chart(source).mark_point(
        size=100,
        color='black'
    ).encode(
        x = 'x',
        y = 'y')
    
    points = alt.Chart(df_km).mark_circle(size = 60).encode(
        x = 'pca1:Q',
        y = 'pca2:Q',
        color = 'cluster:N',
        tooltip = ['company:N']).properties(
    height = 250,
    width = 400
    ).interactive()
                    #color="white", alpha=1, s=200, edgecolor='k').mark_circle(size=100
    


    json6 = (points +poin).to_json()

#filter c with only group members, label and do cluster averages

    dnew = d
    dnew['cluster'] = labels2

    g2 = dnew.groupby('cluster')
    m = g2.mean()
    a2 = m.reset_index()
    m_long2 = a2.melt(id_vars='cluster', value_vars = keyvalues)
    m_long2 = m_long2.rename(columns = {"value": "score", "variable": "keyword"})
    brush = alt.selection(type = 'interval')
    base3 = alt.Chart(m_long2).mark_bar().encode(
        alt.X('cluster:N'),
        alt.Y('score:Q', title ='Score % '),
        color = alt.Color('score:Q',scale = alt.Scale(scheme = 'darkred')),
        opacity = alt.value(.7),
        tooltip = ['score:Q']
    ).properties(
        height = 200,
        width = 200
    ).add_selection(
        brush).interactive()
# A dropdown filter
    columns = features
    column_dropdown = alt.binding_select(options=columns)
    column_select = alt.selection_single(
        fields = ['keyword'],
        on = 'doubleclick',
        clear = False, 
        bind = column_dropdown, 
        name = 'search',
        init = {'keyword': 'balanc'}
    )
    filter_columns3 = base3.add_selection(
        column_select
    ).transform_filter(
        column_select)

    json8 = filter_columns3.to_json()

    return render_template('plot.html', json = json, json2 = json2, json3 = json3, json4 = json4, json5 = json5, json6 = json6, lila = ri, lila2 = ri2, not_ri2 = not_ri2, not_ri = not_ri, company = comp, json7 = json7, json8 = json8, number = number, number2 = number2,c_num2 = c_num2,c_num1 = c_num1)


            
if __name__ == '__main__':
    app.run(port=33507, debug=True)