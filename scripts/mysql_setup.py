#!/usr/bin/env python3
"""
MySQL Database Setup Script for Travel Booking Application

This script helps set up MySQL database for the travel booking application.

Usage:
    python scripts/mysql_setup.py

Environment Variables:
    DB_NAME - Database name (default: travel_booking_db)
    DB_USER - Database user (default: root)
    DB_PASSWORD - Database password (default: empty)
    DB_HOST - Database host (default: localhost)
    DB_PORT - Database port (default: 3306)
"""

import os
import sys
import mysql.connector
from mysql.connector import Error


def create_database():
    """Create MySQL database if it doesn't exist"""
    
    # Database configuration
    config = {
        'host': os.environ.get('DB_HOST', 'localhost'),
        'port': os.environ.get('DB_PORT', '3306'),
        'user': os.environ.get('DB_USER', 'root'),
        'password': os.environ.get('DB_PASSWORD', ''),
    }
    
    db_name = os.environ.get('DB_NAME', 'travel_booking_db')
    
    try:
        # Connect to MySQL server
        print(f"Connecting to MySQL server at {config['host']}:{config['port']}...")
        connection = mysql.connector.connect(**config)
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Create database if it doesn't exist
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
            print(f"Database '{db_name}' created successfully or already exists.")
            
            # Create user if needed (optional)
            if config['user'] != 'root':
                try:
                    cursor.execute(f"CREATE USER IF NOT EXISTS '{config['user']}'@'{config['host']}' IDENTIFIED BY '{config['password']}'")
                    cursor.execute(f"GRANT ALL PRIVILEGES ON {db_name}.* TO '{config['user']}'@'{config['host']}'")
                    cursor.execute("FLUSH PRIVILEGES")
                    print(f"User '{config['user']}' created and granted privileges.")
                except Error as e:
                    print(f"Warning: Could not create user: {e}")
            
            # Test connection to the database
            cursor.execute(f"USE {db_name}")
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"Successfully connected to MySQL version: {version[0]}")
            
            return True
            
    except Error as e:
        print(f"Error: {e}")
        return False
        
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed.")


def print_environment_setup():
    """Print environment variables setup instructions"""
    print("\n" + "="*60)
    print("MYSQL SETUP COMPLETE")
    print("="*60)
    print("\nTo use MySQL with your Django application:")
    print("\n1. Set environment variables:")
    print("   export USE_MYSQL=true")
    print(f"   export DB_NAME={os.environ.get('DB_NAME', 'travel_booking_db')}")
    print(f"   export DB_USER={os.environ.get('DB_USER', 'root')}")
    print(f"   export DB_PASSWORD={os.environ.get('DB_PASSWORD', 'your_password')}")
    print(f"   export DB_HOST={os.environ.get('DB_HOST', 'localhost')}")
    print(f"   export DB_PORT={os.environ.get('DB_PORT', '3306')}")
    print("\n2. Install MySQL client for Python:")
    print("   pip install mysqlclient")
    print("\n3. Run Django migrations:")
    print("   python manage.py makemigrations")
    print("   python manage.py migrate")
    print("\n4. Create sample data:")
    print("   python manage.py create_sample_data")
    print("\n" + "="*60)


def check_mysql_client():
    """Check if MySQL client is installed"""
    try:
        import MySQLdb
        print("✓ MySQLdb (mysqlclient) is installed")
        return True
    except ImportError:
        print("✗ MySQLdb (mysqlclient) is not installed")
        print("Install it with: pip install mysqlclient")
        return False


def main():
    print("Travel Booking - MySQL Setup Script")
    print("="*40)
    
    # Check MySQL client
    if not check_mysql_client():
        print("\nPlease install mysqlclient first, then run this script again.")
        return
    
    # Get database configuration
    print("\nCurrent configuration:")
    print(f"  Host: {os.environ.get('DB_HOST', 'localhost')}")
    print(f"  Port: {os.environ.get('DB_PORT', '3306')}")
    print(f"  User: {os.environ.get('DB_USER', 'root')}")
    print(f"  Database: {os.environ.get('DB_NAME', 'travel_booking_db')}")
    
    # Confirm before proceeding
    confirm = input("\nProceed with MySQL setup? (y/N): ").lower().strip()
    if confirm != 'y':
        print("Setup cancelled.")
        return
    
    # Create database
    if create_database():
        print_environment_setup()
    else:
        print("\nSetup failed. Please check your MySQL configuration.")
        sys.exit(1)


if __name__ == "__main__":
    main()
