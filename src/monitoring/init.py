# src/monitoring/__init__.py
"""
Monitoring module for fraud detection application.
Provides Prometheus metrics integration and Grafana dashboards.
"""

from .metrics import init_metrics

__all__ = ['init_metrics']