# Estructura_Big_Data
Construccion de un cluster Hadoop, analisis usando Spark API y visualisacion de los resultados.


### Comandos de incialiacion del cluster
First install this spark version in the cloned repository (it will take a long time): 
`wget https://archive.apache.org/dist/spark/spark-3.4.2/spark-3.4.2-bin-hadoop3.tgz`

At build you have to first call : 
`docker build -t my-hadoop-spark:3.4.1 -f Dockerfile.hadoop .`
`docker compose run --rm master hdfs namenode -format -force`
so that the hdfs namenode is formatted and still retains its memory

`docker compose up`
You can then check the localhost:8088 and localhost:9870 to ensure all is running correctly.
Then execute : 
`docker exec -it hadoop-client bash`

Try : 
`hdfs dfs -ls /input`

If Superstore.csv appears all is good. Otherwise :
`hdfs dfs -mkdir -p /input`
`hdfs dfs -put /tmp/data/Superstore.csv /input/`

And recheck: 
`hdfs dfs -ls /input`
Everything should now be ready.