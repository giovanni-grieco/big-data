#!/bin/bash

# Default to local mode
MODE="local"

# Parse arguments
for arg in "$@"; do
    case $arg in
        --local)
            MODE="local"
            ;;
        --remote)
            MODE="remote"
            ;;
        *)
            VERSION="$arg"
            ;;
    esac
done

if [ -z "$VERSION" ]; then
    VERSION="3.4.1"
fi

# ...existing code for Java, wget, tar checks, Hadoop/Hive download/extract...

# Set environment variables
export HADOOP_HOME="$HOME/hadoop-$VERSION"
export HIVE_HOME="$HOME/hive"

#check if PATH already has HADOOP_HOME/bin
if [[ ":$PATH:" != *":$HADOOP_HOME/bin:"* ]]; then
    export PATH="$HADOOP_HOME/bin:$PATH"
fi

if [[ ":$PATH" != *":$HIVE_HOME/bin:"* ]]; then
    export PATH="$HIVE_HOME/bin:$PATH"
fi
echo "Environment variables are set."
echo "HADOOP_HOME is set to $HADOOP_HOME"

echo "Checking hadoop-streaming"
if [ ! -f "$HADOOP_HOME/streaming/hadoop-streaming.jar" ]; then
    echo "Hadoop streaming jar not found. Please check your Hadoop installation."
    echo "Downloading hadoop-streaming.jar..."
    wget "https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-streaming/3.3.1/hadoop-streaming-3.3.1.jar"
    if [ $? -ne 0 ]; then
        echo "Failed to download hadoop-streaming.jar"
        exit 1
    fi
    mkdir -p "$HADOOP_HOME/streaming/"
    mv "hadoop-streaming-3.3.1.jar" "$HADOOP_HOME/streaming/hadoop-streaming.jar"
else
    echo "Hadoop streaming jar already exists."
fi

if [ "$MODE" = "local" ]; then
    # ask if $home/hdfs wants to be wiped
    read -p "Do you want to wipe the $HOME/hdfs directory? (y/n): " wipe_hdfs
    if [[ $wipe_hdfs == "y" || $wipe_hdfs == "Y" ]]; then
        echo "Wiping $HOME/hdfs directory..."
        rm -rf "$HOME/hdfs"
    else
        echo "Not wiping $HOME/hdfs directory."
    fi

    # Create necessary directories
    NAMENODE_DIR="$HOME/hdfs/namenode"
    DATANODE_DIR="$HOME/hdfs/datanode"
    MAPRED_LOCAL_DIR="$HOME/hdfs/mapred"

    mkdir -p "$NAMENODE_DIR"
    mkdir -p "$DATANODE_DIR"
    mkdir -p "$MAPRED_LOCAL_DIR"
fi


# ========= CORE-SITE.XML =========
CACHE_DIR="./.setup-cache"
CACHE_FILE="$CACHE_DIR/emr_master_dns"

mkdir -p "$CACHE_DIR"

if [ "$MODE" = "local" ]; then
    # ...existing local setup code...
    cat <<EOL > "$HADOOP_HOME/etc/hadoop/core-site.xml"
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://localhost:9000</value>
    </property>
</configuration>
EOL
else
    # Check for cached EMR master DNS
    if [ -f "$CACHE_FILE" ]; then
        OLD_EMR_MASTER=$(cat "$CACHE_FILE")
        read -p "Reuse last EMR master DNS ($OLD_EMR_MASTER)? [Y/n]: " reuse_dns
        if [[ "$reuse_dns" =~ ^[Nn]$ ]]; then
            read -p "Enter your EMR master node DNS (e.g., ec2-xx-xx-xx-xx.compute-1.amazonaws.com): " EMR_MASTER
            echo "$EMR_MASTER" > "$CACHE_FILE"
        else
            EMR_MASTER="$OLD_EMR_MASTER"
        fi
    else
        read -p "Enter your EMR master node DNS (e.g., ec2-xx-xx-xx-xx.compute-1.amazonaws.com): " EMR_MASTER
        echo "$EMR_MASTER" > "$CACHE_FILE"
    fi

    cat <<EOL > "$HADOOP_HOME/etc/hadoop/core-site.xml"
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://$EMR_MASTER:8020</value>
    </property>
</configuration>
EOL
fi
echo "HADOOP core-site.xml config done"

# ========= HDFS-SITE.XML =========

if [ "$MODE" = "local" ]; then
    cat <<EOL > "$HADOOP_HOME/etc/hadoop/hdfs-site.xml"
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <property>
        <name>dfs.replication</name>
        <value>1</value>
    </property>
    <property>
        <name>dfs.namenode.name.dir</name>
        <value>file://$NAMENODE_DIR</value>
    </property>
    <property>
        <name>dfs.datanode.data.dir</name>
        <value>file://$DATANODE_DIR</value>
    </property>
</configuration>
EOL

    echo "HADOOP hdfs-site.xml config done"

    cat <<EOL > "$HADOOP_HOME/etc/hadoop/mapred-site.xml"
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <property>
        <name>mapreduce.cluster.local.dir</name>
        <value>file://$MAPRED_LOCAL_DIR</value>
    </property>
    <property>
        <name>mapreduce.framework.name</name>
        <value>local</value>
    </property>
</configuration>
EOL

echo "HADOOP mapred-site.xml config done"

echo "HADOOP config done"

echo "Configuring Hive"

cp "$HIVE_HOME/conf/hive-env.sh.template" "$HIVE_HOME/conf/hive-env.sh"

cat <<EOL >> "$HIVE_HOME/conf/hive-env.sh"
HADOOP_HOME=$HADOOP_HOME
export HIVE_CONF_DIR=$HIVE_HOME
export JAVA_HOME=$JAVA_HOME
EOL

echo "HIVE config done"

if [ "$MODE" = "local" ]; then
    hdfs namenode -format
fi

#Ask user if they want to wipe the metastore_db folder
if [ "$MODE" = "local" ]; then
    echo "Checking for metastore_db folder..."
    if [ -d "metastore_db/" ]; then
        read -p "Do you want to wipe the metastore_db folder? (y/n): " wipe_metastore
        if [[ $wipe_metastore == "y" || $wipe_metastore == "Y" ]]; then
            echo "Wiping metastore_db folder..."
            rm -rf "metastore_db/"
            schematool -dbType derby -initSchema
        else
            echo "Not wiping metastore_db folder."
        fi
    else
        echo "metastore_db folder not found. Initializing schema..."
        schematool -dbType derby -initSchema
    fi
fi

#Check if .venv exists, if not, create it and install requirements
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
else
    echo "Virtual environment already exists."
    source .venv/bin/activate
fi

echo "All done!"

echo "!!! To deactivate the virtual environment, run: deactivate !!!"