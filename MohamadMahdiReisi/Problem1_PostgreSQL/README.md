
# PostgreSQL Docker Deployment with Persistent Storage

![PostgreSQL Logo](https://www.postgresql.org/media/img/about/press/elephant.png)

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Detailed Usage](#detailed-usage)
- [Data Persistence Verification](#data-persistence-verification)
- [Maintenance](#maintenance)
- [Troubleshooting](#troubleshooting)
- [Security Considerations](#security-considerations)
- [Contributing](#contributing)
- [License](#license)

## Overview

This project provides a complete solution for deploying PostgreSQL in Docker with persistent storage, designed specifically for:
- Development environments
- Learning database concepts
- Capture The Flag (CTF) challenges
- Application prototyping

## Features

✔ **Persistent Data Storage** - Uses Docker volumes to maintain data between container restarts  
✔ **Pre-configured Environment** - Ready-to-use database with user credentials  
✔ **Simple Operations** - Includes sample SQL commands for basic CRUD operations  
✔ **Verification Scripts** - Commands to validate data persistence  
✔ **Production-ready Foundation** - Can be extended for more complex deployments  

## Quick Start

### 1. Deploy the Container
```bash
docker run -d \
  --name postgres_ctf \
  -e POSTGRES_USER=ctf_user \
  -e POSTGRES_PASSWORD=ctf_password \
  -e POSTGRES_DB=ctf_db \
  -p 5432:5432 \
  -v postgres_data:/var/lib/postgresql/data \
  postgres:latest
```

### 2. Connect and Test
```bash
docker exec -it postgres_ctf psql -U ctf_user -d ctf_db -c "SELECT version();"
```

## Detailed Usage

### Database Initialization
The container automatically:
- Creates the specified user (`ctf_user`)
- Creates the default database (`ctf_db`)
- Sets up the persistent volume

### Common Operations

**Create Table:**
```sql
CREATE TABLE challenges (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  points INTEGER NOT NULL,
  category VARCHAR(50),
  is_active BOOLEAN DEFAULT true
);
```

**Insert Data:**
```sql
INSERT INTO challenges (name, points, category) VALUES 
  ('SQL Injection', 100, 'Web'),
  ('Buffer Overflow', 200, 'Binary'),
  ('Cryptanalysis', 150, 'Crypto');
```

**Query Data:**
```sql
-- Basic query
SELECT * FROM challenges;

-- Filtered query
SELECT name, points FROM challenges WHERE points > 120;

-- Aggregation
SELECT category, AVG(points) as avg_points FROM challenges GROUP BY category;
```

## Data Persistence Verification

1. **Stop and remove the container**
   ```bash
   docker stop postgres_ctf
   docker rm postgres_ctf
   ```

2. **Redeploy with same volume**
   ```bash
   docker run -d \
     --name postgres_ctf_new \
     -v postgres_data:/var/lib/postgresql/data \
     -p 5432:5432 \
     postgres:latest
   ```

3. **Verify data integrity**
   ```bash
   docker exec -it postgres_ctf_new psql -U ctf_user -d ctf_db -c "SELECT * FROM challenges;"
   ```

## Maintenance

### Backup Database
```bash
docker exec postgres_ctf pg_dump -U ctf_user -d ctf_db > ctf_backup.sql
```

### Restore Database
```bash
cat ctf_backup.sql | docker exec -i postgres_ctf psql -U ctf_user -d ctf_db
```

### Monitor Performance
```bash
docker exec -it postgres_ctf psql -U ctf_user -d ctf_db -c "SELECT * FROM pg_stat_activity;"
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Connection refused | Check if container is running: `docker ps` |
| Authentication failed | Verify credentials in environment variables |
| Volume not persisting | Confirm volume mount: `docker inspect postgres_ctf` |
| Port conflicts | Change host port mapping (e.g., `-p 5433:5432`) |

## Security Considerations

For production environments, we recommend:
1. Using complex passwords
2. Enabling SSL connections
3. Implementing network isolation
4. Regular backups
5. Monitoring access logs

## Contributing

We welcome contributions! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

MIT License - See [LICENSE](LICENSE) for details.

---

**Pro Tip**: For advanced configurations, check out the [official PostgreSQL Docker image documentation](https://hub.docker.com/_/postgres).