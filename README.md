# Estructura_Big_Data
Construccion de un cluster Hadoop, analisis usando Spark API y visualisacion de los resultados.


docker compose run --rm master hdfs namenode -format -force

hdfs dfs -mkdir -p /input
hdfs dfs -put /tmp/data/Superstore.csv /input/
hdfs dfs -ls /input