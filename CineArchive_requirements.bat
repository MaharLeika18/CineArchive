@echo off
REM Batch file to install Python packages with specific versions

echo Installing Python packages...
pip install alembic==1.15.2
pip install blinker==1.9.0
pip install cffi==1.17.1
pip install click==8.1.8
pip install cryptography==44.0.2
pip install Flask==3.1.0
pip install Flask-Login==0.6.3
pip install Flask-Migrate==4.1.0
pip install Flask-SQLAlchemy==3.1.1
pip install itsdangerous==2.2.0
pip install Jinja2==3.1.6
pip install Mako==1.3.10
pip install MarkupSafe==3.0.2
pip install mysql-connector==2.2.9
pip install mysql-connector-python==9.3.0
pip install mysql-connector-python-rf==2.2.2
pip install numpy==2.2.5
pip install pandas==2.2.3
pip install pycparser==2.22
pip install PyMySQL==1.1.1
pip install python-dateutil==2.9.0.post0
pip install python-dotenv==1.1.0
pip install pytz==2025.2
pip install six==1.17.0
pip install SQLAlchemy==2.0.40
pip install typing_extensions==4.13.2
pip install tzdata==2025.2
pip install Werkzeug==3.1.3

echo All packages installed successfully.
pause