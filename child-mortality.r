# http://www.proadess.icict.fiocruz.br/index.php?pag=fic&cod=M01&tab=1
# https://bigdata.icict.fiocruz.br/sites/bigdata.icict.fiocruz.br/files//SINASC-DicionarioVariaveis.pdf
library("elastic")

connect(
  es_host = "elasticsearch.icict.fiocruz.br",
  es_port = 8201,
  es_user = "r_user",
  es_pwd = "r_user",
  es_transport_schema = "https"
)

# Range de 0 a 5 anos
# size: 0 -> sem restricao de numero de resultados
# Agrupado por ano de obito
# Ordenado por anos de forma asc
queryMortality <- '{"size":0,
"query":{
"filtered":{
  "filter":{
    "range":{
      "idade_obito":{
        "from":0,
        "to":5
      }
    }
  }
}
}, 
"aggs":{
  "ano":{
    "terms":{
      "field":"ano_obito",
      "size":0,
      "order":{
        "_term":"asc"
      }
    }
  }
}}'

numerador<-Search(index = "datasus-sim", body = q, asdf = TRUE, size = 0)

print(numerador)