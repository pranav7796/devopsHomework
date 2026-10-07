# Amazon S3 — object storage

S3 stores objects (data plus metadata) in globally unique bucket names within a region. Storage classes trade access latency/cost and retrieval fees. Versioning retains prior object versions; lifecycle rules transition or expire objects. Encryption can be server-side or client-side. Bucket policies grant resource-level access; block public access by default and apply least privilege. Common uses include backups, static assets, logs, and data lakes. Terraform demo enables versioning, AES-256 server-side encryption, and public-access blocks.
