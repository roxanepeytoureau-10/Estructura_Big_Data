# Estructura_Big_Data
Construccion de un cluster Hadoop, analisis usando Spark API y visualisacion de los resultados.

At build you may have to first call : 
docker build -t my-hadoop:3.4.1 -f Dockerfile.hadoop .

then :
docker compose run --rm master hdfs namenode -format -force
so that the hdfs namenode is formatted and still retains its memory

docker compose up
you can then check the localhost:8088 to ensure all is running correctly


then execute : 
docker exec -it hadoop-client bash
try : 
hdfs dfs -ls /input

if Superstore.csv appears all is good.

otherwise :
hdfs dfs -mkdir -p /input
hdfs dfs -put /tmp/data/Superstore.csv /input/

and recheck: 
hdfs dfs -ls /input

Everything should now be ready.