#!/bin/bash
# as argument, specify version. Default is 3.4.1
# Example: ./install_hadoop.sh 3.4.1


# Check if a version argument is provided
if [ -z "$1" ]; then
    VERSION="3.4.1"
else
    VERSION="$1"
fi

#check for java 11
if ! java --version 2>&1 | grep -q "11"; then
    echo "Java 11 is required. Please install Java 11 and try again."
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

echo "Don't delete the hadoop-$VERSION directory, as it contains the hadoop tarball."
echo "The download will remain cached in this directory."


# Check if the tarball was already extracted, if the directory exists
if [ -d "$HOME/hadoop-$VERSION" ]; then
    echo "Hadoop version $VERSION is already extracted."
else
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

# Set environment variables
export HADOOP_BASE="$HOME/hadoop-$VERSION"

#check if PATH already has HADOOP_BASE/bin
if [[ ":$PATH:" != *":$HADOOP_BASE/bin:"* ]]; then
    export PATH="$HADOOP_BASE/bin:$PATH"
fi