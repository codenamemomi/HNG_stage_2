# Country Currency & Exchange API

A FastAPI-based REST API service that provides comprehensive country data including currencies, exchange rates, population, and estimated GDP calculations. The service fetches real-time data from external APIs, stores it in a MySQL database, and offers various endpoints for querying and managing country information.

## Features

- **Real-time Data Fetching**: Automatically fetches country data from REST Countries API and exchange rates from Open Exchange Rates API
- **Estimated GDP Calculation**: Computes estimated GDP based on population and exchange rates with randomization for realistic values
- **Comprehensive Filtering**: Filter countries by region, currency, and sort by GDP
- **Data Visualization**: Generates and serves summary images showing top 5 countries by GDP
- **CRUD Operations**: Full CRUD operations for country data management
- **Async Database Operations**: Uses async SQLAlchemy with MySQL for high performance
- **Automatic Data Refresh**: Endpoint to refresh all country data from external sources
- **Status Monitoring**: Health check endpoint with data freshness information

## Tech Stack

- **Framework**: FastAPI
- **Database**: MySQL with async SQLAlchemy
- **ORM**: SQLAlchemy 2.0
- **Async DB Driver**: aiomysql
- **HTTP Client**: httpx
- **Data Validation**: Pydantic
- **Logging**: Loguru
- **Image Generation**: Matplotlib
- **ASGI Server**: Uvicorn

## Installation

### Prerequisites

- Python 3.8+
- MySQL 8.0+
- pip

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/codenamemomi/HNG_stage_2
   cd HNG_stage_2
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up MySQL database**
   ```sql
   CREATE DATABASE countrydb;
   ```

5. **Configure environment variables**

   Create a `.env` file in the root directory:
   ```env
   DB_USER=root
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=3306
   DB_NAME=countrydb

   # Optional: Override default API URLs
   COUNTRIES_API=https://restcountries.com/v2/all?fields=name,capital,region,population,flag,currencies
   EXCHANGE_API=https://open.er-api.com/v6/latest/USD
   ```

6. **Run database migrations**
   ```bash
   python main.py  # This will create tables automatically via SQLAlchemy
   ```

## Running the Application

### Development Server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production Server

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

The API will be available at `http://localhost:8000`

## API Documentation

### Interactive API Docs

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Endpoints

#### Status
- **GET** `/status`
  - Returns total number of countries and last refresh timestamp

#### Countries

- **POST** `/countries/refresh`
  - Refreshes all country data from external APIs
  - Returns refresh status and timestamp

- **GET** `/countries/`
  - Get all countries with optional filtering
  - Query Parameters:
    - `region` (string): Filter by region (case-insensitive)
    - `currency` (string): Filter by currency code (case-insensitive)
    - `sort` (string): Sort by GDP (`gdp_asc` or `gdp_desc`)

- **GET** `/countries/image`
  - Returns a PNG image showing top 5 countries by estimated GDP

- **GET** `/countries/{name}`
  - Get a specific country by name (case-insensitive)

- **DELETE** `/countries/{name}`
  - Delete a country by name (case-insensitive)

## Usage Examples

### Get All Countries
```bash
curl http://localhost:8000/countries/
```

### Filter by Region
```bash
curl "http://localhost:8000/countries/?region=europe"
```

### Filter by Currency and Sort by GDP
```bash
curl "http://localhost:8000/countries/?currency=usd&sort=gdp_desc"
```

### Get Specific Country
```bash
curl "http://localhost:8000/countries/united%20states"
```

### Refresh Data
```bash
curl -X POST http://localhost:8000/countries/refresh
```

### Get Status
```bash
curl http://localhost:8000/status
```

### Get Summary Image
```bash
curl http://localhost:8000/countries/image -o summary.png
```

## Database Schema

### Countries Table

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| name | VARCHAR(100) | Country name (unique) |
| capital | VARCHAR(100) | Capital city |
| region | VARCHAR(100) | Geographic region |
| population | INTEGER | Population count |
| currency_code | VARCHAR(10) | ISO currency code |
| exchange_rate | FLOAT | Exchange rate to USD |
| estimated_gdp | FLOAT | Calculated GDP estimate |
| flag_url | VARCHAR(255) | URL to country flag |
| last_refreshed_at | DATETIME | Last data refresh timestamp |

## Data Sources

- **Countries Data**: [REST Countries API](https://restcountries.com/)
- **Exchange Rates**: [Open Exchange Rates API](https://open.er-api.com/)

## Development

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
# Using black (if configured)
black .

# Using isort for imports
isort .
```

### Database Migrations

The application uses SQLAlchemy's `create_all()` for table creation. For production deployments, consider using Alembic for proper migration management.

## Deployment

### Docker (Recommended)

1. **Build the image**
   ```bash
   docker build -t country-api .
   ```

2. **Run with Docker Compose**
   ```yaml
   # docker-compose.yml
   version: '3.8'
   services:
     db:
       image: mysql:8.0
       environment:
         MYSQL_ROOT_PASSWORD: password
         MYSQL_DATABASE: countrydb
       ports:
         - "3306:3306"

     api:
       build: .
       ports:
         - "8000:8000"
       depends_on:
         - db
       environment:
         - DB_HOST=db
   ```

   ```bash
   docker-compose up -d
   ```

### Environment Variables Reference

| Variable | Default | Description |
|----------|---------|-------------|
| APP_NAME | Country Currency & Exchange API | Application name |
| VERSION | 1.0.0 | API version |
| DB_USER | root | MySQL username |
| DB_PASSWORD | password | MySQL password |
| DB_HOST | localhost | MySQL host |
| DB_PORT | 3306 | MySQL port |
| DB_NAME | countrydb | MySQL database name |
| COUNTRIES_API | REST Countries API URL | External countries API |
| EXCHANGE_API | Open Exchange Rates API URL | External exchange rates API |

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, email support@example.com or create an issue in the repository.

---

**Note**: This API is for educational and demonstration purposes. Exchange rates and GDP calculations are estimates and should not be used for financial decisions.
