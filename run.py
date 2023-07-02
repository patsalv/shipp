from dotenv import load_dotenv
import os

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from app import create_app
from flask_migrate import upgrade
from app.extensions import db, migrate
from app.models.database_model import Device, DeviceConfig, Policy

current_config: str = None

if os.getenv('FLASK_ENV') == 'production':
    current_config = "production"
else:
    current_config = "development"

app = create_app(current_config)

migrate.init_app(app, db)


@app.cli.command()
def execute_job():
    """Run scheduled job"""
    from app.monitors.pihole_monitor import fetch_query_data_job
    fetch_query_data_job()


@app.cli.command()
def deploy():
    """Run deployment tasks."""
    # migrate database to latest revision
    upgrade()


@app.cli.command()
def execute_weekly_notifications():
    """Send weekly notification to users"""
    from app.reporting.email_notification_service import send_weekly_emails
    with app.app_context():
        send_weekly_emails()
    app.logger.info("Sent all weekly notifications")


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Device=Device,
                DeviceConfig=DeviceConfig, Policy=Policy)


if __name__ == '__main__':
    app.logger.info("Starting with app.run()..")
    app.run(debug=True, use_debugger=False, use_reloader=False, passthrough_errors=True)
