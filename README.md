# house-rent-system

> A lightweight full-stack second-hand housing agency management system based on Flask and MySQL

[English](./README.md) | [中文](./README_zh.md)

![GitHub stars](https://img.shields.io/github/stars/killerwy/house-rent-system?style=for-the-badge&logo=github) 
![GitHub forks](https://img.shields.io/github/forks/killerwy/house-rent-system?style=for-the-badge&logo=github) 
![GitHub issues](https://img.shields.io/github/issues/killerwy/house-rent-system?style=for-the-badge&logo=github) 
![Last commit](https://img.shields.io/github/last-commit/killerwy/house-rent-system?style=for-the-badge&logo=github) 
![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3776AB.svg?style=for-the-badge&logo=python&logoColor=white)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E.svg?style=for-the-badge&logo=javascript&logoColor=black)
![CSS](https://img.shields.io/badge/css-%23663399.svg?style=for-the-badge&logo=css&logoColor=white)

## 📑 Table of Contents

- [Description](#-description)
- [Key Features](#-key-features)
- [Use Cases](#-use-cases)
- [Tech Stack](#-tech-stack)
- [Quick Start](#-quick-start)
- [Usage Guide](#-usage-guide)
- [Project Structure](#-project-structure)
- [License](#-license)

## 📝 Description

**house-rent-system** is a full-featured property rental management system built for small and medium-sized real estate agencies. It delivers end-to-end digital management covering housing inventory, landlord/tenant profiles, lease contracts, fee collection, staff permission control, and data backup & recovery.

Built with a lightweight Flask backend and native frontend pages, the system adopts a clear layered architecture, implements database-level business logic via triggers and stored procedures, and provides a three-tier permission system to standardize daily rental operations and improve management efficiency.

## ✨ Key Features

### Role-based Permission Control
- Three built-in roles: Super Admin, Agency Staff, Read-only Staff
- JWT token authentication with interface-level permission validation
- Staff account management (create, edit, password reset, deletion)
- Deletion protection for accounts with operation records

### Housing & Apartment Management
- Full CRUD operations for housing resources with detailed attributes (area, rent price, facilities, status)
- Apartment type classification and management
- Province-city-county cascade selection with automatic location deduplication
- Multi-dimensional filtering: location, status, apartment type, keyword search
- Automatic status synchronization with lease contracts

### Landlord & Tenant Management
- Complete profile management for landlords and tenants
- Format validation for phone numbers and ID card numbers
- Uniqueness check for phone and ID card information
- Deletion restriction for records associated with active houses or contracts

### Lease Contract Management
- Move-in registration with housing availability validation
- Automatic housing status update via database triggers
- Move-out registration with return date recording and status reset
- Contract list with keyword search and status filtering
- Operator tracking for each contract

### Fee Collection Management
- Support for three charge types: rent, security deposit, agency fee
- Fee records fully linked to lease contracts
- Pagination query with type filtering and keyword search
- Auto-generated fee entries via triggers when contracts are created/terminated

### Data Statistics & Visualization
- Stored procedure-based statistics of rental status by apartment type
- ECharts bar chart for intuitive comparison of rented/vacant houses
- Automatic occupancy rate calculation per apartment type

### Database Backup & Recovery
- One-click MySQL database backup with timestamp-named files
- Backup file list and history management
- Path traversal protection for secure recovery operations
- Restricted to super administrators only

### General Utilities
- Unified standard API response format
- Reusable pagination utility for all list queries
- Aggregated database view for house information overview
- Clean frontend interface with Bootstrap styling

## 🎯 Use Cases

- **Daily agency operation**: Digitally manage housing inventory, client information and lease contracts in a unified platform
- **Staff authority management**: Assign differentiated operation permissions to managers, frontline agents and data auditors
- **Business data analysis**: Track rental performance, occupancy rate and housing structure via built-in statistical features
- **Data security protection**: Perform regular database backups to prevent data loss and support rollback
- **Small and medium real estate firms**: Out-of-the-box rental management solution with low deployment and maintenance costs

## 🔧 Tech Stack

- Programming Languages: Python, HTML, CSS, JavaScript
- Framework & Libraries: Flask, Bootstrap, Axios, ECharts
- Database: MySQL

## ⚡ Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/killerwy/house-rent-system.git
cd house-rent-system
```

### 2. Initialize the database
Execute the initialization script `backend/db/init_sql.sql` to create a MySQL database named `house_rent` and seed test data

### 3. Configure environment
Copy env template file

```bash
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

Update environment variables in `.env` according to your MySQL environment

### 4. Install backend dependencies and start the backend service
Navigate to the `backend` directory

```bash
cd backend
```
Create & activate a virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv && source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

run backend service

```bash
python app.py
```

The service will run at `http://localhost:5000` by default.

### 5. Access the system
Open `frontend/index.html` in your browser
> Default super admin account: `admin` / password: `123456`

## 📖 Usage Guide

This chapter provides step-by-step operation tutorials for all core modules.

### 1: System Login
1. Open `frontend/index.html` in your browser.
2. Input your account username and password on the login form.
3. Click the login button to send authentication request to backend API.
4. After successful verification, the system will store JWT token in local storage and jump to the main dashboard page.
5. If the token expires or you visit pages without login, the system will auto redirect back to the login page.

### 2: Manage Apartment Types
1. Enter the menu `House Management - Apartment Type`.
2. Add new apartment:
   - Click "Add" button to pop up the edit modal.
   - Fill in apartment name and remark information.
   - Submit the form to save data to database.
3. Edit existing apartment:
   - Click "Edit" button on target table row.
   - Modify content in pop-up modal and submit changes.
4. Delete apartment:
   - Click "Delete" button, confirm the pop-up prompt.
   - System will block deletion if this type is bound to any housing resource.

### 3: Manage Housing Resources
1. Navigate to `House Management - House List`.
2. Filter target houses:
   - Select province, city, district from dropdown cascading selector.
   - Choose apartment type and house status filter.
   - Input keyword for address/landlord fuzzy search, then trigger filter.
3. Create new housing record:
   - Click "Add House" button to open the creation modal.
   - Complete all required fields: address, location, apartment type, landlord, area, monthly rent, supporting facilities, status.
   - Submit form; system will auto check duplicate house address.
4. Edit housing info:
   - Click "Edit" on target row, modify fields in modal and save.
5. Delete housing record:
   - Click delete button and confirm prompt.
   - System prohibits deletion if related rental contracts exist.

### 4: Manage Landlord Information
1. Open menu `Client Management - Landlord List`.
2. Search landlord: Input name/phone keyword and click search.
3. Add landlord:
   - Tap "Add" button, fill name, phone, ID number, residential address.
   - System will auto verify phone & ID format and uniqueness.
   - Submit to create new landlord entry.
4. Edit landlord: Click edit button, update information and save.
5. Delete landlord:
   - Click delete and confirm alert.
   - System blocks deletion if the landlord owns any houses.

### 5: Manage Tenant Information
1. Enter menu `Client Management - Tenant List`.
2. Search tenant by name, phone or ID number keyword.
3. Create tenant record:
   - Click add button, fill name, phone, ID, work unit.
   - Frontend and backend double-check phone & ID format and duplication.
4. Modify tenant data: Click edit button, update content and submit.
5. Delete tenant:
   - Trigger delete button and confirm prompt.
   - System rejects deletion when the tenant has active rental contracts.

### 6: Create & Manage Rental Contracts
#### 6.1 Create New Rental Contract (Check-in Registration)
1. Open `Rental Business - Create Contract`.
2. Select vacant house from dropdown list (only status=0 vacant houses are displayed).
3. Select corresponding tenant from tenant dropdown.
4. Fill start date, end date and actual monthly rent amount.
5. Submit form to complete registration.
6. Database trigger will auto:
   - Change house status to "Rented".
   - Auto generate rent, deposit and agency fee charge records.

#### 6.2 View All Contracts
1. Go to `Rental Business - Contract List`.
2. Filter contracts by keyword or contract status (In use / Checked out).
3. Click "Detail" to view full contract information pop-up.

#### 6.3 Process House Check-out
1. In contract list, find contracts with status "In use".
2. Click "Check-out" button to open return modal.
3. Fill actual return date.
4. Submit check-out form.
5. Database trigger will auto:
   - Mark contract status as "Checked out".
   - Restore house status to "Vacant".
   - Generate deposit refund charge record automatically.

### 7: Manage Charge Records
1. Open `Fee Management - Charge Record List`.
2. Filter records: input contract keyword or select charge type (rent / deposit / agency fee).
3. Manually add extra charge record:
   - Click "Add Charge" button.
   - Select target rental contract, choose charge type, input amount and remark.
   - Submit to save new billing record.

### 8: View Rental Statistical Charts
1. Enter menu `Data Statistics - Apartment Rental Stats`.
2. Page auto loads statistics data from database stored procedure.
3. Check table data: view apartment name, total houses, rented quantity, vacant quantity and occupancy rate.
4. View visual bar chart: compare rented & vacant quantity of each apartment type.
5. Resize browser window, chart will auto adapt width.

### 9: Super Admin Exclusive Operations
#### 9.1 Staff Account Management
1. Open `System Admin - Staff Management`.
2. Search staff by username or real name keyword.
3. Add new staff: fill account, password, real name, phone, ID, assign role permissions.
4. Edit staff info: modify name, contact, identity and role (cannot edit username).
5. Reset staff password: click "Reset Password", input new password and submit.
6. Delete staff account:
   - System forbids deleting super admin account.
   - Block deletion if staff has historical rental operation records.

#### 9.2 Database Backup & Recovery
1. Open `System Admin - Data Backup`.
2. One-click backup: click "Create Backup", system will generate timestamp SQL file and refresh file list.
3. View backup history: all .sql backup files are displayed with creation time.
4. Recover database from backup:
   - Click "Recover" button next to target backup file.
   - Confirm two warning pop-ups to start recovery.
   - The system will overwrite current database data with backup content.

### 10: Global House Overview View
1. Open menu `Data View - Full House Overview`.
2. Use multi-dimensional filters: province, city, district, apartment name, house status, keyword.
3. Page displays combined data including house address, landlord contact, apartment type, rent and status without switching multiple pages.

## 📁 Project Structure

```
house-rent-system/                  
├── backend                         # Backend service source code 
│   ├── app.py                      # Backend entry file
│   ├── config.py                   # Global configuration file
│   ├── api                         # All interface routing modules
│   │   ├── auth_api.py             # Authentication login & permission verification interface
│   │   ├── backup_api.py           # Data backup and data recovery related interface
│   │   ├── charge_api.py           # Rental fee charging management interface
│   │   ├── customer_api.py         # Tenant customer information CRUD interface
│   │   ├── house_api.py            # House basic information management interface
│   │   ├── landlord_api.py         # Landlord information management interface
│   │   ├── location_api.py         # House district/address location management interface
│   │   ├── rent_api.py             # Rental contract sign & house return registration interface
│   │   ├── stat_api.py             # Data statistics interface
│   │   ├── user_api.py             # System administrator user management interface
│   │   └── view_api.py             # View query interface
│   ├── db                          # Database operation related modules
│   │   ├── backup_tool.py          # Tool script for MySQL backup & restore logic
│   │   ├── init_sql.sql            # Database initialization script
│   │   └── mysql_conn.py           # MySQL database connection pool
│   ├── model                       # Database ORM model / data table mapping layer
│   │   ├── charge_model.py         # Rental fee billing table data model
│   │   ├── customer_model.py       # Tenant customer information table model
│   │   ├── house_model.py          # House basic information table model
│   │   ├── landlord_model.py       # Landlord owner information table model
│   │   ├── location_model.py       # House location community address table model
│   │   ├── rent_model.py           # Rental record & house return record table model
│   │   ├── type_model.py           # House apartment type table model
│   │   └── user_model.py           # System admin user table model
│   ├── util                        # Common utility tool modules
│   │   ├── auth_util.py            # JWT token generation, login authentication utility
│   │   ├── page_util.py            # Pagination query common tool class
│   │   └── response_util.py        # Unified standard API response format encapsulation
│   └── requirements.txt            # Python backend dependency package list
├── frontend                        # Frontend static page
│   ├── index.html                  # Login page of the system
│   ├── main.html                   # Main system layout page
│   ├── css                         # Global style sheet files
│   │   ├── global.css              # Global public style
│   │   └── table.css               # Unified table component dedicated style
│   ├── js                          # Frontend business logic scripts, split by module
│   │   ├── auth.js                 # Login token storage, permission interception logic
│   │   ├── backup.js               # Frontend page logic for backup & restore operation
│   │   ├── charge.js               # Rental fee list & billing operation logic
│   │   ├── customer.js             # Tenant customer add/edit/delete/search logic
│   │   ├── house.js                # House information management page logic
│   │   ├── landlord.js             # Landlord information management page logic
│   │   ├── rent.js                 # Rental contract creation & house return register logic
│   │   ├── stat.js                 # House rental quantity statistics page chart logic
│   │   ├── user.js                 # System admin user management page logic
│   │   └── view.js                 # View all house status view query page logic
│   └── pages                       # Sub-business functional page files
│       ├── backup_manage.html      # Data backup & recovery management page
│       ├── charge_list.html        # Rental fee charging record list page
│       ├── customer_list.html      # Tenant customer information list page
│       ├── house_list.html         # House basic information management list page
│       ├── house_type.html         # House apartment type classification management page
│       ├── house_view.html         # View page
│       ├── landlord_list.html      # Landlord owner information list page
│       ├── rent_add.html           # New rental contract registration page
│       ├── rent_list.html          # Rental & house return record list page
│       ├── stat_page.html          # House type rental quantity statistics page
│       └── sys_user.html           # System administrator user management page
├── README.md                       # English version project introduction
├── README_zh.md                    # Chinese version project introduction
├── LICENSE                         # Project open source license statement file
├── .gitignore                      # Git ignore file
└── .env.example                    # Example environment variable configuration template
```

## 📜 License

This project is licensed under the **MIT** License.

---
*This README was generated with ❤️ by [ReadmeBuddy](https://readmebuddy.com)*