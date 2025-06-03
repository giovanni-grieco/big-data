#Check if .venv exists, if not, create it and install requirements
sudo -v

HADOOP_HOME="/usr/lib/hadoop"

export HADOOP_HOME
echo "Checking hadoop-streaming"
if [ ! -f "$HADOOP_HOME/streaming/hadoop-streaming.jar" ]; then
    echo "Hadoop streaming jar not found. Please check your Hadoop installation."
    echo "Downloading hadoop-streaming.jar..."
    wget "https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-streaming/3.3.1/hadoop-streaming-3.3.1.jar"
    if [ $? -ne 0 ]; then
        echo "Failed to download hadoop-streaming.jar"
        exit 1
    fi
    sudo mkdir -p "$HADOOP_HOME/streaming/"
    sudo mv "hadoop-streaming-3.3.1.jar" "$HADOOP_HOME/streaming/hadoop-streaming.jar"
else
    echo "Hadoop streaming jar already exists."
fi

if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
    source .venv/bin/activate
    pip3 install -r requirements.txt
else
    echo "Virtual environment already exists."
    source .venv/bin/activate
fi