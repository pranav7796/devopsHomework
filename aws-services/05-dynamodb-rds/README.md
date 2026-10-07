# DynamoDB and RDS — databases

## DynamoDB

Managed NoSQL key-value/document database. Tables contain items with attributes. A partition key distributes records; an optional sort key orders related items within a partition. Model access patterns first. It fits low-latency key-based workloads and elastic serverless applications.

## RDS

Managed relational databases for engines including PostgreSQL, MySQL, MariaDB, Oracle, and SQL Server (availability varies by region/edition). A DB instance provides compute/storage. Restrict access with VPC security groups, encrypt data, and configure backups. Multi-AZ improves availability through a standby; read replicas scale reads and support some migration patterns. Use RDS where SQL, transactions, and relational constraints fit the application.
