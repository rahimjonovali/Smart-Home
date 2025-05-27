from django.apps import AppConfig


class DashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dashboard'

    def ready(self):
        import dashboard.signals
        
        # Start MQTT service in a separate thread when Django starts
        try:
            from dashboard.mqtt_service import mqtt_service
            import threading
            
            def start_mqtt_background():
                mqtt_service.start_mqtt_listeners()
            
            # Start MQTT service in background thread
            mqtt_thread = threading.Thread(target=start_mqtt_background, daemon=True)
            mqtt_thread.start()
            
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Failed to start MQTT service: {e}")