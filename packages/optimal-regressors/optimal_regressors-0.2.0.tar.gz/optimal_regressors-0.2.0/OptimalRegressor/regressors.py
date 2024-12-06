from sklearn.metrics import mean_absolute_error
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor

def OptimalDecisionTreeRegressor(trainX,trainy,valX,valy,candidate_nodes=[5,50,500,5000],fit=False):
    model = DecisionTreeRegressor(random_state=0)
    model.fit(trainX,trainy)
    preds = model.predict(valX)
    mae = mean_absolute_error(preds,valy)
    nodes = candidate_nodes[0]
    for i in candidate_nodes:
        model = DecisionTreeRegressor(max_leaf_nodes=i,random_state=0)
        model.fit(trainX,trainy)
        preds = model.predict(valX)
        err = mean_absolute_error(preds,valy)
        if err<mae:
            mae = err
            nodes = i
    final_model = DecisionTreeRegressor(max_leaf_nodes=nodes,random_state=0)
    if fit:
        final_model.fit(trainX,trainy)
    return final_model,nodes


def OptimalRandomForestRegressor(trainX,trainy,valX,valy,candidate_nodes=[5,50,500,5000],fit=False):
    model = RandomForestRegressor(random_state=0)
    model.fit(trainX,trainy)
    preds = model.predict(valX)
    mae = mean_absolute_error(preds,valy)
    nodes = candidate_nodes[0]
    for i in candidate_nodes:
        model = RandomForestRegressor(max_leaf_nodes=i,random_state=0)
        model.fit(trainX,trainy)
        preds = model.predict(valX)
        err = mean_absolute_error(preds,valy)
        if err<mae:
            mae = err
            nodes = i
    final_model = RandomForestRegressor(max_leaf_nodes=nodes,random_state=0)
    if fit:
        final_model.fit(trainX,trainy)
    return final_model