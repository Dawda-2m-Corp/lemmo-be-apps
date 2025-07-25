# Healthcare Logistics Frontend Workflow

This document provides a comprehensive guide for frontend developers working with the Lemmo Healthcare Logistics System. It covers the complete workflow, API endpoints, data structures, and best practices.

## 📋 Table of Contents

1. [System Overview](#system-overview)
2. [Authentication Workflow](#authentication-workflow)
3. [Dashboard Workflow](#dashboard-workflow)
4. [Inventory Management Workflow](#inventory-management-workflow)
5. [Logistics Workflow](#logistics-workflow)
6. [Supplier Management Workflow](#supplier-management-workflow)
7. [Facility Management Workflow](#facility-management-workflow)
8. [Requisition Workflow](#requisition-workflow)
9. [Stock Management Workflow](#stock-management-workflow)
10. [API Reference](#api-reference)
11. [Error Handling](#error-handling)
12. [Best Practices](#best-practices)

## 🏥 System Overview

The Lemmo Healthcare Logistics System is a comprehensive platform designed for healthcare facilities to manage their supply chain, inventory, and logistics operations. The system supports multiple user roles with different access levels and responsibilities.

### Key Features

- **Role-based Access Control**: Different interfaces for different healthcare professionals
- **Real-time Tracking**: Live updates for shipments, inventory, and alerts
- **Regulatory Compliance**: FDA/DEA compliance tracking and reporting
- **Emergency Handling**: Priority workflows for urgent situations
- **Analytics Dashboard**: Comprehensive reporting and insights

### User Roles

- **Administrator**: Full system access
- **Pharmacist**: Medication and inventory management
- **Nurse**: Requisition and stock requests
- **Doctor**: Prescription and medication requests
- **Logistics Manager**: Shipment and vehicle management
- **Warehouse Manager**: Inventory and stock management
- **Supply Chain Specialist**: Supplier and contract management
- **Inventory Clerk**: Basic inventory operations
- **Dispatcher**: Shipment assignment and tracking
- **Driver**: Delivery tracking and updates

## 🔐 Authentication Workflow

### Login Process

```javascript
// 1. User enters credentials
const loginData = {
  email: "user@healthcare.com",
  password: "secure_password",
};

// 2. Authenticate via GraphQL
const LOGIN_MUTATION = `
  mutation Login($email: String!, $password: String!) {
    tokenAuth(email: $email, password: $password) {
      token
      user {
        id
        email
        role
        firstName
        lastName
        department
      }
    }
  }
`;

// 3. Store token and user info
localStorage.setItem("authToken", response.data.tokenAuth.token);
localStorage.setItem("userInfo", JSON.stringify(response.data.tokenAuth.user));
```

### Session Management

```javascript
// Check if user is authenticated
const isAuthenticated = () => {
  const token = localStorage.getItem("authToken");
  return token && !isTokenExpired(token);
};

// Get user role for conditional rendering
const getUserRole = () => {
  const userInfo = JSON.parse(localStorage.getItem("userInfo") || "{}");
  return userInfo.role;
};

// Logout
const logout = () => {
  localStorage.removeItem("authToken");
  localStorage.removeItem("userInfo");
  // Redirect to login
};
```

### Role-based Navigation

```javascript
const getNavigationItems = (userRole) => {
  const navigationMap = {
    PHARMACIST: [
      { label: "Inventory", path: "/inventory" },
      { label: "Medications", path: "/medications" },
      { label: "Batch Tracking", path: "/batches" },
      { label: "Compliance", path: "/compliance" },
    ],
    LOGISTICS_MANAGER: [
      { label: "Shipments", path: "/shipments" },
      { label: "Vehicles", path: "/vehicles" },
      { label: "Routes", path: "/routes" },
      { label: "Tracking", path: "/tracking" },
    ],
    NURSE: [
      { label: "Requisitions", path: "/requisitions" },
      { label: "Stock Requests", path: "/stock-requests" },
      { label: "Emergency Requests", path: "/emergency" },
    ],
  };
  return navigationMap[userRole] || [];
};
```

## 📊 Dashboard Workflow

### Main Dashboard

```javascript
// Fetch dashboard overview data
const DASHBOARD_QUERY = `
  query DashboardOverview {
    dashboardOverview
    alerts
    inventoryOverview
    logisticsOverview
    supplierOverview
    facilityOverview
  }
`;

// Real-time updates
const subscribeToUpdates = () => {
  // WebSocket connection for real-time alerts
  const ws = new WebSocket("ws://localhost:8000/ws/dashboard/");

  ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    updateDashboard(data);
  };
};
```

### Alert System

```javascript
// Display alerts based on priority
const displayAlerts = (alerts) => {
  const alertTypes = {
    LOW_STOCK: { color: "orange", icon: "warning" },
    EXPIRING_PRODUCT: { color: "red", icon: "clock" },
    EMERGENCY_SHIPMENT: { color: "red", icon: "emergency" },
    MAINTENANCE_DUE: { color: "yellow", icon: "tools" },
  };

  alerts.forEach((alert) => {
    showNotification(alert.message, alertTypes[alert.type]);
  });
};
```

## 📦 Inventory Management Workflow

### Product Management

```javascript
// Fetch products with filters
const PRODUCTS_QUERY = `
  query Products($category: UUID, $productType: String, $isActive: Boolean) {
    products(categoryId: $category, productType: $productType, isActive: $isActive) {
      id
      name
      description
      productType
      stockQuantity
      price
      genericName
      brandName
      ndcCode
      controlledSubstance
      storageType
      expirationDateRequired
      isLowStock
      isOutOfStock
    }
  }
`;

// Create new product
const CREATE_PRODUCT_MUTATION = `
  mutation CreateProduct($input: CreateProductInput!) {
    createProduct(input: $input) {
      product {
        id
        name
        productType
      }
      success
      message
    }
  }
`;
```

### Batch Tracking

```javascript
// Track product batches
const BATCHES_QUERY = `
  query ProductBatches($productId: UUID) {
    productBatches(productId: $productId) {
      id
      batchNumber
      lotNumber
      quantity
      remainingQuantity
      manufacturingDate
      expirationDate
      isExpired
      isExpiringSoon
      qualityControlPassed
    }
  }
`;

// Quality control check
const QUALITY_CHECK_MUTATION = `
  mutation QualityControlCheck($id: UUID!, $passed: Boolean!, $notes: String) {
    qualityControlCheck(id: $id, passed: $passed, notes: $notes) {
      batch {
        id
        qualityControlPassed
      }
      success
      message
    }
  }
`;
```

### Healthcare-Specific Features

```javascript
// FDA compliance tracking
const COMPLIANCE_QUERY = `
  query ComplianceReport {
    complianceReport {
      fdaComplianceRate
      fdaApprovedProducts
      certifiedSuppliers
      licensedFacilities
    }
  }
`;

// Controlled substance tracking
const CONTROLLED_SUBSTANCES_QUERY = `
  query ControlledSubstances {
    products(controlledSubstance: "SCHEDULE_II") {
      id
      name
      ndcCode
      controlledSubstance
      requiresPrescription
      stockQuantity
    }
  }
`;
```

## 🚚 Logistics Workflow

### Shipment Management

```javascript
// Create shipment
const CREATE_SHIPMENT_MUTATION = `
  mutation CreateShipment($input: CreateShipmentInput!) {
    createShipment(input: $input) {
      shipment {
        id
        shipmentNumber
        status
        priority
        originFacility {
          id
          name
        }
        destinationFacility {
          id
          name
        }
        requiresRefrigeration
        isHazardous
      }
      success
      message
    }
  }
`;

// Track shipment
const SHIPMENT_TRACKING_QUERY = `
  query ShipmentTracking($shipmentId: UUID!) {
    shipmentTracking(shipmentId: $shipmentId) {
      id
      eventType
      location
      timestamp
      description
      metadata
    }
  }
`;
```

### Vehicle Management

```javascript
// Vehicle fleet
const VEHICLES_QUERY = `
  query Vehicles($status: String, $isRefrigerated: Boolean) {
    vehicles(status: $status, isRefrigerated: $isRefrigerated) {
      id
      vehicleId
      make
      model
      year
      vehicleType
      status
      isRefrigerated
      hasGpsTracking
      assignedDriver {
        id
        firstName
        lastName
      }
      nextMaintenanceDate
    }
  }
`;

// Maintenance tracking
const MAINTENANCE_QUERY = `
  query VehicleMaintenance($vehicleId: UUID!) {
    vehicleMaintenance(vehicleId: $vehicleId) {
      id
      maintenanceType
      description
      scheduledDate
      completedDate
      status
      cost
      notes
    }
  }
`;
```

### Emergency Handling

```javascript
// Emergency shipments
const EMERGENCY_SHIPMENTS_QUERY = `
  query EmergencyShipments {
    emergencyShipments {
      id
      shipmentNumber
      priority
      originFacility {
        name
      }
      destinationFacility {
        name
      }
      estimatedDeliveryTime
      status
    }
  }
`;

// Priority routing
const createEmergencyShipment = async (shipmentData) => {
  const response = await graphqlRequest(
    `
    mutation CreateEmergencyShipment($input: CreateShipmentInput!) {
      createShipment(input: $input) {
        shipment {
          id
          priority
          status
        }
        success
        message
      }
    }
  `,
    { input: { ...shipmentData, priority: "EMERGENCY" } }
  );

  // Trigger immediate dispatch
  if (response.data.createShipment.success) {
    await dispatchEmergencyShipment(response.data.createShipment.shipment.id);
  }
};
```

## 🏢 Supplier Management Workflow

### Supplier Directory

```javascript
// Supplier listing
const SUPPLIERS_QUERY = `
  query Suppliers($supplierType: String, $isActive: Boolean) {
    suppliers(supplierType: $supplierType, isActive: $isActive) {
      id
      name
      supplierType
      status
      isPreferred
      qualityRating
      reliabilityRating
      fdaRegistrationNumber
      deaRegistrationNumber
      contactInfo {
        phone
        email
        address
      }
    }
  }
`;

// Supplier performance
const SUPPLIER_PERFORMANCE_QUERY = `
  query SupplierPerformance($supplierId: UUID!) {
    supplierRatings(supplierId: $supplierId) {
      id
      ratingType
      score
      comments
      date
    }
  }
`;
```

### Purchase Orders

```javascript
// Create purchase order
const CREATE_PURCHASE_ORDER_MUTATION = `
  mutation CreatePurchaseOrder($input: CreatePurchaseOrderInput!) {
    createPurchaseOrder(input: $input) {
      purchaseOrder {
        id
        poNumber
        supplier {
          name
        }
        status
        totalAmount
        requestedBy {
          firstName
          lastName
        }
        requestedDate
      }
      success
      message
    }
  }
`;

// Purchase order workflow
const purchaseOrderWorkflow = {
  DRAFT: "Draft",
  SUBMITTED: "Submitted for Approval",
  APPROVED: "Approved",
  ORDERED: "Ordered",
  RECEIVED: "Received",
  CANCELLED: "Cancelled",
};
```

### Contract Management

```javascript
// Active contracts
const ACTIVE_CONTRACTS_QUERY = `
  query ActiveContracts {
    activeContracts {
      id
      contractNumber
      supplier {
        name
      }
      contractType
      startDate
      endDate
      totalValue
      status
      performanceScore
    }
  }
`;

// Contract terms
const CONTRACT_TERMS_QUERY = `
  query ContractTerms($contractId: UUID!) {
    contractTerms(contractId: $contractId) {
      id
      termType
      description
      value
      effectiveDate
    }
  }
`;
```

## 🏥 Facility Management Workflow

### Facility Directory

```javascript
// Facility listing
const FACILITIES_QUERY = `
  query Facilities($category: String, $operationalStatus: String) {
    facilities(category: $category, operationalStatus: $operationalStatus) {
      id
      name
      category
      operationalStatus
      address
      city
      state
      phone
      email
      bedCount
      hasPharmacy
      hasLaboratory
      emergencyServices
      licenseNumber
      licenseExpiryDate
    }
  }
`;

// Healthcare-specific facilities
const HEALTHCARE_FACILITIES_QUERY = `
  query HealthcareFacilities {
    hospitals {
      id
      name
      bedCount
      traumaCenterLevel
    }
    pharmacies {
      id
      name
      hasCompounding
    }
    laboratories {
      id
      name
      accreditation
    }
  }
`;
```

### Department Management

```javascript
// Facility departments
const DEPARTMENTS_QUERY = `
  query FacilityDepartments($facilityId: UUID!) {
    facilityDepartments(facilityId: $facilityId) {
      id
      name
      description
      departmentHead
      phone
      email
      isActive
    }
  }
`;

// Department contacts
const DEPARTMENT_CONTACTS_QUERY = `
  query DepartmentContacts($departmentId: UUID!) {
    departmentContacts(departmentId: $departmentId) {
      id
      name
      title
      contactType
      phone
      email
      isPrimary
    }
  }
`;
```

## 📋 Requisition Workflow

### Create Requisition

```javascript
// New requisition
const CREATE_REQUISITION_MUTATION = `
  mutation CreateRequisition($input: CreateRequisitionInput!) {
    createRequisition(input: $input) {
      requisition {
        id
        requisitionNumber
        status
        priority
        requestedBy {
          firstName
          lastName
          role
        }
        requestedFacility {
          name
        }
        requestedDate
        requiredDate
        reason
      }
      success
      message
    }
  }
`;

// Requisition workflow states
const requisitionWorkflow = {
  DRAFT: "Draft",
  SUBMITTED: "Submitted",
  UNDER_REVIEW: "Under Review",
  APPROVED: "Approved",
  REJECTED: "Rejected",
  FULFILLED: "Fulfilled",
};
```

### Approval Process

```javascript
// Approve requisition
const APPROVE_REQUISITION_MUTATION = `
  mutation ApproveRequisition($id: UUID!, $comments: String) {
    approveRequisition(id: $id, comments: $comments) {
      requisition {
        id
        status
        approvedBy {
          firstName
          lastName
        }
        approvedDate
      }
      success
      message
    }
  }
`;

// Reject requisition
const REJECT_REQUISITION_MUTATION = `
  mutation RejectRequisition($id: UUID!, $reason: String!) {
    rejectRequisition(id: $id, reason: $reason) {
      requisition {
        id
        status
        rejectedBy {
          firstName
          lastName
        }
        rejectedDate
        rejectionReason
      }
      success
      message
    }
  }
`;
```

### Emergency Requisitions

```javascript
// Emergency request
const createEmergencyRequisition = async (requisitionData) => {
  const emergencyData = {
    ...requisitionData,
    priority: "EMERGENCY",
    requiredDate: new Date(Date.now() + 24 * 60 * 60 * 1000), // 24 hours
  };

  const response = await graphqlRequest(CREATE_REQUISITION_MUTATION, {
    input: emergencyData,
  });

  if (response.data.createRequisition.success) {
    // Trigger immediate approval for emergency requests
    await autoApproveEmergencyRequisition(
      response.data.createRequisition.requisition.id
    );
  }
};
```

## 📊 Stock Management Workflow

### Stock Levels

```javascript
// Stock overview
const STOCK_QUERY = `
  query Stock($productId: UUID, $facilityId: UUID) {
    stock(productId: $productId, facilityId: $facilityId) {
      id
      product {
        name
        productType
      }
      facility {
        name
      }
      quantity
      unitCost
      reorderPoint
      maxStockLevel
      lastUpdated
      isLowStock
      isOutOfStock
    }
  }
`;

// Stock alerts
const STOCK_ALERTS_QUERY = `
  query StockAlerts {
    lowStock {
      id
      product {
        name
      }
      quantity
      reorderPoint
    }
    outOfStock {
      id
      product {
        name
      }
    }
    expiringStock {
      id
      product {
        name
      }
      expirationDate
    }
  }
`;
```

### Stock Transactions

```javascript
// Stock transactions
const STOCK_TRANSACTIONS_QUERY = `
  query StockTransactions($stockId: UUID!) {
    stockTransactions(stockId: $stockId) {
      id
      transactionType
      quantity
      unitCost
      totalAmount
      reference
      notes
      createdBy {
        firstName
        lastName
      }
      createdAt
    }
  }
`;

// Create transaction
const CREATE_TRANSACTION_MUTATION = `
  mutation CreateStockTransaction($input: CreateStockTransactionInput!) {
    createStockTransaction(input: $input) {
      transaction {
        id
        transactionType
        quantity
        totalAmount
      }
      success
      message
    }
  }
`;
```

## 🔌 API Reference

### GraphQL Endpoint

```
POST /graphql/
Content-Type: application/json
Authorization: Bearer <token>
```

### REST Endpoints

#### Authentication

```
POST /api/auth/login/
POST /api/auth/logout/
GET /api/auth/user/
```

#### Inventory

```
GET /api/inventory/products/
POST /api/inventory/products/
GET /api/inventory/products/{id}/
PUT /api/inventory/products/{id}/
DELETE /api/inventory/products/{id}/
```

#### Logistics

```
GET /api/logistics/shipments/
POST /api/logistics/shipments/
GET /api/logistics/shipments/{id}/
PUT /api/logistics/shipments/{id}/
```

#### Suppliers

```
GET /api/supplier/suppliers/
POST /api/supplier/suppliers/
GET /api/supplier/suppliers/{id}/
PUT /api/supplier/suppliers/{id}/
```

### WebSocket Connections

```javascript
// Real-time updates
const ws = new WebSocket("ws://localhost:8000/ws/dashboard/");

ws.onopen = () => {
  console.log("Connected to real-time updates");
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  handleRealTimeUpdate(data);
};
```

## ⚠️ Error Handling

### GraphQL Errors

```javascript
const handleGraphQLError = (error) => {
  if (error.graphQLErrors) {
    error.graphQLErrors.forEach((err) => {
      switch (err.extensions.code) {
        case "UNAUTHENTICATED":
          redirectToLogin();
          break;
        case "PERMISSION_DENIED":
          showPermissionError();
          break;
        case "VALIDATION_ERROR":
          showValidationErrors(err.extensions.validationErrors);
          break;
        default:
          showGenericError(err.message);
      }
    });
  }
};
```

### Network Errors

```javascript
const handleNetworkError = (error) => {
  if (error.networkError) {
    if (error.networkError.statusCode === 401) {
      // Token expired
      refreshToken();
    } else if (error.networkError.statusCode === 403) {
      // Insufficient permissions
      showPermissionDenied();
    } else {
      // Server error
      showServerError();
    }
  }
};
```

### Validation Errors

```javascript
const showValidationErrors = (errors) => {
  errors.forEach((error) => {
    const field = error.field;
    const message = error.message;

    // Highlight field with error
    const fieldElement = document.querySelector(`[name="${field}"]`);
    if (fieldElement) {
      fieldElement.classList.add("error");
      showFieldError(fieldElement, message);
    }
  });
};
```

## 🎯 Best Practices

### State Management

```javascript
// Use Redux or Context API for global state
const initialState = {
  user: null,
  permissions: [],
  notifications: [],
  loading: false,
  errors: [],
};

// Centralized API calls
const apiService = {
  async query(query, variables) {
    try {
      const response = await fetch("/graphql/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${getToken()}`,
        },
        body: JSON.stringify({ query, variables }),
      });

      const data = await response.json();

      if (data.errors) {
        throw new Error(data.errors[0].message);
      }

      return data.data;
    } catch (error) {
      handleError(error);
      throw error;
    }
  },
};
```

### Component Structure

```javascript
// Healthcare-specific components
const HealthcareProvider = ({ children, requiredRole }) => {
  const userRole = getUserRole();

  if (!hasPermission(userRole, requiredRole)) {
    return <PermissionDenied />;
  }

  return children;
};

// Usage
<HealthcareProvider requiredRole="PHARMACIST">
  <MedicationManagement />
</HealthcareProvider>;
```

### Real-time Updates

```javascript
// WebSocket connection for real-time data
const useRealTimeUpdates = (subscription) => {
  const [data, setData] = useState(null);

  useEffect(() => {
    const ws = new WebSocket("ws://localhost:8000/ws/");

    ws.onopen = () => {
      ws.send(JSON.stringify({ type: "subscribe", subscription }));
    };

    ws.onmessage = (event) => {
      const update = JSON.parse(event.data);
      setData(update);
    };

    return () => ws.close();
  }, [subscription]);

  return data;
};
```

### Security Considerations

```javascript
// Token management
const tokenManager = {
  getToken() {
    return localStorage.getItem("authToken");
  },

  setToken(token) {
    localStorage.setItem("authToken", token);
  },

  removeToken() {
    localStorage.removeItem("authToken");
  },

  isTokenValid() {
    const token = this.getToken();
    if (!token) return false;

    try {
      const payload = JSON.parse(atob(token.split(".")[1]));
      return payload.exp * 1000 > Date.now();
    } catch {
      return false;
    }
  },
};

// Auto-refresh token
setInterval(() => {
  if (tokenManager.isTokenValid()) {
    refreshToken();
  }
}, 5 * 60 * 1000); // Every 5 minutes
```

### Performance Optimization

```javascript
// Lazy loading for large components
const InventoryManagement = lazy(() => import("./InventoryManagement"));
const LogisticsTracking = lazy(() => import("./LogisticsTracking"));

// Memoization for expensive calculations
const useInventoryStats = (products) => {
  return useMemo(() => {
    return {
      totalProducts: products.length,
      lowStockCount: products.filter((p) => p.isLowStock).length,
      outOfStockCount: products.filter((p) => p.isOutOfStock).length,
      totalValue: products.reduce(
        (sum, p) => sum + p.stockQuantity * p.price,
        0
      ),
    };
  }, [products]);
};

// Debounced search
const useDebouncedSearch = (callback, delay) => {
  const [searchTerm, setSearchTerm] = useState("");

  const debouncedCallback = useCallback(debounce(callback, delay), [
    callback,
    delay,
  ]);

  useEffect(() => {
    debouncedCallback(searchTerm);
  }, [searchTerm, debouncedCallback]);

  return [searchTerm, setSearchTerm];
};
```

## 📱 Mobile Considerations

### Responsive Design

```css
/* Mobile-first approach */
.container {
  padding: 1rem;
}

@media (min-width: 768px) {
  .container {
    padding: 2rem;
  }
}

/* Touch-friendly buttons */
.button {
  min-height: 44px;
  min-width: 44px;
  padding: 12px 16px;
}
```

### Offline Support

```javascript
// Service worker for offline functionality
const cacheInventoryData = async () => {
  const cache = await caches.open("inventory-cache");
  const response = await fetch("/api/inventory/products/");
  await cache.put("/api/inventory/products/", response);
};

// Sync when online
window.addEventListener("online", () => {
  syncOfflineData();
});
```

This workflow provides a comprehensive guide for frontend developers to integrate with the Lemmo Healthcare Logistics System. The system is designed to be scalable, secure, and compliant with healthcare regulations while providing an excellent user experience.
