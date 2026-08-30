# 🗄️ Database Design

> Database architecture and data model specification for Smart Infrastructure Operations Dashboard (SIOD).

![Project](https://img.shields.io/badge/Project-SIOD-blue)
![Database](https://img.shields.io/badge/Database-Design-green)
![Architecture](https://img.shields.io/badge/Data-Model-purple)
![Status](https://img.shields.io/badge/Document-Database%20Design-orange)

---

# 📖 Overview

This document defines the database architecture and data model used by **Smart Infrastructure Operations Dashboard (SIOD)**.

The database layer is responsible for storing:

- User information.
- Infrastructure assets.
- Services.
- Metrics metadata.
- Incidents.
- Notifications.
- Reports.
- Plugin information.
- AI operational history.

SIOD separates operational data based on its characteristics.

---

# 🏗️ Database Architecture

SIOD uses different storage strategies depending on the type of data.

```
                    SIOD

                     │

        ┌────────────┼────────────┐

        ▼            ▼            ▼

 Relational DB   Time Series   Vector DB

 PostgreSQL      Prometheus    AI Knowledge

        │            │            │

        ▼            ▼            ▼

Application     Metrics       AI Memory

Data            Data          Data
```

---

# 🗃️ Storage Strategy

## Relational Database

Recommended:

```
PostgreSQL
```

Used for:

- Users.
- Assets.
- Incidents.
- Configuration.
- Reports.
- Plugins.

---

## Time Series Database

Recommended:

```
Prometheus
```

Used for:

- CPU metrics.
- Memory metrics.
- Network metrics.
- Performance history.

---

## Vector Database

Used for AI knowledge storage.

Examples:

- ChromaDB.
- Qdrant.
- Weaviate.

Used for:

- Documentation.
- Runbooks.
- Previous incidents.
- Operational knowledge.

---

# 🧩 Core Entity Relationship

High-level relationship:

```
Users

  │

  ▼

Organizations

  │

  ▼

Assets

  │

  ├──────── Services

  │

  ├──────── Metrics

  │

  └──────── Incidents

                │

                ▼

          AI Analysis History
```

---

# 👤 Users Table

Stores user information.

Table:

```
users
```

Schema:

| Column | Type | Description |
|---|---|---|
| id | UUID | User identifier |
| username | VARCHAR | Login username |
| email | VARCHAR | User email |
| password_hash | VARCHAR | Encrypted password |
| role_id | UUID | User role |
| created_at | TIMESTAMP | Creation time |

---

# 🔐 Roles Table

Stores authorization roles.

Table:

```
roles
```

Example:

| Role | Permission |
|-|-|
| Admin | Full access |
| Operator | Manage incidents |
| Viewer | Read only |

---

# 🏢 Organizations Table

Supports future multi-tenant capability.

Table:

```
organizations
```

Schema:

| Column | Type |
|-|-|
| id | UUID |
| name | VARCHAR |
| created_at | TIMESTAMP |

---

# 🖥️ Assets Table

Stores infrastructure resources.

Table:

```
assets
```

Examples:

- Server.
- Container.
- VM.
- Network device.
- Cloud resource.

Schema:

| Column | Type | Description |
|-|-|-|
| id | UUID | Asset ID |
| name | VARCHAR | Resource name |
| type | VARCHAR | Asset type |
| hostname | VARCHAR | Host identity |
| status | VARCHAR | Current state |
| metadata | JSON | Additional information |

---

# 🔗 Asset Relationship Table

Stores infrastructure dependencies.

Table:

```
asset_relationships
```

Example:

```
Server

  │

  └── Docker Container

          │

          └── Application
```

Schema:

| Column | Type |
|-|-|
| id | UUID |
| source_asset | UUID |
| target_asset | UUID |
| relationship_type | VARCHAR |

---

# ⚙️ Services Table

Stores running services.

Table:

```
services
```

Example:

- Nginx.
- MySQL.
- Redis.
- Application service.

Schema:

| Column | Type |
|-|-|
| id | UUID |
| asset_id | UUID |
| name | VARCHAR |
| status | VARCHAR |
| version | VARCHAR |

---

# 📊 Metrics Table

Stores metric references.

Table:

```
metrics
```

Note:

High-frequency metric data is stored in the time-series database.

This table stores metadata.

Schema:

| Column | Type |
|-|-|
| id | UUID |
| asset_id | UUID |
| metric_name | VARCHAR |
| metric_type | VARCHAR |
| source | VARCHAR |

---

# 🚨 Incidents Table

Stores infrastructure incidents.

Table:

```
incidents
```

Schema:

| Column | Type | Description |
|-|-|-|
| id | UUID | Incident ID |
| asset_id | UUID | Related resource |
| title | VARCHAR | Incident name |
| severity | VARCHAR | Level |
| status | VARCHAR | Current state |
| source | VARCHAR | Detection source |
| created_at | TIMESTAMP | Time detected |

---

# 🔄 Incident History Table

Stores incident lifecycle.

Table:

```
incident_history
```

Schema:

| Column | Type |
|-|-|
| id | UUID |
| incident_id | UUID |
| action | VARCHAR |
| description | TEXT |
| created_at | TIMESTAMP |

Example:

```
Created

↓

Investigating

↓

Resolved
```

---

# 🔔 Notifications Table

Stores notification history.

Table:

```
notifications
```

Schema:

| Column | Type |
|-|-|
| id | UUID |
| incident_id | UUID |
| channel | VARCHAR |
| status | VARCHAR |
| sent_at | TIMESTAMP |

---

# 📄 Reports Table

Stores generated reports.

Table:

```
reports
```

Schema:

| Column | Type |
|-|-|
| id | UUID |
| type | VARCHAR |
| content | JSON |
| generated_at | TIMESTAMP |

---

# 🔌 Plugins Table

Stores installed plugins.

Table:

```
plugins
```

Schema:

| Column | Type |
|-|-|
| id | UUID |
| name | VARCHAR |
| version | VARCHAR |
| status | VARCHAR |
| configuration | JSON |

---

# 🤖 AI Analysis History Table

Stores AI operational decisions.

Table:

```
ai_analysis_history
```

Purpose:

- Improve future recommendations.
- Track AI decisions.
- Build operational knowledge.

Schema:

| Column | Type |
|-|-|
| id | UUID |
| incident_id | UUID |
| prompt | TEXT |
| response | TEXT |
| model | VARCHAR |
| created_at | TIMESTAMP |

---

# 📚 AI Knowledge Base

Used for Retrieval Augmented Generation.

Data sources:

- Documentation.
- Troubleshooting guides.
- Runbooks.
- Incident solutions.

Architecture:

```
Documents

     ↓

Embedding

     ↓

Vector Database

     ↓

AI Agent
```

---

# ⚙️ Configuration Table

Stores system configuration.

Table:

```
configurations
```

Schema:

| Column | Type |
|-|-|
| id | UUID |
| key | VARCHAR |
| value | JSON |
| updated_at | TIMESTAMP |

---

# 🔐 Audit Log Table

Tracks important activities.

Table:

```
audit_logs
```

Schema:

| Column | Type |
|-|-|
| id | UUID |
| user_id | UUID |
| action | VARCHAR |
| timestamp | TIMESTAMP |

---

# 📈 Database Scaling Strategy

Initial:

```
Single PostgreSQL Instance

+

Prometheus
```

Future:

```
PostgreSQL Cluster

+

Distributed Time Series Storage

+

Vector Database Cluster
```

---

# 🧪 Data Retention Strategy

Different data requires different retention policies.

Example:

| Data | Retention |
|-|-|
| Metrics | 30-365 days |
| Incidents | Permanent |
| Logs | Configurable |
| AI History | Long term |

---

# 🔐 Database Security

Requirements:

- Encrypted connections.
- Credential protection.
- Access control.
- Backup strategy.
- Migration management.

---

# 📊 Database Summary

| Entity | Purpose |
|-|-|
| Users | User management |
| Roles | Authorization |
| Organizations | Multi-tenant support |
| Assets | Infrastructure inventory |
| Services | Application resources |
| Metrics | Metric metadata |
| Incidents | Problem tracking |
| Notifications | Alert history |
| Reports | Operational reports |
| Plugins | Extension registry |
| AI History | AI operational memory |
| Audit Logs | Security tracking |

---

# Conclusion

The SIOD database design is created to support both current monitoring requirements and future AIOps capabilities.

By separating relational data, time-series metrics, and AI knowledge storage, SIOD can scale from a simple monitoring dashboard into a complete Infrastructure Operations Platform.
