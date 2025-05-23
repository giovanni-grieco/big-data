#!/bin/bash
# as argument, specify version. Default is 3.4.1
# Example: ./setup.sh 3.4.1
# Check if a version argument is provided
if [ -z "$1" ]; then
    VERSION="3.4.1"
else
    VERSION="$1"
fi

#check for java 11
if ! java --version 2>&1 | grep -q "11"; then
    echo "Java 11 is required. Please install Java 11 and try again."
    echo "Visit https://cwiki.apache.org/confluence/display/HADOOP/Hadoop+Java+Versions for more information."
    echo "Make sure to set JAVA_HOME environment variable to point to your Java 11 installation."
    echo "You can set JAVA_HOME in your ~/.bashrc or ~/.bash_profile file."
    echo "For example, add the following line to your ~/.bashrc or ~/.bash_profile:"
    echo "export JAVA_HOME=/path/to/your/java11"
    echo "Then, run 'source ~/.bashrc' or 'source ~/.bash_profile' to apply the changes."
    exit 1
fi
# Check if wget is installed
if ! command -v wget &> /dev/null; then
    echo "wget could not be found. Please install wget and try again."
    exit 1
fi
# Check if tar is installed
if ! command -v tar &> /dev/null; then
    echo "tar could not be found. Please install tar and try again."
    exit 1
fi

#check if hadoop has already been downloaded
#if not, then download, otherwise avoid redownloading

if [ -d "$HOME/hadoop-$VERSION" ]; then
    echo "Hadoop version $VERSION already in $HOME."
else
    echo "Hadoop not found in $HOME"
    if [ ! -f "hadoop-$VERSION.tar.gz" ]; then
        # Download Hadoop
        wget "https://archive.apache.org/dist/hadoop/common/hadoop-$VERSION/hadoop-$VERSION.tar.gz"
        #check if the download was successful
        if [ $? -ne 0 ]; then
            echo "Failed to download Hadoop version $VERSION"
            exit 1
        fi
    else
        echo "Hadoop version $VERSION already downloaded."
    fi

    echo "Don't delete the hadoop-$VERSION.tar.gz, as it contains the hadoop tarball."
    echo "The download will remain cached in this directory."


    # Check if the tarball was already extracted, if the directory exists
    if [ -d "$HOME/hadoop-$VERSION" ]; then
        echo "Hadoop version $VERSION is already extracted."
    else
        echo "Extracting hadoop from tarball..."
        # Extract the tarball
        tar -xzf "hadoop-$VERSION.tar.gz"
        #check if the extraction was successful
        if [ $? -ne 0 ]; then
            echo "Failed to extract Hadoop version $VERSION"
            exit 1
        fi
    fi
    # Check if the extracted directory already exists in $HOME
    if [ -d "$HOME/hadoop-$VERSION" ]; then
        echo "Hadoop version $VERSION is already in $HOME."
    else
        # Move the extracted directory to $HOME
        mv "hadoop-$VERSION" "$HOME"
    fi
fi


if [ ! -d "$HOME/hive" ]; then
    echo "Hive not found in $HOME/hive"
    #check if targz file already exists
    hive_archive_file_name="apache-hive-2.3.9-bin.tar.gz"
    if [ ! -f "$hive_archive_file_name" ]; then
        # Download Hive
        wget "https://archive.apache.org/dist/hive/hive-2.3.9/apache-hive-2.3.9-bin.tar.gz"
        #check if the download was successful
        if [ $? -ne 0 ]; then
            echo "Failed to download Hive version 2.3.9"
            exit 1
        fi
    else
        echo "Hive version 2.3.9 already downloaded."
    fi
    # Check if the tarball was already extracted, if the directory exists
    if [ -d "$HOME/hive" ]; then
        echo "Hive version 2.3.9 is already extracted."
    else
        echo "Extracting hive from tarball..."
        # Extract the tarball
        tar -xzf "$hive_archive_file_name"
        #check if the extraction was successful
        if [ $? -ne 0 ]; then
            echo "Failed to extract Hive version 2.3.9"
            exit 1
        fi
    fi
    # Check if the extracted directory already exists in $HOME
    if [ -d "$HOME/hive" ]; then
        echo "Hive version 2.3.9 is already in $HOME."
    else
        # Move the extracted directory to $HOME
        mv "apache-hive-2.3.9-bin" "$HOME/hive"
        rm $HIVE_HOME/lib/guava-14.0.1.jar
        cp $HADOOP_HOME/share/hadoop/common/lib/guava-27.0-jre.jar $HIVE_HOME/lib/
    fi
else
    echo "Hive version 2.3.9 already in $HOME."
fi

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
    #check if the download was successful
    if [ $? -ne 0 ]; then
        echo "Failed to download hadoop-streaming.jar"
        exit 1
    fi
    # Move the jar to the streaming directory
    mkdir -p "$HADOOP_HOME/streaming/"
    mv "hadoop-streaming-3.3.1.jar" "$HADOOP_HOME/streaming/hadoop-streaming.jar"
else
    echo "Hadoop streaming jar already exists."
fi




echo "Configuring Hadoop core-site.xml"

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

cat <<EOL > "$HADOOP_HOME/etc/hadoop/hdfs-site.xml"
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
    <property>
        <name>dfs.replication</name>
        <value>1</value>
    </property>
</configuration>
EOL
echo "HADOOP config done"

echo "Configuring Hive"
cp "$HIVE_HOME/conf/hive-env.sh.template" "$HIVE_HOME/conf/hive-env.sh"

cat <<EOL >> "$HIVE_HOME/conf/hive-env.sh"
HADOOP_HOME=$HADOOP_HOME
export HIVE_CONF_DIR=$HIVE_HOME
export JAVA_HOME=$JAVA_HOME
EOL

echo "HIVE config done"

hdfs namenode -format


#Ask user if they want to wipe the metastore_db folder
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