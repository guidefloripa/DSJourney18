# author: Guilherme Steinmann

train = read.csv('train.csv')
test = read.csv('test2.csv')

train1 = train[, colnames(train) %in% c(colnames(test), 'NU_NOTA_MT')]
train1 = subset(train1, is.na(NU_NOTA_MT)==FALSE)
train1 = subset(train1, NU_NOTA_LC>0)

train1$TP_COR_RACA = as.factor(train1$TP_COR_RACA)
test$TP_COR_RACA = as.factor(test$TP_COR_RACA)

train1$TP_NACIONALIDADE = as.factor(train1$TP_NACIONALIDADE)
test$TP_NACIONALIDADE = as.factor(test$TP_NACIONALIDADE)

train1$TP_ST_CONCLUSAO = as.factor(train1$TP_ST_CONCLUSAO)
test$TP_ST_CONCLUSAO = as.factor(test$TP_ST_CONCLUSAO)

train1$TP_ESCOLA = as.factor(train1$TP_ESCOLA)
test$TP_ESCOLA = as.factor(test$TP_ESCOLA)

train1$IN_TREINEIRO = as.factor(train1$IN_TREINEIRO)
test$IN_TREINEIRO = as.factor(test$IN_TREINEIRO)

train1$TP_LINGUA = as.factor(train1$TP_LINGUA)
test$TP_LINGUA = as.factor(test$TP_LINGUA)

train1$IN_BAIXA_VISAO = as.factor(train1$IN_BAIXA_VISAO)
test$IN_BAIXA_VISAO = as.factor(test$IN_BAIXA_VISAO)

train1$IN_CEGUEIRA = as.factor(train1$IN_CEGUEIRA)
test$IN_CEGUEIRA = as.factor(test$IN_CEGUEIRA)

train1$IN_SURDEZ = as.factor(train1$IN_SURDEZ)
test$IN_SURDEZ = as.factor(test$IN_SURDEZ)

train1$IN_DISLEXIA = as.factor(train1$IN_DISLEXIA)
test$IN_DISLEXIA = as.factor(test$IN_DISLEXIA)

train1$IN_SABATISTA = as.factor(train1$IN_SABATISTA)
test$IN_SABATISTA = as.factor(test$IN_SABATISTA)

train1$IN_GESTANTE = as.factor(train1$IN_GESTANTE)
test$IN_GESTANTE = as.factor(test$IN_GESTANTE)

train1$IN_IDOSO = as.factor(train1$IN_IDOSO)
test$IN_IDOSO = as.factor(test$IN_IDOSO)

train1$TP_PRESENCA_LC = as.factor(train1$TP_PRESENCA_LC)
test$TP_PRESENCA_LC = as.factor(test$TP_PRESENCA_LC)

train1$TP_PRESENCA_CH = as.factor(train1$TP_PRESENCA_CH)
test$TP_PRESENCA_CH = as.factor(test$TP_PRESENCA_CH)

train1$TP_PRESENCA_CN = as.factor(train1$TP_PRESENCA_CN)
test$TP_PRESENCA_CN = as.factor(test$TP_PRESENCA_CN)

train1$TP_STATUS_REDACAO = as.factor(train1$TP_STATUS_REDACAO)
test$TP_STATUS_REDACAO = as.factor(test$TP_STATUS_REDACAO)

train1$CAT_TP_ESCOLA_2 = train1$TP_ESCOLA == "2"
test$CAT_TP_ESCOLA_2 = test$TP_ESCOLA == "2"

train1_mat = subset(train1, NU_NOTA_MT > 0)

pred1 = lm(NU_NOTA_MT ~ TP_SEXO + CAT_TP_ESCOLA_2 + IN_TREINEIRO + IN_SABATISTA + NU_NOTA_CN + NU_NOTA_CH + NU_NOTA_LC + TP_LINGUA + NU_NOTA_REDACAO + Q006 + Q024 + Q025 + Q026 + Q047, data=train1_mat)
test$pred1 = predict(pred1,newdata=test)

pred2 = lm(NU_NOTA_MT ~ TP_SEXO + CAT_TP_ESCOLA_2 + IN_TREINEIRO + IN_SABATISTA + NU_NOTA_LC + TP_LINGUA + NU_NOTA_COMP1 + NU_NOTA_REDACAO + Q006 + Q024 + Q025 + Q026 + Q047, data=train1_mat)
test$pred2 = predict(pred2,newdata=test)

for (i in 1:nrow(test)) { if ((is.na(test$NU_NOTA_LC[i])==FALSE)&(test$NU_NOTA_LC[i]<=0)){test$pred2[i] = 0} }

test$NU_NOTA_MT = test$pred1
for (i in 1:nrow(test)) { if (is.na(test$NU_NOTA_MT[i])){test$NU_NOTA_MT[i] = test$pred2[i]} }
for (i in 1:nrow(test)) { if ((is.na(test$pred1[i])==FALSE)&(test$NU_NOTA_CN[i]<=0)){test$NU_NOTA_MT[i] = test$pred2[i]} }

res = test[,c("NU_INSCRICAO","NU_NOTA_MT")]
write.csv(res, file="res_p2.csv", row.names=FALSE)

#train_residuals = subset(train1_mat, NU_NOTA_CN > 0)
#train_residuals = subset(train_residuals, NU_NOTA_CH > 0)
#train_residuals$res = pred1$residuals
#train_residuals$resbool = abs(pred1$residuals) > 250
#residuals = subset(train_residuals, resbool==TRUE)
#residuals$predict = predict(pred1, newdata=residuals)

