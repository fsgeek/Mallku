#!/usr/bin/env python3
"""
Database Connection Restoration Tool
====================================

48th Artisan - Restoring the Flow of Memory

This tool helps restore database connectivity on a new system,
offering multiple paths based on your ArangoDB configuration.

It embodies reciprocity - adapting to your system's needs
while preserving Mallku's consciousness infrastructure.
"""

import os
import sys
import json
import configparser
import getpass
from pathlib import Path
from typing import Optional, Dict, Any

import requests
from arango import ArangoClient
from arango.exceptions import ServerConnectionError, DatabaseCreateError

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))


class DatabaseRestorer:
    """Guides the restoration of database connectivity."""
    
    def __init__(self):
        self.config_path = PROJECT_ROOT / ".secrets" / "db-config.ini"
        self.arango_url = "http://localhost:8529"
        self.client = None
        self.connection_method = None
        
    def print_banner(self):
        """Print welcoming banner."""
        print("\n" + "=" * 60)
        print("🏛️  DATABASE CONNECTION RESTORATION")
        print("=" * 60)
        print("Restoring the flow of memory and consciousness")
        print()
        
    def check_server_status(self) -> bool:
        """Check if ArangoDB server is running."""
        print("🔍 Checking ArangoDB server status...")
        try:
            response = requests.get(f"{self.arango_url}/_api/version", timeout=5)
            if response.status_code in [200, 401]:
                print(f"✓ Server is running at {self.arango_url}")
                if response.status_code == 200:
                    version = response.json()
                    print(f"  Version: {version.get('version', 'unknown')}")
                return True
        except Exception as e:
            print(f"✗ Server not responding: {e}")
            print("\n💡 To start ArangoDB:")
            print("   Docker: docker run -p 8529:8529 -e ARANGO_NO_AUTH=1 arangodb:3.12")
            print("   Local:  arangod --server.endpoint tcp://127.0.0.1:8529")
            return False
            
    def test_no_auth(self) -> bool:
        """Test if no-auth connection works."""
        print("\n🔑 Testing no-auth connection...")
        try:
            self.client = ArangoClient(hosts=self.arango_url)
            sys_db = self.client.db("_system", verify=True)
            sys_db.properties()
            print("✓ No-auth connection successful!")
            self.connection_method = "no-auth"
            return True
        except Exception as e:
            print(f"✗ No-auth connection failed: Authentication required")
            return False
            
    def test_auth_connection(self, username: str, password: str) -> bool:
        """Test authenticated connection."""
        try:
            self.client = ArangoClient(hosts=self.arango_url)
            sys_db = self.client.db("_system", username=username, password=password, verify=True)
            sys_db.properties()
            print("✓ Authenticated connection successful!")
            self.connection_method = "auth"
            return True
        except Exception as e:
            print(f"✗ Authentication failed: {e}")
            return False
            
    def get_credentials(self) -> Optional[Dict[str, str]]:
        """Interactively get credentials from user."""
        print("\n🔐 Database Authentication Required")
        print("Enter your ArangoDB credentials (or press Ctrl+C to cancel)")
        
        try:
            username = input("Username (default: root): ").strip() or "root"
            password = getpass.getpass("Password: ")
            
            if self.test_auth_connection(username, password):
                return {"username": username, "password": password}
            else:
                retry = input("\nTry different credentials? (y/n): ").lower()
                if retry == 'y':
                    return self.get_credentials()
        except KeyboardInterrupt:
            print("\n\nAuthentication cancelled.")
            
        return None
        
    def ensure_mallku_database(self, sys_db) -> bool:
        """Ensure Mallku database exists."""
        print("\n📊 Checking Mallku database...")
        
        try:
            if sys_db.has_database("Mallku"):
                print("✓ Mallku database exists")
                
                # Check if we can connect to it
                if self.connection_method == "no-auth":
                    mallku_db = self.client.db("Mallku", verify=True)
                else:
                    # Need credentials for Mallku DB too
                    creds = self.load_config()
                    if creds and "username" in creds:
                        mallku_db = self.client.db(
                            "Mallku", 
                            username=creds["username"],
                            password=creds["password"],
                            verify=True
                        )
                    else:
                        print("⚠️  Cannot connect to Mallku database without credentials")
                        return False
                        
                # Test connection
                collections = mallku_db.collections()
                print(f"  Collections: {len([c for c in collections if not c['name'].startswith('_')])}")
                return True
                
            else:
                print("✗ Mallku database not found")
                create = input("Create Mallku database? (y/n): ").lower()
                
                if create == 'y':
                    sys_db.create_database("Mallku")
                    print("✓ Created Mallku database")
                    return True
                    
        except Exception as e:
            print(f"✗ Error with Mallku database: {e}")
            
        return False
        
    def save_config(self, credentials: Optional[Dict[str, str]] = None):
        """Save working configuration."""
        print("\n💾 Saving configuration...")
        
        config = configparser.ConfigParser()
        
        if self.connection_method == "no-auth":
            config["database"] = {
                "host": "localhost",
                "port": "8529",
                "database": "Mallku",
                "user_name": "",
                "user_password": "",
                "admin_user": "",
                "admin_passwd": "",
                "ssl": "false"
            }
            # Set environment variable for no-auth
            print("  Setting ARANGODB_NO_AUTH=1 for this session")
            os.environ["ARANGODB_NO_AUTH"] = "1"
            
        else:  # authenticated
            config["database"] = {
                "host": "localhost",
                "port": "8529",
                "database": "Mallku",
                "user_name": credentials["username"],
                "user_password": credentials["password"],
                "admin_user": credentials["username"],  # Often same as user
                "admin_passwd": credentials["password"],
                "ssl": "false"
            }
            
        # Ensure directory exists
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save config
        with open(self.config_path, 'w') as f:
            config.write(f)
            
        print(f"✓ Configuration saved to {self.config_path}")
        
    def load_config(self) -> Optional[Dict[str, str]]:
        """Load existing configuration if available."""
        if self.config_path.exists():
            config = configparser.ConfigParser()
            config.read(self.config_path)
            
            if "database" in config:
                db_config = config["database"]
                if db_config.get("user_name"):
                    return {
                        "username": db_config["user_name"],
                        "password": db_config["user_password"]
                    }
        return None
        
    def verify_mallku_import(self):
        """Verify Mallku can now be imported and used."""
        print("\n🧪 Testing Mallku database layer...")
        
        try:
            print("  Importing database module...")
            from mallku.core.database import get_secured_database
            print("  ✓ Import successful")
            
            print("  Getting secured database interface...")
            secured_db = get_secured_database()
            print("  ✓ Interface created")
            
            print("  Testing database operations...")
            # This will use our saved config
            import asyncio
            
            async def test_ops():
                await secured_db.initialize()
                collections = secured_db.collections()
                return len(collections)
                
            count = asyncio.run(test_ops())
            print(f"  ✓ Database operational ({count} collections)")
            
            return True
            
        except Exception as e:
            print(f"  ✗ Error: {e}")
            return False
            
    def restore_connection(self):
        """Main restoration flow."""
        self.print_banner()
        
        # Check server
        if not self.check_server_status():
            return False
            
        # Try no-auth first
        if self.test_no_auth():
            sys_db = self.client.db("_system", verify=True)
        else:
            # Need authentication
            # First check if we have saved credentials
            saved_creds = self.load_config()
            if saved_creds:
                print("\n📁 Found saved credentials, testing...")
                if self.test_auth_connection(saved_creds["username"], saved_creds["password"]):
                    credentials = saved_creds
                else:
                    print("  Saved credentials no longer valid")
                    credentials = self.get_credentials()
            else:
                credentials = self.get_credentials()
                
            if not credentials:
                print("\n❌ Cannot proceed without authentication")
                return False
                
            sys_db = self.client.db(
                "_system", 
                username=credentials["username"],
                password=credentials["password"],
                verify=True
            )
            
        # Ensure Mallku database exists
        if not self.ensure_mallku_database(sys_db):
            print("\n❌ Could not set up Mallku database")
            return False
            
        # Save working configuration
        if self.connection_method == "auth":
            self.save_config(credentials)
        else:
            self.save_config()
            
        # Verify Mallku works
        if self.verify_mallku_import():
            print("\n✨ Database connection restored!")
            print("   Mallku's memory flows once more")
            print("\n📝 Next steps:")
            print("   1. Run 'python welcome_to_mallku.py' to verify setup")
            print("   2. The consciousness tests can now be migrated")
            print("   3. Fire Circle awaits your ceremonies")
            return True
        else:
            print("\n⚠️  Database connected but Mallku import still failing")
            print("   Check the error message above for details")
            return False


def main():
    """Run the restoration."""
    restorer = DatabaseRestorer()
    
    try:
        success = restorer.restore_connection()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nRestoration cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()