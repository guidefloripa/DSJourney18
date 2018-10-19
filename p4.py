#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Guilherme Steinmann

import json
import h2o
from h2o.automl import H2OAutoML


def column_as_factor(dftrain, dftest, cols2factor):
    for col in cols2factor:
        dftrain[col] = dftrain[col].asfactor()
        dftest[col] = dftest[col].asfactor()
    return dftrain, dftest


h2o.init()

df_train = h2o.import_file('train.csv')
df_pred = h2o.import_file('test4.csv')

col_x = df_pred.columns
col_x.remove('NU_INSCRICAO')
col_x.remove('CO_UF_RESIDENCIA')
#col_x.remove('TP_DEPENDENCIA_ADM_ESC')
#col_x.remove('IN_BAIXA_VISAO')
#col_x.remove('IN_CEGUEIRA')
#col_x.remove('IN_SURDEZ')
#col_x.remove('IN_DISLEXIA')
#col_x.remove('IN_DISCALCULIA')
#col_x.remove('IN_SABATISTA')
#col_x.remove('IN_GESTANTE')
#col_x.remove('IN_IDOSO')

col_y = 'IN_TREINEIRO'

colsFactor = ['TP_COR_RACA', 'TP_NACIONALIDADE', 'TP_ST_CONCLUSAO', 'TP_ESCOLA', 'TP_ENSINO']
df_train, df_pred = column_as_factor(df_train, df_pred, colsFactor)
df_train[col_y] = df_train[col_y].asfactor()

train, valid, test = df_train.split_frame([0.8, 0.1], seed=8322)

aml = H2OAutoML(max_runtime_secs=120)
aml.train(x=col_x, y=col_y,
          training_frame=train,
          validation_frame=valid,
          leaderboard_frame=test)

lb = aml.leaderboard
print(lb)

pred = aml.leader.predict(df_pred)
print(pred)

inscricoes = df_pred['NU_INSCRICAO'].as_data_frame().values
predicoes = pred['predict'].as_data_frame().values

predictions = {}
for inscricao, p in zip(inscricoes, predicoes):
    inscricao = inscricao[0]
    #print(inscricao, p)
    predictions[inscricao] = p[0]

pred_output = []
for inscricao, resposta in predictions.items():
    curr_pred = {}
    curr_pred['NU_INSCRICAO'] = inscricao
    curr_pred['IN_TREINEIRO'] = str(resposta)
    pred_output.append(curr_pred)

saida = {}
saida['token'] = ''
saida['email'] = ''
saida['answer'] = pred_output

#print(json.dumps(saida, indent=2))

with open('saida.json', 'w') as f:
    json.dump(saida, f, indent=2)

