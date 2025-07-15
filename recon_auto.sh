#!/bin/bash

read -p "Enter target IP: " target_ip
read -p "Enter folder name for output: " folder_name
read -p "Enter domain name for /etc/hosts (e.g., example.local): " domain_name

# Create output folder
mkdir -p "$folder_name"

nmap_file="${folder_name}/${folder_name}_nmap"
rustscan_file="${folder_name}/${folder_name}_rustscan"
feroxbuster_file="${folder_name}/${folder_name}_feroxbuster"

echo "Running nmap..."
nmap -sC -sV -A --disable-arp-ping "$target_ip" > "$nmap_file"

echo "Running rustscan..."
rustscan -a "$target_ip" > "$rustscan_file"

# Check if port 80 is open
if nmap "$target_ip" -p 80 | grep -q "80/tcp open"; then
    echo "Port 80 is open. Checking for website..." | tee -a "$nmap_file"
    # Try to get website title
    website_title=$(curl -s http://"$target_ip" | grep -oP '(?<=<title>).*?(?=</title>)')
    if [ -n "$website_title" ]; then
        echo "Website found: $website_title" | tee -a "$nmap_file"
        echo "Domain name to add to /etc/hosts: $target_ip $domain_name" | tee -a "$nmap_file"
        echo "Running feroxbuster on http://$domain_name"
        feroxbuster -u "http://$domain_name" | tee -a "$feroxbuster_file"
    else
        echo "No website detected on port 80." | tee -a "$nmap_file"
    fi
else
    echo "Port 80 is closed." | tee -a "$nmap_file"
fi

echo "Results saved in folder: $folder_name"
echo "  Nmap: $nmap_file"
echo "  Rustscan: $rustscan_file"
echo "  Feroxbuster: $feroxbuster_file (if applicable)"