# Lemmo Healthcare Logistics System

A comprehensive Django-based backend system for healthcare logistics and supply chain management. This system is designed to handle the complex requirements of healthcare facilities, including medication management, supplier relationships, transportation, and regulatory compliance.

## 📚 Documentation

- **[Frontend Developer Workflow](./docs/frontend-workflow.md)** - Comprehensive guide for frontend developers integrating with the system

## 🏥 Features

### Core Modules

#### 1. **Authentication & User Management**

- Role-based access control for healthcare professionals
- User activity tracking and session management
- Healthcare-specific roles (Pharmacist, Nurse, Doctor, Logistics Manager, etc.)
- Professional license management
- Department and facility assignments

#### 2. **Inventory Management**

- **Product Management**: Comprehensive product catalog with healthcare-specific fields

  - Medication classifications (controlled substances, prescription requirements)
  - Storage requirements (refrigeration, temperature monitoring)
  - FDA approval tracking and regulatory compliance
  - Batch and lot number tracking
  - Expiration date management
  - NDC codes and manufacturer information

- **Stock Management**:

  - Real-time stock levels
  - Reorder point alerts
  - Low stock notifications
  - Expiration date tracking
  - Quality control integration

- **Product Categories**: Hierarchical categorization system
- **Batch Management**: Complete batch lifecycle tracking

#### 3. **Location & Facility Management**

- **Facility Types**: Hospitals, clinics, pharmacies, laboratories, warehouses
- **Operational Status**: Active, maintenance, construction, closed
- **Healthcare Specific Features**:
  - Bed count and capacity management
  - Operating rooms and emergency rooms
  - Specialty services tracking
  - Storage capacity (refrigeration, freezer)
  - Licensing and accreditation tracking

#### 4. **Supplier Management**

- **Supplier Profiles**: Comprehensive supplier information

  - FDA and DEA registration numbers
  - Certifications and compliance tracking
  - Performance metrics and ratings
  - Financial terms and credit limits

- **Purchase Orders**: Complete procurement workflow

  - Multi-level approval process
  - Priority and emergency ordering
  - Quality control integration
  - Cost tracking and budget management

- **Contract Management**: Supplier agreement tracking
  - Service level agreements
  - Payment terms and schedules
  - Performance monitoring
  - Renewal tracking

#### 5. **Logistics & Transportation**

- **Vehicle Management**:

  - Fleet tracking and maintenance
  - Refrigerated transport capabilities
  - GPS and temperature monitoring
  - Insurance and registration tracking

- **Driver Management**:

  - License and certification tracking
  - Schedule management
  - Performance monitoring
  - Vehicle assignments

- **Shipment Tracking**:
  - Real-time delivery tracking
  - Temperature monitoring for sensitive items
  - Route optimization
  - Delivery confirmation and quality checks

#### 6. **Requisition System**

- **Request Management**: Internal facility requests
  - Multi-level approval workflow
  - Priority classification
  - Budget tracking
  - Status tracking

#### 7. **Stock Management**

- **Transaction Tracking**: Complete audit trail
- **Stock Movements**: Inbound, outbound, transfers
- **Inventory Reconciliation**: Regular stock counts
- **Loss Prevention**: Theft and damage tracking

### Healthcare-Specific Features

#### Regulatory Compliance

- **FDA Compliance**: Approval tracking and documentation
- **DEA Compliance**: Controlled substance management
- **Temperature Control**: Cold chain management
- **Quality Assurance**: GMP and quality standards
- **Documentation**: Complete audit trails

#### Emergency Management

- **Emergency Orders**: Priority processing
- **Critical Stock Alerts**: Real-time notifications
- **Emergency Contacts**: Rapid communication
- **Disaster Response**: Emergency supply management

#### Patient Safety

- **Expiration Management**: Automatic alerts for expiring products
- **Quality Control**: Batch testing and validation
- **Recall Management**: Product recall tracking
- **Patient Tracking**: Medication traceability

## 🚀 Technology Stack

- **Backend**: Django 4.x with Python 3.8+
- **Database**: PostgreSQL (recommended) or SQLite
- **API**: GraphQL with Graphene-Django
- **Authentication**: Django's built-in authentication with custom user model
- **File Storage**: Django's file storage system
- **History Tracking**: django-simple-history
- **Tree Structures**: django-mptt for hierarchical data

## 📋 Installation

### Prerequisites

- Python 3.8 or higher
- PostgreSQL (recommended) or SQLite
- Virtual environment (recommended)

### Setup

1. **Clone the repository**

```bash
git clone <repository-url>
cd lemmo-be-apps
```

2. **Create virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure database**

```bash
# Update settings.py with your database configuration
python manage.py migrate
```

5. **Create superuser**

```bash
python manage.py createsuperuser
```

6. **Run development server**

```bash
python manage.py runserver
```

## 🏗️ Architecture

### App Structure

```
lemmo_apps/
├── authentication/     # User management and authentication
├── inventory/         # Product and stock management
├── location/          # Facility and location management
├── supplier/          # Supplier and procurement management
├── logistics/         # Transportation and delivery
├── requisition/      # Internal request management
├── stock/            # Stock transactions and movements
├── order/            # Order management
├── dashboard/         # Analytics and reporting
├── fhir_api/         # FHIR integration
└── integration/      # Third-party integrations
```

### Key Models

#### User Management

- `User`: Extended user model with healthcare roles
- `UserSession`: Session tracking
- `UserActivity`: Activity logging

#### Inventory

- `Product`: Comprehensive product information
- `ProductCategory`: Hierarchical categorization
- `ProductBatch`: Batch and lot tracking
- `ProductImage`: Product images

#### Facilities

- `Facility`: Healthcare facility management
- `FacilityDepartment`: Department organization
- `FacilityContact`: Contact management

#### Suppliers

- `Supplier`: Supplier profiles and ratings
- `PurchaseOrder`: Procurement workflow
- `Contract`: Supplier agreements

#### Logistics

- `Vehicle`: Fleet management
- `Driver`: Driver management
- `Shipment`: Delivery tracking

## 🔧 Configuration

### Environment Variables

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost/lemmo_db

# Security
SECRET_KEY=your-secret-key
DEBUG=True

# File Storage
MEDIA_ROOT=/path/to/media/files
STATIC_ROOT=/path/to/static/files

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-password
```

### GraphQL Endpoint

The system provides a comprehensive GraphQL API at `/graphql/` with the following main query types:

- **Authentication**: User management and session tracking
- **Inventory**: Product and stock queries
- **Location**: Facility and location management
- **Supplier**: Supplier and procurement data
- **Logistics**: Transportation and delivery tracking

## 📊 Dashboard Features

### Analytics & Reporting

- **Inventory Analytics**: Stock levels, turnover rates, value tracking
- **Supplier Performance**: Delivery times, quality ratings, cost analysis
- **Logistics Metrics**: Delivery times, route efficiency, vehicle utilization
- **Financial Reports**: Cost tracking, budget analysis, ROI calculations
- **Compliance Reports**: Regulatory compliance, audit trails, quality metrics

### Real-time Monitoring

- **Stock Alerts**: Low stock, out of stock, expiring products
- **Quality Alerts**: Failed quality checks, recall notifications
- **Delivery Tracking**: Real-time shipment status
- **Maintenance Alerts**: Vehicle and equipment maintenance schedules

## 🔒 Security & Compliance

### Data Protection

- **Encryption**: Sensitive data encryption
- **Access Control**: Role-based permissions
- **Audit Trails**: Complete activity logging
- **Data Backup**: Regular backup procedures

### Healthcare Compliance

- **HIPAA Compliance**: Patient data protection
- **FDA Compliance**: Medication tracking
- **DEA Compliance**: Controlled substance management
- **Quality Standards**: GMP and quality assurance

## 🚀 Deployment

### Production Setup

1. **Web Server**: Nginx or Apache
2. **Application Server**: Gunicorn or uWSGI
3. **Database**: PostgreSQL with connection pooling
4. **Cache**: Redis for session and query caching
5. **File Storage**: AWS S3 or similar for media files
6. **Monitoring**: Application performance monitoring
7. **Backup**: Automated backup procedures

### Docker Deployment

```bash
# Build and run with Docker
docker-compose up -d
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:

- Create an issue in the repository
- Contact the development team
- Check the documentation

## 🔮 Roadmap

### Planned Features

- **AI/ML Integration**: Predictive analytics for demand forecasting
- **Mobile App**: Native mobile applications
- **IoT Integration**: Smart sensors for temperature monitoring
- **Blockchain**: Supply chain transparency and traceability
- **Advanced Analytics**: Machine learning for optimization
- **Multi-tenant**: Support for multiple healthcare organizations
- **API Integrations**: EHR systems, pharmacy systems, lab systems

### Future Enhancements

- **Telemedicine Integration**: Remote healthcare delivery
- **Vaccine Management**: Specialized vaccine tracking
- **Clinical Trials**: Research and trial management
- **International Support**: Multi-language and multi-currency
- **Advanced Reporting**: Custom report builder
- **Workflow Automation**: Process automation and optimization

---

**Built with ❤️ for Healthcare Logistics**
