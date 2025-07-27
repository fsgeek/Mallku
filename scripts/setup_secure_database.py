#!/usr/bin/env python3
"""
Secure Database Setup for Mallku
================================

Based on Indaleko's secure credential patterns, this script:
1. Generates secure random passwords
2. Creates configuration with proper credentials
3. Sets up Docker containers with authentication
4. Provides simple retrieval commands

This replaces the expedient "test_password" approach with
proper security that requires no memorization.

Run with:
    python scripts/setup_secure_database.py --setup
    python scripts/setup_secure_database.py --show-credentials
"""

import argparse
import configparser
import json
import logging
import os
import secrets
import string
import sys
from datetime import UTC, datetime
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class MallkuSecureDBConfig:
    """Secure database configuration management for Mallku."""

    DEFAULT_CONFIG_DIR = Path.home() / ".mallku" / "config"
    DEFAULT_CONFIG_FILE = DEFAULT_CONFIG_DIR / "db_secure.ini"
    DEFAULT_DOCKER_CONFIG = DEFAULT_CONFIG_DIR / "docker_secure.json"

    def __init__(self, config_file: Path | None = None):
        """Initialize secure configuration."""
        self.config_file = config_file or self.DEFAULT_CONFIG_FILE
        self.docker_config_file = self.DEFAULT_DOCKER_CONFIG
        self.config = configparser.ConfigParser()

    @staticmethod
    def generate_secure_password(length: int = 20) -> str:
        """
        Generate a cryptographically secure password.

        Uses secrets module for cryptographic randomness.
        Excludes ambiguous characters (0, O, l, 1, I).
        """
        # Exclude ambiguous characters
        alphabet = "".join(c for c in string.ascii_letters + string.digits if c not in "O0lI1")
        # Ensure at least one of each type
        password = [
            secrets.choice(string.ascii_uppercase),
            secrets.choice(string.ascii_lowercase),
            secrets.choice(string.digits),
        ]
        # Fill the rest
        password.extend(secrets.choice(alphabet) for _ in range(length - 3))
        # Shuffle to avoid predictable patterns
        secrets.SystemRandom().shuffle(password)
        return "".join(password)

    @staticmethod
    def generate_secure_username(prefix: str = "mallku", length: int = 8) -> str:
        """Generate a secure username with prefix."""
        suffix = "".join(
            secrets.choice(string.ascii_lowercase + string.digits) for _ in range(length)
        )
        return f"{prefix}_{suffix}"

    def generate_config(self) -> dict[str, dict[str, str]]:
        """Generate new secure configuration."""
        timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")

        config = {
            "database": {
                "host": "localhost",
                "port": "8529",
                "database": "mallku",
                "ssl": "false",
                "created": timestamp,
            },
            "credentials": {
                "root_password": self.generate_secure_password(24),
                "mallku_user": self.generate_secure_username("mallku", 6),
                "mallku_password": self.generate_secure_password(20),
            },
            "docker": {
                "container_name": f"mallku-db-{timestamp}",
                "volume_name": f"mallku-data-{timestamp}",
                "network_name": "mallku-internal",
            },
            "api": {
                "gateway_container": f"mallku-api-{timestamp}",
                "gateway_port": "8080",
            },
        }

        return config

    def save_config(self, config: dict[str, dict[str, str]]) -> None:
        """Save configuration securely."""
        # Ensure directory exists with restricted permissions
        self.config_file.parent.mkdir(parents=True, exist_ok=True)

        # Convert dict to ConfigParser format
        for section, values in config.items():
            self.config[section] = values

        # Write config file with restricted permissions
        with open(self.config_file, "w") as f:
            self.config.write(f)

        # Restrict file permissions (owner read/write only)
        os.chmod(self.config_file, 0o600)

        # Also save Docker-specific config
        docker_config = {
            "version": "3.8",
            "container": config["docker"]["container_name"],
            "volume": config["docker"]["volume_name"],
            "network": config["docker"]["network_name"],
            "root_password": config["credentials"]["root_password"],
            "api_container": config["api"]["gateway_container"],
            "api_port": config["api"]["gateway_port"],
        }

        with open(self.docker_config_file, "w") as f:
            json.dump(docker_config, f, indent=2)

        os.chmod(self.docker_config_file, 0o600)

        logger.info(f"Secure configuration saved to {self.config_file}")
        logger.info(f"Docker configuration saved to {self.docker_config_file}")

    def load_config(self) -> bool:
        """Load existing configuration."""
        if not self.config_file.exists():
            return False

        self.config.read(self.config_file)
        return True

    def get_credentials(self) -> dict[str, str] | None:
        """Retrieve credentials from config."""
        if not self.load_config():
            return None

        if "credentials" not in self.config:
            return None

        return dict(self.config["credentials"])

    def show_credentials(self) -> None:
        """Display credentials for user access."""
        creds = self.get_credentials()
        if not creds:
            print("❌ No credentials found. Run with --setup first.")
            return

        print("\n🔐 Mallku Database Credentials")
        print("=" * 50)
        print(f"  Username: {creds.get('mallku_user')}")
        print(f"  Password: {creds.get('mallku_password')}")
        print(f"  Root Password: {creds.get('root_password')}")
        print("\n📍 Connection Details:")
        print(f"  Host: {self.config['database']['host']}")
        print(f"  Port: {self.config['database']['port']}")
        print(f"  Database: {self.config['database']['database']}")
        print("\n🐳 Docker Details:")
        print(f"  Container: {self.config['docker']['container_name']}")
        print(f"  Volume: {self.config['docker']['volume_name']}")
        print("=" * 50)

    def create_docker_compose(self, config: dict[str, dict[str, str]]) -> Path:
        """Create secure docker-compose.yml."""
        compose_file = self.DEFAULT_CONFIG_DIR / "docker-compose-secure.yml"

        compose_content = f"""version: '3.8'

# Secure Mallku Database Configuration
# Generated: {datetime.now(UTC).isoformat()}

services:
  database:
    image: arangodb:latest
    container_name: {config["docker"]["container_name"]}
    environment:
      - ARANGO_ROOT_PASSWORD={config["credentials"]["root_password"]}
    volumes:
      - {config["docker"]["volume_name"]}:/var/lib/arangodb3
    networks:
      - {config["docker"]["network_name"]}
    # No ports exposed - security through architecture
    healthcheck:
      test: ["CMD", "wget", "--spider", "-q", "http://localhost:8529/_api/version"]
      interval: 10s
      timeout: 5s
      retries: 10
      start_period: 30s

  api:
    build:
      context: {Path.cwd()}
      dockerfile: docker/Dockerfile.api
    container_name: {config["api"]["gateway_container"]}
    depends_on:
      database:
        condition: service_healthy
    environment:
      - MALLKU_DB_HOST=database
      - MALLKU_DB_PORT=8529
      - MALLKU_DB_NAME={config["database"]["database"]}
      - MALLKU_DB_USER={config["credentials"]["mallku_user"]}
      - MALLKU_DB_PASSWORD={config["credentials"]["mallku_password"]}
      - MALLKU_API_HOST=0.0.0.0
      - MALLKU_API_PORT={config["api"]["gateway_port"]}
    ports:
      - "{config["api"]["gateway_port"]}:{config["api"]["gateway_port"]}"
    networks:
      - {config["docker"]["network_name"]}
      - mallku-external
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:{config["api"]["gateway_port"]}/health"]
      interval: 30s
      timeout: 10s
      retries: 5

networks:
  {config["docker"]["network_name"]}:
    internal: true  # Cannot be reached from host
  mallku-external:
    # Only the API container connects here

volumes:
  {config["docker"]["volume_name"]}:
"""

        with open(compose_file, "w") as f:
            f.write(compose_content)

        return compose_file

    def update_mallku_config(self, config: dict[str, dict[str, str]]) -> None:
        """Update Mallku's database configuration to use secure credentials."""
        # Update the main database.py config
        db_config_updates = {
            "MALLKU_DB_HOST": config["database"]["host"],
            "MALLKU_DB_PORT": config["database"]["port"],
            "MALLKU_DB_NAME": config["database"]["database"],
            "MALLKU_DB_USER": config["credentials"]["mallku_user"],
            "MALLKU_DB_PASSWORD": config["credentials"]["mallku_password"],
        }

        # Create .env file for easy loading
        env_file = Path.cwd() / ".env.secure"
        with open(env_file, "w") as f:
            for key, value in db_config_updates.items():
                f.write(f"{key}={value}\n")

        os.chmod(env_file, 0o600)

        logger.info(f"Environment variables saved to {env_file}")
        logger.info("Source this file before running Mallku: source .env.secure")


def setup_command(args: argparse.Namespace) -> None:
    """Set up secure database configuration."""
    config_manager = MallkuSecureDBConfig()

    # Check if config already exists
    if config_manager.load_config() and not args.force:
        print("⚠️  Configuration already exists. Use --force to regenerate.")
        config_manager.show_credentials()
        return

    print("🔐 Generating secure database configuration...")

    # Generate secure config
    config = config_manager.generate_config()

    # Save configuration
    config_manager.save_config(config)

    # Create docker-compose file
    compose_file = config_manager.create_docker_compose(config)
    print(f"✓ Docker Compose file created: {compose_file}")

    # Update Mallku config
    config_manager.update_mallku_config(config)

    # Show the credentials
    print("\n✅ Secure configuration created successfully!")
    config_manager.show_credentials()

    print("\n📝 Next steps:")
    print(
        "  1. Start the database: docker-compose -f ~/.mallku/config/docker-compose-secure.yml up -d"
    )
    print("  2. Source environment: source .env.secure")
    print("  3. Run Mallku with secure credentials automatically loaded")


def show_command(args: argparse.Namespace) -> None:
    """Show existing credentials."""
    config_manager = MallkuSecureDBConfig()
    config_manager.show_credentials()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Secure database setup for Mallku",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Initial setup
  python scripts/setup_secure_database.py --setup

  # Show credentials when needed
  python scripts/setup_secure_database.py --show-credentials

  # Force regenerate credentials
  python scripts/setup_secure_database.py --setup --force
        """,
    )

    parser.add_argument(
        "--setup", action="store_true", help="Set up new secure database configuration"
    )

    parser.add_argument(
        "--show-credentials", action="store_true", help="Display existing credentials"
    )

    parser.add_argument(
        "--force", action="store_true", help="Force regeneration of credentials (with --setup)"
    )

    args = parser.parse_args()

    if args.setup:
        setup_command(args)
    elif args.show_credentials:
        show_command(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
