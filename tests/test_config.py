from app.config import Settings

def test_default_topic_and_group():
    config = Settings()
    assert config.kafka_topic == "orders"
    assert config.kafka_group_id
    assert "dbname=" in config.postgres_dsn
