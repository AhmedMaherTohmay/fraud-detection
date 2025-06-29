# src/monitoring/setup.py
"""
Setup script for fraud detection monitoring.
This script helps initialize and manage the monitoring infrastructure.
"""

import os
import subprocess
import sys
from pathlib import Path

class MonitoringSetup:
    def __init__(self):
        self.monitoring_dir = Path(__file__).parent
        self.config_dir = self.monitoring_dir / "config"
        
    def install_requirements(self):
        """Install required Python packages for monitoring."""
        requirements = [
            "prometheus-flask-exporter==0.23.0",
            "prometheus-client==0.19.0"
        ]
        
        print("Installing monitoring requirements...")
        for req in requirements:
            subprocess.check_call([sys.executable, "-m", "pip", "install", req])
        print("✅ Requirements installed successfully!")
    
    def start_monitoring(self):
        """Start Prometheus and Grafana using Docker Compose."""
        os.chdir(self.config_dir)
        print("Starting monitoring infrastructure...")
        try:
            subprocess.run(["docker-compose", "up", "-d"], check=True)
            print("✅ Monitoring infrastructure started successfully!")
            print("\n📊 Access URLs:")
            print("   Grafana: http://localhost:3000 (admin/admin)")
            print("   Prometheus: http://localhost:9090")
            print("   Your App Metrics: http://localhost:5000/metrics")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error starting monitoring infrastructure: {e}")
    
    def stop_monitoring(self):
        """Stop Prometheus and Grafana containers."""
        os.chdir(self.config_dir)
        print("Stopping monitoring infrastructure...")
        try:
            subprocess.run(["docker-compose", "down"], check=True)
            print("✅ Monitoring infrastructure stopped successfully!")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error stopping monitoring infrastructure: {e}")
    
    def show_status(self):
        """Show status of monitoring containers."""
        os.chdir(self.config_dir)
        print("Monitoring infrastructure status:")
        try:
            subprocess.run(["docker-compose", "ps"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Error checking status: {e}")
    
    def view_logs(self, service=None):
        """View logs from monitoring services."""
        os.chdir(self.config_dir)
        if service:
            print(f"Viewing logs for {service}...")
            subprocess.run(["docker-compose", "logs", "-f", service])
        else:
            print("Viewing all monitoring logs...")
            subprocess.run(["docker-compose", "logs", "-f"])

def main():
    setup = MonitoringSetup()
    
    if len(sys.argv) < 2:
        print("Usage: python setup.py [install|start|stop|status|logs]")
        return
    
    command = sys.argv[1]
    
    if command == "install":
        setup.install_requirements()
    elif command == "start":
        setup.start_monitoring()
    elif command == "stop":
        setup.stop_monitoring()
    elif command == "status":
        setup.show_status()
    elif command == "logs":
        service = sys.argv[2] if len(sys.argv) > 2 else None
        setup.view_logs(service)
    else:
        print(f"Unknown command: {command}")
        print("Available commands: install, start, stop, status, logs")

if __name__ == "__main__":
    main()