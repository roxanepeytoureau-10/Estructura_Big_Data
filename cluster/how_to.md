### Installs

sudo apt install openjdk-11-jdk
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH


wget https://archive.apache.org/dist/spark/spark-3.4.2/spark-3.4.2-bin-hadoop3.tgz
wget https://downloads.apache.org/hadoop/common/hadoop-3.4.1/hadoop-3.4.1.tar.gz

sudo tar -xzf hadoop-3.4.1.tar.gz -C /opt/
sudo mv /opt/hadoop-3.4.1 /opt/Hadoop
sudo chown -R $USER:$USER /opt/Hadoop
ls -l /opt/Hadoop

sudo tar -xzf spark-3.4.2-bin-hadoop3.tgz -C /opt/
sudo mv /opt/spark-3.4.2-bin-hadoop3 /opt/spark
ls -l /opt/spark

export HADOOP_HOME=/opt/hadoop
export SPARK_HOME=/opt/spark
export PATH=$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$SPARK_HOME/bin:$PATH
echo $HADOOP_HOME

source ~/.bashrc

sudo apt update
sudo apt install openssh-server -y

ssh localhost
yes



### Config
sudo nano /etc/hosts
127.0.0.1   master
127.0.0.1   worker1
127.0.0.1   worker2
127.0.0.1   worker3

nano /opt/hadoop/etc/hadoop/workers
worker1
worker2
worker3


file:///home/lyroxyy/BigData/cluster/master/name

in :   
nano $HADOOP_HOME/etc/hadoop/core-site.xml
write : 
<configuration>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://localhost:9000</value>
    </property>
</configuration>

in :   
nano $HADOOP_HOME/etc/hadoop/hdfs-site.xml
write (modifying the paths so they match yours the end should be the same): 
<configuration>
    <property>
        <name>dfs.replication</name>
        <value>3</value>
    </property>

    <property>
        <name>dfs.namenode.name.dir</name>
        <value>file:///home/lyroxyy/BigData/cluster/master/name</value>
    </property>

    <property>
        <name>dfs.datanode.data.dir</name>
        <value>file:///home/lyroxyy/BigData/cluster/worker1/data,file:///home/lyroxyy/BigData/cluster/worker2>
    </property>
</configuration>

<configuration>
<property>
    <name>yarn.resourcemanager.hostname</name>
    <value>master</value>
</property>

in :   
nano $HADOOP_HOME/etc/hadoop/yarn-site.xml
write (modifying the paths so they match yours the end should be the same): 
<property>
    <name>yarn.nodemanager.aux-services</name>
    <value>mapreduce_shuffle</value>
</property>
</configuration>



ssh-keygen -t rsa -P ""


# This part you may have to do at each restart of the system if not kept in memory
nano $HADOOP_HOME/etc/hadoop/hadoop-env.sh
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export HADOOP_HOME=/opt/hadoop
export PATH=$JAVA_HOME/bin:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$PATH
export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
hadoop version



### Starting the system 
hdfs namenode -format
start-dfs.sh
start-yarn.sh

check with jps : you should at least see (namenode, datanode, resourcemanager)

normally : http://localhost:9870/
and : http://localhost:8088/cluster/apps
should appear as active (although only with one)

(to put the data in hdfs, mind the path in the second one)
hdfs dfs -mkdir -p /data
hdfs dfs -put /home/lyroxyy/BigData/cluster/Superstore.csv /data/
hdfs dfs -ls /data
(the last one should show the csv)


check yarn with : 
spark-submit --class org.apache.spark.examples.SparkPi --master yarn --deploy-mode client $SPARK_HOME/examples/jars/spark-examples_*.jar 10
if it work the job should appear at 8088

then to ensure you can submit pyspark jobs: 
conda create -n spark310 python=3.10 -y
conda activate spark310

export PYSPARK_PYTHON=$(which python)
export PYSPARK_DRIVER_PYTHON=$(which python)
python --version

pyspark
(if it starts is okay.) 



### In notebook

create a notebook in the file
choose as a kernel the conda env spark310

then in a cell: 

import os
import sys

# Spark paths
os.environ["SPARK_HOME"] = "/opt/spark"
os.environ["HADOOP_CONF_DIR"] = "/opt/hadoop/etc/hadoop"

# Ensure kernel Python is used by PySpark
os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

# Add Spark Python directories to sys.path
sys.path.insert(0, os.path.join(os.environ["SPARK_HOME"], "python"))
sys.path.insert(0, os.path.join(os.environ["SPARK_HOME"], "python", "lib", "py4j-0.10.9.7-src.zip"))


and to test : 

from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("JupyterSpark") \
    .master("yarn") \
    .getOrCreate()

df = spark.read.csv("hdfs:///data/Superstore.csv", header=True, inferSchema=True)
df.show(5)


theoretically the job sends back the first 5 lines and should appear in your localhost:8088

### To down 
stop-dfs.sh
stop-yarn.sh