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
- Required registration fields: CPF, name, PIX key and phone
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

2. Open your browser and navigate to `http://localhost:3000`

## Configuration

The application uses Reflex with the following plugins:
- SitemapPlugin: Automatically generates sitemap.xml
- TailwindV4Plugin: Modern CSS framework for styling

## Development

To start developing:

1. Make your changes to Python files
2. The app will automatically reload with hot reloading enabled
3. Visit the local development server to see your changes

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

[Add your license information here]
