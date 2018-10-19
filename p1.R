# author: Guilherme Steinmann

data = read.csv("train.csv")

x1 = c("NU_INSCRICAO", "NU_NOTA_MT", "NU_NOTA_CN", "NU_NOTA_LC", "NU_NOTA_CH", "NU_NOTA_REDACAO")
data1 = data[,x1]
data1$NU_NOTA_FINAL = (data1$NU_NOTA_MT*3 + data1$NU_NOTA_CN*2 + data1$NU_NOTA_LC*1.5 + data1$NU_NOTA_CH + data1$NU_NOTA_REDACAO*3) / 10.5

#order(data1$NU_NOTA_FINAL, decreasing = TRUE)[1:20]
#sort(data1$NU_NOTA_FINAL,decreasing = TRUE)[1:20]

max_score = subset(data1, data1$NU_NOTA_FINAL >= 807.319)
res = max_score[order(max_score$NU_NOTA_FINAL,decreasing=TRUE),c("NU_INSCRICAO","NU_NOTA_FINAL")]

write.csv(res, file="res_p1.csv", row.names=FALSE)
