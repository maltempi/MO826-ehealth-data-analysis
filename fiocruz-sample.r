#This sample may be found here:
#https://www.youtube.com/watch?time_continue=5&v=MLdDROFQNuw
# This script shows data from this index:
# http://www.proadess.icict.fiocruz.br/index.php?pag=fic&cod=M05&tab=1

# Mortalidade proporcional por doença diarreica aguda em menores de 5 anos

library("elastic")
connect(es_host = "elasticsearch.icict.fiocruz.br", 
        es_port = 8201, 
        es_user = "r_user", 
        es_pwd = "r_user",
        es_transport_schema = "https")

q<-'{"size":0,
      "query":{
        "filtered":{
              "query":{
                "wildcard": {"CAUSABAS":"A0??"}
            }, 
            "filter":{
              "range":{
                "idade_obito":{
                  "from":0,
                  "to":5
                }
              }
            }
          }
          }, "aggs":{
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
  
  
  q<-'{"size":0,
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
      }
    }'
  
  denominador<-Search(index = "datasus-sim", body = q, asdf = TRUE, size = 0);
    
  q<-'{"size":0,
        "query":{
          "filtered":{
            "query":{
              "wildcard": {"CAUSABAS":"R0??"}
            }, 
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

mal_definidas<-Search(index = "datasus-sim", body = q, asdf = TRUE, size = 0)
  
denominador <- unlist(denominador$aggregations$ano$buckets$doc_count) - unlist(mal_definidas$aggregations$ano$buckets$doc_count)  
  
tempo<-unlist(numerador$aggregations$ano$buckets$key)

tempo  

valor_n <- unlist(numerador$aggregations$ano$buckets$doc_count)  
  
dda<-(valor_n/denominador)*100  
  
base<-data.frame(tempo, dda)

require(ggplot2)  

p <- ggplot(base, aes(tempo, dda))+geom_point()
p
  
p1 <- p + geom_smooth(method = lm)
p1
 
valor_n<-unlist(numerador$aggregations$ano$buckets$doc_count)

valor_d<-unlist(denominador$aggregations$ano$buckets$doc_count)
  
dda<-(valor_n/valor_d)*1000

  
require(ggplot2)
  
base<-data.frame(tempo, dda)
  
p<-ggplot(base, aes(x=tempo, y=dda)) + geom_point()
  
p
  
  
p1<-p + geom_smooth(method = lm)
p1
