#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Guilherme Steinmann

import json
import numpy as np
import pandas as pd
import h2o
from h2o.automl import H2OAutoML

code = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5}


def code_len():
    return 6


def resp2code(r):
    if r in code.keys():
        return code[r]
    else:
        return 0


def code2resp(c):
    for k, v in code.items():
        if v == c:
            return k
    return '*'


def get_data():
    df = pd.read_csv('train.csv')

    X = []
    Y = []
    N = 0
    nfactors = 52
    for index, row in df.iterrows():
        if N > 30000:
            break

        tp_presenca_mt = row['TP_PRESENCA_MT']
        tx_respostas_mt = row['TX_RESPOSTAS_MT']
        if tx_respostas_mt is pd.np.nan:
            continue

        assert tp_presenca_mt == 1
        assert len(tx_respostas_mt) == 45

        r_mt_treino = [resp2code(r) for r in tx_respostas_mt[:-5]]
        if np.count_nonzero(np.array(r_mt_treino)) < 30:
            print(tx_respostas_mt)
            continue

        tp_sexo = row['TP_SEXO']
        tp_escola = row['TP_ESCOLA']
        in_treineiro = row['IN_TREINEIRO']
        co_prova_mt = row['CO_PROVA_MT']
        nu_nota_lc = row['NU_NOTA_LC']
        q001 = row['Q001']
        q002 = row['Q002']
        q006 = row['Q006']
        q024 = row['Q024']
        q025 = row['Q025']
        q026 = row['Q026']
        q027 = row['Q027']
        q047 = row['Q047']

        if q001 == 'A' or q001 == 'B' or q001 == 'C' or q001 == 'D' or q001 == 'E':
            q001 = 'P1'
        else:
            q001 = 'P2'

        if q002 == 'A' or q002 == 'B' or q002 == 'C' or q002 == 'D' or q002 == 'E':
            q002 = 'M1'
        else:
            q002 = 'M2'

        if q006 == 'A' or q006 == 'B' or q006 == 'C':
            q006 = 'R1'
        elif q006 == 'D' or q006 == 'E' or q006 == 'F' or q006 == 'G':
            q006 = 'R2'
        else:
            q006 = 'R3'

        if q024 == 'A':
            q024 = 'N'
        else:
            q024 = 'Y'

        if q026 == 'A' or q026 == 'B':
            q026 = 'Y'
        else:
            q026 = 'N'

        if q027 == 'A' or q027 == 'B' or q027 == 'C' or q027 == 'D' or q027 == 'E':
            q027 = 'AR'
        else:
            q027 = 'SR'

        if q047 == 'A' or q047 == 'B':
            q047 = 'Pub'
        else:
            q047 = 'Pri'

        x = []
        x.append(nu_nota_lc)
        #x.append(nu_nota_redacao)
        x.append(tp_sexo)
        x.append(1 if tp_escola == 2 else 0)
        x.append(in_treineiro)
        x.append(co_prova_mt)
        x.append(q001)
        x.append(q002)
        x.append(q006)
        x.append(q024)
        x.append(q025)
        x.append(q026)
        x.append(q027)
        x.append(q047)
        for r in tx_respostas_mt[:-5]:
            x.append(resp2code(r))

        y = []
        for r in tx_respostas_mt[-5:]:
            y.append(resp2code(r))

        X.append(x)
        Y.append(y)
        N += 1

    X = np.array(X)
    Y = np.array(Y)
    return X, Y, nfactors


def get_test():
    df = pd.read_csv('test3.csv')

    X = []
    N = 0
    nfactors = 52
    for index, row in df.iterrows():
        if N > 10000:
            break

        tp_presenca_mt = row['TP_PRESENCA_MT']
        tx_respostas_mt = row['TX_RESPOSTAS_MT']
        if tx_respostas_mt is pd.np.nan:
            continue

        assert tp_presenca_mt == 1
        assert len(tx_respostas_mt) == 40

        inscricao = row['NU_INSCRICAO']
        tp_sexo = row['TP_SEXO']
        tp_escola = row['TP_ESCOLA']
        in_treineiro = row['IN_TREINEIRO']
        co_prova_mt = row['CO_PROVA_MT']
        nu_nota_lc = row['NU_NOTA_LC']
        q001 = row['Q001']
        q002 = row['Q002']
        q006 = row['Q006']
        q024 = row['Q024']
        q025 = row['Q025']
        q026 = row['Q026']
        q027 = row['Q027']
        q047 = row['Q047']

        if q001 == 'A' or q001 == 'B' or q001 == 'C' or q001 == 'D' or q001 == 'E':
            q001 = 'P1'
        else:
            q001 = 'P2'

        if q002 == 'A' or q002 == 'B' or q002 == 'C' or q002 == 'D' or q002 == 'E':
            q002 = 'M1'
        else:
            q002 = 'M2'

        if q006 == 'A' or q006 == 'B' or q006 == 'C':
            q006 = 'R1'
        elif q006 == 'D' or q006 == 'E' or q006 == 'F' or q006 == 'G':
            q006 = 'R2'
        else:
            q006 = 'R3'

        if q024 == 'A':
            q024 = 'N'
        else:
            q024 = 'Y'

        if q026 == 'A' or q026 == 'B':
            q026 = 'Y'
        else:
            q026 = 'N'

        if q027 == 'A' or q027 == 'B' or q027 == 'C' or q027 == 'D' or q027 == 'E':
            q027 = 'AR'
        else:
            q027 = 'SR'

        if q047 == 'A' or q047 == 'B':
            q047 = 'Pub'
        else:
            q047 = 'Pri'

        x = []
        x.append(inscricao)
        x.append(nu_nota_lc)
        x.append(tp_sexo)
        x.append(1 if tp_escola == 2 else 0)
        x.append(in_treineiro)
        x.append(co_prova_mt)
        x.append(q001)
        x.append(q002)
        x.append(q006)
        x.append(q024)
        x.append(q025)
        x.append(q026)
        x.append(q027)
        x.append(q047)
        for r in tx_respostas_mt:
            x.append(resp2code(r))

        X.append(x)
        N += 1
    X = np.array(X)
    return X, nfactors


np.random.seed(17)
X, Y, X_nfactors = get_data()
to_pred, to_pred_nfactors = get_test()

h2o.init()
predictions = {}

for i in range(Y.shape[1]):
    Y_i = Y[:, i]

    x = h2o.H2OFrame(X)

    col_x = []
    n = 1
    for col in x.columns:
        col_x.append('C'+str(n))
        n += 1
    x.set_names(col_x)

    n = len(col_x)
    for col in col_x:
        n -= 1
        if n >= X_nfactors:
            continue
        x[col] = x[col].asfactor()

    y = h2o.H2OFrame(Y_i)
    col_y = 'resposta'
    y.set_names([col_y])

    df = x.cbind(y)
    mask = df[col_y] != 0
    df = df[mask]

    df[col_y] = df[col_y].asfactor()

    train, valid, test = df.split_frame([0.75, 0.15], seed=212)

    print(i, df.nrows)

    aml = H2OAutoML(max_runtime_secs=120)
    aml.train(x=col_x, y=col_y,
              training_frame=train,
              validation_frame=valid,
              leaderboard_frame=test)

    lb = aml.leaderboard
    print(lb)

    #preds = aml.leader.predict(test)
    #print(preds)

    col_y = ['inscricao']+col_x
    pred_x = h2o.H2OFrame(to_pred)
    pred_x.set_names(col_y)

    n = len(col_y)
    for col in col_y:
        n -= 1
        if n >= to_pred_nfactors:
            continue
        pred_x[col] = pred_x[col].asfactor()

    pred = aml.leader.predict(pred_x)
    #pred = pred.cbind(pred_x['inscricao'])
    #print(pred)

    inscricoes = pred_x['inscricao'].as_data_frame().values
    predicoes = pred['predict'].as_data_frame().values

    for inscricao, p in zip(inscricoes, predicoes):
        inscricao = inscricao[0]
        p = p[0]

        #print(inscricao, p)

        if inscricao not in predictions:
            predictions[inscricao] = []
        predictions[inscricao].append(code2resp(p))

    print('----------------')


pred_output = []

for inscricao, resposta in predictions.items():
    curr_pred = {}
    curr_pred['NU_INSCRICAO'] = inscricao
    curr_pred['TX_RESPOSTAS_MT'] = ''.join(resposta)

    pred_output.append(curr_pred)


saida = {}
saida['token'] = ''
saida['email'] = ''
saida['answer'] = pred_output

#print(json.dumps(saida, indent=2))

with open('saida.json', 'w') as f:
    json.dump(saida, f, indent=2)
