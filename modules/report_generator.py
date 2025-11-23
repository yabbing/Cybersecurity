"""
Report generation module for JSON and HTML output
"""

import json
import os
from datetime import datetime
from typing import Dict, Any
from jinja2 import Template
import logging

# ============================================================================
# JSON REPORT GENERATION
# ============================================================================

def generate_json_report(scan_data: Dict[str, Any], output_path: str) -> bool:
    """
    Generate JSON report from scan data
    
    Args:
        scan_data: Dictionary containing all scan results
        output_path: Path to save the JSON file
        
    Returns:
        True if successful, False otherwise
    """
    logger = logging.getLogger(__name__)
    
    try:
        with open(output_path, 'w') as f:
            json.dump(scan_data, f, indent=2)
        
        logger.info(f"JSON report saved to: {output_path}")
        return True
        
    except Exception as e:
        logger.error(f"Error generating JSON report: {str(e)}")
        return False

# ============================================================================
# HTML REPORT GENERATION
# ============================================================================

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Recon Report - {{ target }}</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            color: #333;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header .subtitle {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .metadata {
            background: #f8f9fa;
            padding: 20px 30px;
            border-bottom: 2px solid #e9ecef;
        }
        
        .metadata-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
        }
        
        .metadata-item {
            display: flex;
            align-items: center;
        }
        
        .metadata-label {
            font-weight: bold;
            color: #495057;
            margin-right: 10px;
        }
        
        .metadata-value {
            color: #6c757d;
        }
        
        .content {
            padding: 30px;
        }
        
        .section {
            margin-bottom: 40px;
        }
        
        .section-title {
            font-size: 1.8em;
            color: #2a5298;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }
        
        .port-table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .port-table th {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }
        
        .port-table td {
            padding: 12px 15px;
            border-bottom: 1px solid #e9ecef;
        }
        
        .port-table tr:hover {
            background: #f8f9fa;
        }
        
        .port-number {
            font-weight: bold;
            color: #667eea;
            font-size: 1.1em;
        }
        
        .service-name {
            color: #2a5298;
            font-weight: 600;
        }
        
        .enum-section {
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            padding: 20px;
            margin: 20px 0;
            border-radius: 5px;
        }
        
        .enum-title {
            font-size: 1.3em;
            color: #2a5298;
            margin-bottom: 15px;
            font-weight: 600;
        }
        
        .enum-data {
            background: white;
            padding: 15px;
            border-radius: 5px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            white-space: pre-wrap;
            word-wrap: break-word;
            max-height: 400px;
            overflow-y: auto;
        }
        
        .badge {
            display: inline-block;
            padding: 5px 10px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
        }
        
        .badge-open {
            background: #d4edda;
            color: #155724;
        }
        
        .badge-closed {
            background: #f8d7da;
            color: #721c24;
        }
        
        .no-data {
            color: #6c757d;
            font-style: italic;
            padding: 20px;
            text-align: center;
        }
        
        .footer {
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #6c757d;
            border-top: 2px solid #e9ecef;
        }
        
        .warning-box {
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin: 20px 0;
            border-radius: 5px;
        }
        
        .warning-box strong {
            color: #856404;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 Reconnaissance Report</h1>
            <div class="subtitle">Automated Security Assessment</div>
        </div>
        
        <div class="metadata">
            <div class="metadata-grid">
                <div class="metadata-item">
                    <span class="metadata-label">Target:</span>
                    <span class="metadata-value">{{ target }}</span>
                </div>
                <div class="metadata-item">
                    <span class="metadata-label">Scan Date:</span>
                    <span class="metadata-value">{{ scan_date }}</span>
                </div>
                <div class="metadata-item">
                    <span class="metadata-label">Total Ports Scanned:</span>
                    <span class="metadata-value">{{ total_ports }}</span>
                </div>
                <div class="metadata-item">
                    <span class="metadata-label">Open Ports:</span>
                    <span class="metadata-value">{{ open_ports }}</span>
                </div>
            </div>
        </div>
        
        <div class="content">
            <div class="warning-box">
                <strong>⚠️ Legal Notice:</strong> This report contains security assessment data. 
                Ensure you have proper authorization before conducting any security testing.
            </div>
            
            <div class="section">
                <h2 class="section-title">📊 Port Scan Results</h2>
                {% if ports and ports|length > 0 %}
                <table class="port-table">
                    <thead>
                        <tr>
                            <th>Port</th>
                            <th>State</th>
                            <th>Service</th>
                            <th>Version</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for port in ports %}
                        <tr>
                            <td><span class="port-number">{{ port.port }}</span></td>
                            <td><span class="badge badge-{{ port.state }}">{{ port.state|upper }}</span></td>
                            <td><span class="service-name">{{ port.service or 'Unknown' }}</span></td>
                            <td>{{ port.version or 'N/A' }}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
                {% else %}
                <div class="no-data">No open ports detected</div>
                {% endif %}
            </div>
            
            {% if enumeration_results %}
            <div class="section">
                <h2 class="section-title">🔎 Enumeration Results</h2>
                
                {% for enum_type, enum_data in enumeration_results.items() %}
                <div class="enum-section">
                    <div class="enum-title">{{ enum_type|upper }} Enumeration</div>
                    <div class="enum-data">{{ enum_data }}</div>
                </div>
                {% endfor %}
            </div>
            {% endif %}
        </div>
        
        <div class="footer">
            <p>Generated by Recon Toolkit | {{ scan_date }}</p>
            <p style="margin-top: 10px; font-size: 0.9em;">For Ethical Hacking & CTF Competitions Only</p>
        </div>
    </div>
</body>
</html>
"""

def generate_html_report(scan_data: Dict[str, Any], output_path: str) -> bool:
    """
    Generate HTML report from scan data
    
    Args:
        scan_data: Dictionary containing all scan results
        output_path: Path to save the HTML file
        
    Returns:
        True if successful, False otherwise
    """
    logger = logging.getLogger(__name__)
    
    try:
        # Prepare template data
        template_data = {
            'target': scan_data.get('target', 'Unknown'),
            'scan_date': scan_data.get('scan_date', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            'total_ports': scan_data.get('total_ports_scanned', 0),
            'open_ports': len(scan_data.get('ports', [])),
            'ports': scan_data.get('ports', []),
            'enumeration_results': scan_data.get('enumeration_results', {})
        }
        
        # Render template
        template = Template(HTML_TEMPLATE)
        html_content = template.render(**template_data)
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"HTML report saved to: {output_path}")
        return True
        
    except Exception as e:
        logger.error(f"Error generating HTML report: {str(e)}")
        return False

# ============================================================================
# REPORT COORDINATOR
# ============================================================================

def generate_reports(scan_data: Dict[str, Any], output_dir: str, base_filename: str) -> Dict[str, str]:
    """
    Generate both JSON and HTML reports
    
    Args:
        scan_data: Dictionary containing all scan results
        output_dir: Directory to save reports
        base_filename: Base filename (without extension)
        
    Returns:
        Dictionary with paths to generated reports
    """
    logger = logging.getLogger(__name__)
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate file paths
    json_path = os.path.join(output_dir, f"{base_filename}.json")
    html_path = os.path.join(output_dir, f"{base_filename}.html")
    
    results = {}
    
    # Generate JSON report
    if generate_json_report(scan_data, json_path):
        results['json'] = json_path
    
    # Generate HTML report
    if generate_html_report(scan_data, html_path):
        results['html'] = html_path
    
    return results
