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

# Extract the downloaded tarball
tar -xzf "hadoop-$VERSION.tar.gz"
#check if the extraction was successful
if [ $? -ne 0 ]; then
    echo "Failed to extract Hadoop version $VERSION"
    exit 1
fi

# Move the extracted directory to the desired location
mv "hadoop-$VERSION" "$HOME/hadoop-$VERSION"
#check if the move was successful
if [ $? -ne 0 ]; then
    echo "Failed to move Hadoop version $VERSION to $HOME"
    exit 1
fi

# Set environment variables
export HADOOP_BASE="$HOME/hadoop-$VERSION"
export PATH="$HADOOP_BASE/bin:$PATH"
