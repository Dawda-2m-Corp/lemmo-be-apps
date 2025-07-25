# Data Generation Management Commands

This document provides comprehensive documentation for the Django management commands used to generate fake test data for the Lemmo Healthcare Logistics System.

## 📋 Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Available Commands](#available-commands)
5. [Usage Examples](#usage-examples)
6. [Data Relationships](#data-relationships)
7. [Healthcare-Specific Data](#healthcare-specific-data)
8. [Troubleshooting](#troubleshooting)

## 🎯 Overview

The system includes Django management commands that use the **Faker** library to generate realistic test data for all major components of the healthcare logistics system. These commands are designed to create interconnected data that mimics real-world scenarios.

### Key Features

- **Realistic Data**: Uses Faker to generate realistic names, addresses, phone numbers, etc.
- **Healthcare-Specific**: Includes healthcare-specific fields like FDA registration, medical certifications, etc.
- **Interconnected**: Creates relationships between different entities (users, facilities, products, etc.)
- **Configurable**: Allows you to specify the number of records to generate
- **Safe**: Includes `--clear` option to safely clear existing data

## 🔧 Prerequisites

### Required Dependencies

Add the following to your `requirements.txt`:

```txt
Faker==19.3.1
```

### Installation

```bash
pip install Faker
```

## 📊 Available Commands

### 1. Authentication Data Generation

**Command**: `generate_users`

**Purpose**: Generates users, user sessions, and user activities for testing authentication and user management.

**Location**: `lemmo_apps/authentication/management/commands/generate_users.py`

#### Parameters

| Parameter      | Type | Default | Description                           |
| -------------- | ---- | ------- | ------------------------------------- |
| `--users`      | int  | 10      | Number of users to create             |
| `--sessions`   | int  | 50      | Number of user sessions to create     |
| `--activities` | int  | 100     | Number of user activities to create   |
| `--clear`      | flag | False   | Clear existing data before generating |

#### Generated Data

- **Users**: Healthcare professionals with roles (Pharmacist, Nurse, Doctor, etc.)
- **User Sessions**: Login sessions with IP addresses and user agents
- **User Activities**: Activity logs for audit trails

#### Healthcare Features

- Role-based user generation (ADMIN, PHARMACIST, NURSE, DOCTOR, etc.)
- Professional license numbers
- Department assignments
- Employee IDs
- Healthcare-specific activity types

### 2. Inventory Data Generation

**Command**: `generate_inventory`

**Purpose**: Generates product categories, products, and product batches for inventory management testing.

**Location**: `lemmo_apps/inventory/management/commands/generate_inventory.py`

#### Parameters

| Parameter      | Type | Default | Description                            |
| -------------- | ---- | ------- | -------------------------------------- |
| `--categories` | int  | 20      | Number of product categories to create |
| `--products`   | int  | 100     | Number of products to create           |
| `--batches`    | int  | 200     | Number of product batches to create    |
| `--clear`      | flag | False   | Clear existing data before generating  |

#### Generated Data

- **Product Categories**: Hierarchical product categorization
- **Products**: Healthcare products with detailed specifications
- **Product Batches**: Batch tracking with expiration dates

#### Healthcare Features

- FDA approval tracking
- NDC codes for medications
- Controlled substance classifications
- Temperature storage requirements
- Expiration date management
- Quality control tracking

### 3. Location Data Generation

**Command**: `generate_locations`

**Purpose**: Generates facility types, facilities, departments, and contacts for location management.

**Location**: `lemmo_apps/location/management/commands/generate_locations.py`

#### Parameters

| Parameter          | Type | Default | Description                              |
| ------------------ | ---- | ------- | ---------------------------------------- |
| `--facility-types` | int  | 10      | Number of facility types to create       |
| `--facilities`     | int  | 50      | Number of facilities to create           |
| `--departments`    | int  | 100     | Number of facility departments to create |
| `--contacts`       | int  | 150     | Number of facility contacts to create    |
| `--clear`          | flag | False   | Clear existing data before generating    |

#### Generated Data

- **Facility Types**: Hospital, Clinic, Pharmacy, Laboratory, etc.
- **Facilities**: Healthcare facilities with detailed information
- **Departments**: Medical departments within facilities
- **Contacts**: Contact information for facilities

#### Healthcare Features

- Healthcare facility categories (Hospital, Clinic, Pharmacy, etc.)
- Bed count and capacity management
- Operating rooms and emergency services
- Licensing and accreditation tracking
- Specialty services
- Storage capacity (refrigeration, freezer)

### 4. Supplier Data Generation

**Command**: `generate_suppliers`

**Purpose**: Generates suppliers, contacts, ratings, purchase orders, and contracts for supplier management.

**Location**: `lemmo_apps/supplier/management/commands/generate_suppliers.py`

#### Parameters

| Parameter           | Type | Default | Description                           |
| ------------------- | ---- | ------- | ------------------------------------- |
| `--suppliers`       | int  | 30      | Number of suppliers to create         |
| `--contacts`        | int  | 60      | Number of supplier contacts to create |
| `--ratings`         | int  | 100     | Number of supplier ratings to create  |
| `--purchase-orders` | int  | 50      | Number of purchase orders to create   |
| `--contracts`       | int  | 20      | Number of contracts to create         |
| `--clear`           | flag | False   | Clear existing data before generating |

#### Generated Data

- **Suppliers**: Healthcare suppliers with detailed profiles
- **Supplier Contacts**: Contact information for suppliers
- **Supplier Ratings**: Performance ratings and reviews
- **Purchase Orders**: Procurement orders with items
- **Contracts**: Supplier agreements with terms

#### Healthcare Features

- FDA and DEA registration numbers
- Healthcare certifications (ISO, GMP, etc.)
- Medical specialties and product categories
- Quality and reliability ratings
- Healthcare-specific contract terms

### 5. Logistics Data Generation

**Command**: `generate_logistics`

**Purpose**: Generates vehicles, drivers, routes, and shipments for logistics management.

**Location**: `lemmo_apps/logistics/management/commands/generate_logistics.py`

#### Parameters

| Parameter     | Type | Default | Description                           |
| ------------- | ---- | ------- | ------------------------------------- |
| `--vehicles`  | int  | 20      | Number of vehicles to create          |
| `--drivers`   | int  | 15      | Number of drivers to create           |
| `--routes`    | int  | 30      | Number of routes to create            |
| `--shipments` | int  | 50      | Number of shipments to create         |
| `--clear`     | flag | False   | Clear existing data before generating |

#### Generated Data

- **Vehicles**: Fleet vehicles with specifications
- **Drivers**: Licensed drivers with certifications
- **Routes**: Delivery routes with stops
- **Shipments**: Shipments with tracking information

#### Healthcare Features

- Refrigerated transport capabilities
- Medical transport certifications
- Hazardous materials handling
- Temperature monitoring
- Emergency response training
- Healthcare-specific vehicle types (Ambulance, etc.)

## 🚀 Usage Examples

### Basic Usage

Generate default amounts of data for all modules:

```bash
# Generate users and authentication data
python manage.py generate_users

# Generate inventory data
python manage.py generate_inventory

# Generate location data
python manage.py generate_locations

# Generate supplier data
python manage.py generate_suppliers

# Generate logistics data
python manage.py generate_logistics
```

### Custom Amounts

Generate specific amounts of data:

```bash
# Generate 50 users, 200 sessions, 500 activities
python manage.py generate_users --users 50 --sessions 200 --activities 500

# Generate 200 products, 50 categories, 500 batches
python manage.py generate_inventory --products 200 --categories 50 --batches 500

# Generate 100 facilities, 200 departments
python manage.py generate_locations --facilities 100 --departments 200

# Generate 100 suppliers, 200 purchase orders
python manage.py generate_suppliers --suppliers 100 --purchase-orders 200

# Generate 50 vehicles, 30 drivers, 100 shipments
python manage.py generate_logistics --vehicles 50 --drivers 30 --shipments 100
```

### Clear and Regenerate

Clear existing data and generate fresh data:

```bash
# Clear all data and generate fresh test data
python manage.py generate_users --clear
python manage.py generate_inventory --clear
python manage.py generate_locations --clear
python manage.py generate_suppliers --clear
python manage.py generate_logistics --clear
```

### Sequential Generation

Generate data in the correct order for proper relationships:

```bash
# 1. Generate users first (required for other commands)
python manage.py generate_users --users 20

# 2. Generate locations (facilities needed for logistics)
python manage.py generate_locations --facilities 30

# 3. Generate inventory (products needed for suppliers)
python manage.py generate_inventory --products 100

# 4. Generate suppliers (needs users and products)
python manage.py generate_suppliers --suppliers 20

# 5. Generate logistics (needs users and facilities)
python manage.py generate_logistics --vehicles 15 --drivers 10
```

## 🔗 Data Relationships

### Dependencies

The commands have the following dependencies:

1. **Users** → Required by all other commands
2. **Facilities** → Required by logistics commands
3. **Products** → Required by supplier commands

### Recommended Generation Order

```bash
# 1. Authentication (Users)
python manage.py generate_users

# 2. Location (Facilities)
python manage.py generate_locations

# 3. Inventory (Products)
python manage.py generate_inventory

# 4. Supplier (needs Users + Products)
python manage.py generate_suppliers

# 5. Logistics (needs Users + Facilities)
python manage.py generate_logistics
```

## 🏥 Healthcare-Specific Data

### Authentication Data

- **User Roles**: ADMIN, PHARMACIST, NURSE, DOCTOR, LOGISTICS_MANAGER, etc.
- **Professional Licenses**: License numbers for healthcare professionals
- **Departments**: Medical departments and specialties
- **Activity Types**: Healthcare-specific activities (LOGIN, APPROVE, DISPATCH, etc.)

### Inventory Data

- **Product Types**: MEDICATION, MEDICAL_SUPPLY, EQUIPMENT, VACCINE, etc.
- **FDA Compliance**: FDA approval dates and registration numbers
- **Controlled Substances**: Schedule I-V classifications
- **Storage Requirements**: Refrigeration, temperature monitoring
- **NDC Codes**: National Drug Codes for medications

### Location Data

- **Facility Types**: Hospital, Clinic, Pharmacy, Laboratory, etc.
- **Healthcare Services**: Emergency services, trauma centers, specialty services
- **Licensing**: Healthcare facility licenses and accreditations
- **Storage Capacity**: Refrigeration and freezer capacity

### Supplier Data

- **FDA Registration**: FDA registration numbers for suppliers
- **DEA Registration**: DEA registration for controlled substances
- **Healthcare Certifications**: ISO 13485, GMP, HACCP, etc.
- **Medical Specialties**: Product category specializations

### Logistics Data

- **Vehicle Types**: Ambulance, Refrigerated Truck, Medical Transport
- **Driver Certifications**: Medical transport, hazardous materials, emergency response
- **Temperature Control**: Refrigerated transport with temperature monitoring
- **Emergency Services**: Emergency response training and capabilities

## 🔧 Troubleshooting

### Common Issues

#### 1. Missing Dependencies

**Error**: `No users found. Please generate users first.`

**Solution**: Generate users first:

```bash
python manage.py generate_users
```

#### 2. Database Constraints

**Error**: Foreign key constraint violations

**Solution**: Generate data in the correct order (see Data Relationships section)

#### 3. Faker Installation

**Error**: `ModuleNotFoundError: No module named 'faker'`

**Solution**: Install Faker:

```bash
pip install Faker
```

#### 4. Memory Issues

**Error**: Out of memory when generating large datasets

**Solution**: Generate data in smaller batches:

```bash
python manage.py generate_users --users 100
python manage.py generate_users --users 100
```

### Performance Tips

1. **Generate in Batches**: For large datasets, generate data in smaller batches
2. **Use Clear Flag**: Use `--clear` to avoid duplicate data
3. **Monitor Progress**: Commands show progress every 10-50 records
4. **Database Optimization**: Consider database optimization for large datasets

### Debugging

#### Enable Verbose Output

```bash
python manage.py generate_users --verbosity 2
```

#### Check Generated Data

```bash
# Check user count
python manage.py shell -c "from lemmo_apps.authentication.models import User; print(User.objects.count())"

# Check product count
python manage.py shell -c "from lemmo_apps.inventory.models.product import Product; print(Product.objects.count())"
```

## 📈 Data Statistics

### Typical Data Volumes

| Command              | Default Records                          | Max Recommended |
| -------------------- | ---------------------------------------- | --------------- |
| `generate_users`     | 10 users, 50 sessions, 100 activities    | 1000 users      |
| `generate_inventory` | 20 categories, 100 products, 200 batches | 5000 products   |
| `generate_locations` | 10 types, 50 facilities, 100 departments | 1000 facilities |
| `generate_suppliers` | 30 suppliers, 50 purchase orders         | 500 suppliers   |
| `generate_logistics` | 20 vehicles, 15 drivers, 50 shipments    | 500 vehicles    |

### Memory Usage

- **Small Dataset** (< 1000 records): ~50MB RAM
- **Medium Dataset** (1000-10000 records): ~200MB RAM
- **Large Dataset** (> 10000 records): ~500MB+ RAM

## 🎯 Best Practices

1. **Start Small**: Begin with default amounts and scale up
2. **Generate Sequentially**: Follow the recommended order
3. **Use Clear Flag**: Avoid duplicate data issues
4. **Monitor Performance**: Watch for memory and performance issues
5. **Backup Database**: Backup before generating large datasets
6. **Test Relationships**: Verify that relationships are created correctly

## 📚 Additional Resources

- [Faker Documentation](https://faker.readthedocs.io/)
- [Django Management Commands](https://docs.djangoproject.com/en/stable/howto/custom-management-commands/)
- [Healthcare Data Standards](https://www.hl7.org/)
- [FDA Data Standards](https://www.fda.gov/industry/fda-data-standards)

---

This documentation provides comprehensive guidance for using the data generation commands. For additional support or questions, please refer to the main project documentation or create an issue in the repository.
