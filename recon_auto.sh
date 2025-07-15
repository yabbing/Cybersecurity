#!/bin/bash

read -p "Enter target IP: " target_ip
read -p "Enter output filename: " output_file

echo "Running nmap..."
nmap -sC -sV -A --disable-arp-ping "$target_ip" > "$output_file"

echo -e "\n\nRustscan Results:" >> "$output_file"
rustscan -a "$target_ip" >> "$output_file"

echo "Results saved to $output_file"