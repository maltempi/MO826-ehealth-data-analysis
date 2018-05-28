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

# size: 0 -> unlimited entries
queryMortality <- '{
  "query": {
    "filtered": {
      "query": {
        "query_string": {
          "analyze_wildcard": true,
          "query": "*"
        }
      },
      "filter": {
        "bool": {
          "must": [
            {
              "$state": {
                "store": "globalState"
              },
              "range": {
                "idade_obito": {
                  "gte": 0,
                  "lt": 5
                }
              }
            }
          ],
          "must_not": []
        }
      }
    }
  },
  "size": 0,
  "aggs": {
    "2": {
      "terms": {
        "field": "res_nome_municipio",
        "size": 0,
        "order": {
          "_term": "asc"
        }
      },
      "aggs": {
        "3": {
          "terms": {
            "field": "ano_obito",
            "size": 0,
            "order": {
              "_count": "desc"
            }
          },
          "aggs": {
            "4": {
              "terms": {
                "field": "idade_obito",
                "size": 0,
                "order": {
                  "_count": "desc"
                }
              }
            }
          }
        }
      }
    }
  }
}'

data<-Search(index = "datasus-sim", body = queryMortality, asdf = TRUE, size = 0)

print(data)

