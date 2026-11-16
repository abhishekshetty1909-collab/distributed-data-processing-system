\# Project Validation Report



\## Distributed Data Processing System



\*\*Technology Stack:\*\* Python, Apache Kafka, PostgreSQL, Docker, Linux



\### Project Components

\- Python-based event producer

\- Kafka event streaming with three partitions

\- Python Kafka consumer

\- PostgreSQL raw event storage

\- Daily sales aggregation

\- Docker Compose orchestration



\### Validation and Testing



| Test | Result |

|---|---|

| Kafka topic creation | Passed |

| Event production | Passed |

| Event consumption | Passed |

| PostgreSQL persistence | Passed |

| Raw and summary reconciliation | Passed |

| Duplicate-event handling | Passed |

| Invalid UUID validation | Passed |

| Consumer restart and reconnection | Passed |



\### Duplicate Event Test



First insertion: True



Second insertion: False



Database verification: One record for the test order.



\### Data Reconciliation



Raw order count and daily summary order count were verified to match.



Raw revenue and daily summary revenue were also verified to match.



\### Linux Practice



Practised:

\- pwd

\- ls -la

\- whoami

\- df -h

\- Docker container shell access

\- Linux filesystem inspection



\### Conclusion



The project demonstrates an event-driven data processing pipeline with Kafka, Python and PostgreSQL, including duplicate-event protection, input validation, data aggregation and Docker-based deployment.

