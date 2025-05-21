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