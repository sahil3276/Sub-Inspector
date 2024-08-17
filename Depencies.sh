#!/bin/bash

# Function to check if a package is installed
is_package_installed() {
    dpkg -s "$1" &> /dev/null
}

# Function to check if a Go-based tool is installed
is_tool_installed() {
    command -v "$1" &> /dev/null
}

# Function to install a package if it's not already installed
install_package() {
    if ! is_package_installed "$1"; then
        echo "Installing $1..."
        sudo apt install -y "$1" > /dev/null 2>&1
    else
        echo "$1 is already installed."
    fi
}

# Function to install a Go-based tool if it's not already installed
install_tool() {
    if ! is_tool_installed "$1"; then
        echo "Installing $1..."
        go install -v "$2" > /dev/null 2>&1
        echo "$1 installed."
    else
        echo "$1 is already installed."
    fi
}

# Check and install additional tools
echo "Checking and installing required packages..."
install_package sublist3r

# Install Python dependencies
pip install requests dnspython > /dev/null 2>&1
echo "Python dependencies installed."

# Check and install Go-based tools
if is_tool_installed go; then
    install_tool subfinder github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
    install_tool assetfinder github.com/tomnomnom/assetfinder@latest
    install_tool notify github.com/projectdiscovery/notify/cmd/notify@latest
    install_tool amass github.com/owasp-amass/amass/v4/...@master
else
    echo "Go is not installed. Please install Go before running this script."
    echo -e "\e[1;32m1. https://medium.com/@prathameshbagul/solving-the-package-crypto-ecdh-is-not-in-goroot-error-in-linux-quick-and-easy-fix-e6a0211c6354" 
    exit 1
fi

echo -e "\e[1;32mAll required packages are installed.\e[0m"
echo ""
echo ""

# Highlighted instructions for additional setup
# --------------------------------------------------------------
echo -e "\e[1;31mIMPORTANT\e[0m"
echo -e "\e[1;33mRefer my Write-up For Full Amass Configuration.!\e[0m"
echo -e "\e[1;32m1. https://sahil3276.medium.com/unlocking-the-full-potential-of-amass-part-1-0521ddbee8cc" 
echo -e "2. https://sahil3276.medium.com/unlocking-the-full-potential-of-amass-part-2-292b7fab6618\e[0m"
echo -e ""

# --------------------------------------------------------------

echo -e "\e[1;32mSetup complete! All tools and dependencies are installed.\e[0m"
