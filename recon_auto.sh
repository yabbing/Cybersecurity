#!/bin/bash

read -p "Enter target IP: " target_ip
read -p "Enter output filename: " output_file
read -p "Enter domain name for /etc/hosts (e.g., example.local): " domain_name

echo "Running nmap..."
nmap -sC -sV -A --disable-arp-ping "$target_ip" > "$output_file"

echo -e "\n\nRustscan Results:" >> "$output_file"
rustscan -a "$target_ip" >> "$output_file"

# Check if port 80 is open
if nmap "$target_ip" -p 80 | grep -q "80/tcp open"; then
    echo "Port 80 is open. Checking for website..." | tee -a "$output_file"
    # Try to get website title
    website_title=$(curl -s http://"$target_ip" | grep -oP '(?<=<title>).*?(?=</title>)')
    if [ -n "$website_title" ]; then
        echo "Website found: $website_title" | tee -a "$output_file"
        # Add to /etc/hosts
        echo "Adding $domain_name to /etc/hosts..."
        echo "$target_ip $domain_name" | sudo tee -a /etc/hosts > /dev/null
        echo "Running feroxbuster on http://$domain_name"
        feroxbuster -u "http://$domain_name" | tee -a "$output_file"
    else
        echo "No website detected on port 80." | tee -a "$output_file"
    fi
else
    echo "Port 80 is closed." | tee -a "$output_file"
fi

echo "Results saved to $output_file"