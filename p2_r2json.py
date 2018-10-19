#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Guilherme Steinmann

import json
import pandas as pd

df = pd.read_csv('res_p2.csv')

pred_output = []
for index, row in df.iterrows():
    inscricao = row['NU_INSCRICAO']
    nota = row['NU_NOTA_MT']

    if pd.isna(nota):
        nota = 0.0

    curr_pred = {}
    curr_pred['NU_INSCRICAO'] = inscricao
    curr_pred['NU_NOTA_MT'] = nota
    pred_output.append(curr_pred)


saida = {}
saida['token'] = ''
saida['email'] = ''
saida['answer'] = pred_output

print(json.dumps(saida, indent=2))

with open('saida2.json', 'w') as f:
    json.dump(saida, f, indent=2)
