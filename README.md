# Quality Gates Service

A service for checking the quality of information systems

## 🚀 Quick Start

### Running the Service

To start the service on development mode, run:
```bash
uvicorn api.main:app --reload
```

### Docker Deployment

```bash
# Build the image
docker build -t quality-gates .

# Run with default settings (starts the server)
docker run -p 8000:8000 quality-gates

# Run migrations only
docker run quality-gates migrate

# Run server only
docker run -p 8000:8000 quality-gates run
```

## 📋 Overview

The service stores a list of information systems in the database and checks their quality based on a list of checks.

Quality checks are performed within CI/CD using GitLab CI, and then a POST request updates the list of services and their status in the database.

## ⚙️ Configuration

### Environment Variables

| Variable | Type | Description |
|----------|------|-------------|
| `API_TOKEN` | `str` | Authentication token for the service |
| `DB_DSN` | `str` | Database connection string: `postgresql://user:password@host:5432/db_name` |
| `HOST` | `str` | Server host (default: `0.0.0.0`) |
| `PORT` | `int` | Server port (default: `8000`) |
| `DEBUG` | `bool` | Debug mode (default: `false`) |
| `SWAGGER` | `bool` | Enable Swagger UI (default: `false`) |

## 🔌 API Endpoints

### POST `/monitoring/update`

Update the list of services and their status using API token.

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `information_system` | `str` | Name of the information system |
| `service_name` | `str` | Name of the service |
| `monitoring` | `bool` | Quality check status |

#### Example Request

```bash
curl -X POST http://localhost:8000/monitoring/update?token=$API_TOKEN \
  -H "Content-Type: application/json" \
  -d '{
    "information_system": "test",
    "service_name": "test",
    "monitoring": true
  }'
```

### GET `/monitoring/status/{information_system}`

Get a list of services in the information system.

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `information_system` | `str` | Name of the information system |

#### Example Request

```bash
curl -X GET http://localhost:8000/monitoring/status/test
```

### GET `/monitoring/all_services`

Get a list of all services.

#### Example Request

```bash
curl -X GET http://localhost:8000/monitoring/all_services
```

### GET `/health`

Health check endpoint.

```bash
curl -X GET http://localhost:8000/health
```

## 📚 Documentation

### Swagger UI

Swagger documentation is available at: http://localhost:8000/docs

### API Documentation

ReDoc documentation is available at: http://localhost:8000/redoc

## 🗄️ Database Management

### Creating New Migrations

To create a new migration, run:
```bash
alembic revision --autogenerate -m "your migration message"
```

### Running Migrations

```bash
# Run all pending migrations
alembic upgrade head

# Or using Python module
python -m quality_gates migrate
```

## 🔍 Quality Assurance

Quality checks for information systems are performed within CI/CD using GitLab CI.

The service integrates with your CI/CD pipeline to:
- ✅ Monitor service health
- ✅ Track quality metrics
- ✅ Update service status automatically
- ✅ Provide real-time quality insights

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   GitLab CI     │───▶│  Quality Gates  │───▶│   PostgreSQL    │
│                 │    │     Service     │    │   Database      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📦 Development

### Prerequisites

- Python 3.12+
- PostgreSQL
- Docker (optional)

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd quality-gates
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   export API_TOKEN="your-api-token"
   export DB_DSN="postgresql://user:password@host:5432/db_name"
   ```

4. **Run migrations**
   ```bash
   python -m quality_gates migrate
   ```

5. **Start the development server**
   ```bash
   python -m quality_gates run
   ```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request