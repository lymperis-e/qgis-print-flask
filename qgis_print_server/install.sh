sudo apt install gnupg software-properties-common

# Add QGIS repository key
wget -qO - https://qgis.org/downloads/qgis-2020.gpg.key | sudo gpg --no-default-keyring --keyring gnupg-ring:/etc/apt/trusted.gpg.d/qgis-archive.gpg --import
sudo chmod a+r /etc/apt/trusted.gpg.d/qgis-archive.gpg
gpg --fingerprint 51F523511C7028C3

# Add QGIS repository to sources list
sudo add-apt-repository "deb https://qgis.org/debian lsb_release -c -s main"


# Update package list and install QGIS
sudo apt update
sudo apt install qgis python3-qgis qgis-plugin-grass


sudo apt-get install python3-pyqt5
pip3 install PyQt5

# Set environment variables for QGIS
echo 'export QGIS_PREFIX_PATH="/usr"' | sudo tee -a /etc/environment
echo 'export PYTHONPATH=$QGIS_PREFIX_PATH/share/qgis/python' | sudo tee -a /etc/environment
echo 'export LD_LIBRARY_PATH=$QGIS_PREFIX_PATH/lib' | sudo tee -a /etc/environment

# Reload the environment variables
source /etc/environment


# Test the installation
python3 -c "from qgis.core import QgsApplication; QgsApplication.showSettings()"
