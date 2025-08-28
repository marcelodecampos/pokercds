# PokerCDS

*Read this in other languages: [English](README.en.md), [Português](README.md)*

A financial control system for poker nights among friends built with Reflex.

## Overview

PokerCDS is a web system to organize and control financial transactions during poker nights among friends. The system manages buy-in purchases, chip control, and player financial movements.

## Technologies Used

- **Reflex**: Modern Python web framework
- **SQLAlchemy**: ORM for database management
- **Alembic**: Database migration tool
- **psycopg3**: PostgreSQL driver for Python
- **TailwindCSS v4**: Modern CSS framework for styling

## Features

- **Authentication and Access**
  - Login screen with CPF and password
  - Login button for system access
  - No self-registration option for members
  - Member registration for poker group (administrators only)
  - Permission system with multiple administrators
- **Member Management**
  - Registration with CPF, name (up to 64 characters), PIX key (up to 128 characters) and phone
  - Option to enable/disable members
  - Access control based on member status
- **Financial Control**
  - Buy-in purchase control (R$ 50.00 each)
  - Player registration and purchases
  - Payment methods: cash, card or promissory note
  - Control of guarantees (cards and promissory notes) per player
  - Real-time financial movement tracking
  - Buy-in history per player
  - Final game accounting
  - Generation of debit and credit list between players
  - Report of who owes and to whom they should pay
  - Automatic settlement calculation based on chips vs guarantees

## System Rules

- Each buy-in costs exactly R$ 50.00 and equals the same value in chips
- It's not allowed to buy different values from R$ 50.00
- Players can buy multiple buy-ins during the night
- Each purchase must be made individually (one buy-in at a time)
- Only administrators can register new members in the system
- The system allows multiple administrators
- System access is done through CPF and password
- There's no self-registration option on the login screen
- Disabled members cannot access the system
- Required registration fields: CPF, name, nickname, PIX key and phone
- **NEW**: Only administrators can edit member nicknames
- Regular users can edit their own data, except CPF and nickname
- **Buy-in Payment Methods:**
  - Cash: immediate payment of R$ 50.00
  - Card: left as guarantee equivalent to R$ 50.00
  - Promissory note: payment commitment equivalent to R$ 50.00
- **Final Settlement:**
  - Players who paid in cash receive the exact value of final chips
  - If chip value > (cards + promissory notes) × R$ 50.00: player has money to receive
  - If chip value < (cards + promissory notes) × R$ 50.00: player must pay
  - At the end of the game, accounting is generated with payment list between players

## Prerequisites

- Python 3.12+
- Node.js 16+ (for frontend dependencies)
- PostgreSQL (database)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/marcelodecampos/PokerCDS.git
cd PokerCDS
```

2. Configure PostgreSQL database and create a database for the application

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure database migrations:
```bash
alembic upgrade head
```

5. Initialize Reflex application:
```bash
reflex init
```

## Usage

1. Run the development server:
```bash
reflex run
```

2. For development with detailed logs:
```bash
reflex run --env dev --loglevel debug
```

3. Open your browser and navigate to `http://localhost:3000`

## Configuration

The application uses Reflex with the following plugins:
- SitemapPlugin: Automatically generates sitemap.xml
- TailwindV4Plugin: Modern CSS framework for styling

## Development

To start developing:

1. Make your changes to Python files
2. The application will automatically reload with hot reloading enabled
3. Run with debug logs for troubleshooting:
   ```bash
   reflex run --env dev --loglevel debug
   ```
4. Visit the local development server to see your changes

### Useful Debug Commands

- **Normal development**: `reflex run`
- **Full debug**: `reflex run --env dev --loglevel debug`
- **Check configuration**: `reflex config`
- **Clear cache**: `reflex clean`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

[Add your license information here]

## Implemented Features

### ✅ Authentication
- Login Screen: Complete interface with CPF and password validation
- Login button for system access
- No self-registration option for members
- Member registration for poker group (administrators only)
- Permission system with multiple administrators

### ✅ User Management
- **User Profile**: 
  - View and edit personal data
  - Editable fields: name, email, PIX key, phone
  - Non-editable fields: CPF (always), nickname (only admin can change)
- **Password Change**: Secure system for password modification
- **Member Management (Admin)**:
  - Paginated member listing (maximum 20 per page)
  - Complete CRUD: create, view, edit, delete
  - Multiple selection for bulk deletion
  - Permission control (admin/active member/inactive)
  - Administrators can edit all fields, including nicknames

### ✅ Games Management (Admin)
- **Games Listing**: 
  - Games ordered by descending date (most recent first)
  - Display of date and optional description
  - Pagination up to 20 games per page
- **Games CRUD**:
  - Create new games with date and description
  - Edit existing games
  - Delete individual games or in bulk
  - Multiple selection for bulk operations
- **Validations**: Required date, optional description

## Permissions and Access Control

### Regular Users:
- View and edit own profile (except CPF and nickname)
- Change own password
- Access poker features (when implemented)

### Administrators:
- All regular user permissions
- Register new members
- Manage all members (complete CRUD)
- Change any member's nickname
- Activate/deactivate members
- Grant/revoke administrator privileges
- **Manage games**: Create, edit, view and delete games
- **Session control**: Access to game-member relationship

### Fields with Restrictions:
- **CPF**: Cannot be changed after registration
- **Nickname**: Only administrators can modify
- **Admin Permissions**: Only administrators can modify
- **Active/Inactive Status**: Only administrators can modify

## Project Structure

```
PokerCDS/
├── PokerCDS/
│   ├── components/          # Reusable UI components
│   │   ├── __init__.py
│   │   └── login_form.py    # Login form
│   ├── pages/              # Application pages
│   │   ├── __init__.py
│   │   └── login.py        # Login page
│   ├── entities/           # Database models
│   │   ├── __init__.py
│   │   ├── base.py         # SQLModel base class
│   │   └── member.py       # Member model
│   ├── utils/              # Utilities
│   │   ├── __init__.py
│   │   ├── timezone.py     # Timezone functions
│   │   └── password.py     # Password utilities
│   └── PokerCDS.py         # Main application
├── alembic/                # Database migrations
├── rxconfig.py            # Reflex configuration
└── README.md
```

## How to Test Login

1. Run the application:
```bash
reflex run
```

2. Access `http://localhost:3000`

3. Use the temporary credentials:
   - CPF: `594.693.904-15` (or `59469390415`)
   - Password: `admin123`

**Note**: These are temporary credentials for development. In the final version, authentication will be done through the database with encrypted passwords.

## Development Standards

### Code and Architecture
- Follow DRY (Don't Repeat Yourself) principles for reusable components
- Clear separation between business logic (State) and presentation (Components)
- Centralized validations in base states
- Configurable components through props
- **NEW**: All Reflex components must have a unique and representative ID
- IDs must follow hierarchical and descriptive convention (e.g., `members-table-card`, `login-form-submit-button`)

### Interface and UX
- Responsive design with dark theme by default
- Theme colors: dark appearance, sky accent color, sand gray color
- Error and success messages in Portuguese
- Visible loading states during asynchronous operations
- Confirmation before destructive actions (deletions)

## Benefits of Unique IDs

### Development and Maintenance:
- **HTML Inspection**: Elements easily identifiable in browser DevTools
- **Debugging**: Quick identification of issues in specific components
- **Automated Testing**: Specific and reliable selectors for each element
- **Analytics**: Detailed tracking of user interactions

### Naming Convention:
- `page-*` for main page elements
- `component-*` for specific component elements
- `modal-*` for modal and dialog elements
- `*-button`, `*-icon`, `*-text` for specific element types
- `item-*-{id}` for specific items in lists

### Examples:
```html
<!-- Members management page -->
<div id="members-management-page">
  <div id="members-table-card">
    <button id="members-add-button">
    <div id="member-row-1">
      <button id="member-edit-button-1">
      <button id="member-delete-button-1">
