import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    kafka_bootstrap_servers: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9094")
    kafka_topic: str = os.getenv("KAFKA_TOPIC", "orders")
    kafka_group_id: str = os.getenv("KAFKA_GROUP_ID", "orders-postgres-writer")
    events_per_second: float = float(os.getenv("EVENTS_PER_SECOND", "2"))
    postgres_host: str = os.getenv("POSTGRES_HOST", "localhost")
    postgres_port: int = int(os.getenv("POSTGRES_PORT", "5432"))
    postgres_db: str = os.getenv("POSTGRES_DB", "ecommerce")
    postgres_user: str = os.getenv("POSTGRES_USER", "pipeline")
    postgres_password: str = os.getenv("POSTGRES_PASSWORD", "pipeline_dev_password")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

    @property
    def postgres_dsn(self):
        return (f"host={self.postgres_host} port={self.postgres_port} "
                f"dbname={self.postgres_db} user={self.postgres_user} "
                f"password={self.postgres_password}")

settings = Settings()
