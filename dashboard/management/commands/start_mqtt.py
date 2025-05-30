from django.core.management.base import BaseCommand
from dashboard.mqtt_service import mqtt_service
import time
import signal
import sys

class Command(BaseCommand):
    help = 'Start MQTT service to listen for sensor data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--restart-interval',
            type=int,
            default=300,
            help='Restart MQTT clients every N seconds (default: 300)'
        )

    def handle(self, *args, **options):
        restart_interval = options['restart_interval']
        
        def signal_handler(sig, frame):
            self.stdout.write(self.style.WARNING('Stopping MQTT service...'))
            mqtt_service.stop_all_clients()
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        self.stdout.write(self.style.SUCCESS('Starting MQTT service...'))
        
        try:
            while True:
                # Start MQTT listeners
                mqtt_service.start_mqtt_listeners()
                self.stdout.write(self.style.SUCCESS('MQTT listeners started'))
                
                # Wait for restart interval
                time.sleep(restart_interval)
                
                # Restart clients to handle any connection issues
                self.stdout.write(self.style.WARNING('Restarting MQTT clients...'))
                mqtt_service.stop_all_clients()
                
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING('MQTT service stopped'))
            mqtt_service.stop_all_clients()