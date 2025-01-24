# Strategic Car Game

A turn-based strategic car game focused on customizing and optimizing cars for various events. Players can upgrade their cars, participate in events with unique challenges, and manage their resources to progress through the game.

## Features

- **Car Customization**:
  - Install and uninstall parts to improve stats such as speed, acceleration, handling, durability, and fuel efficiency.
- **Dynamic Events**:
  - Compete in events with unique modifiers like weather conditions (e.g., Rainy Weather, Icy Roads).
  - Earn rewards based on performance.
- **Inventory Management**:
  - A dedicated inventory system to manage and equip parts.
- **Garage System**:
  - View car stats, install parts, and repair damage.
- **Save and Load**:
  - Save progress to one of three slots and load games from saved files.
- **Helper Script**:
  - Automatically generate project structure and file contents for sharing or debugging.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

### Installation

1. Clone the repository:
   ```bash
   git clone
   ```
2. Navigate to the project directory:
   ```bash
   cd car game
   ```
3. Set up a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
### Usage

1. Run the game:
   ```bash
   python car_game.py
   ```
2. To generate project reports, use the helper script:
   ```bash
   python generate_project_info.py
   ```
   - Outputs will be saved in the `reports/` folder:
     - `project_structure.txt`: Project folder and file hierarchy.
     - `project_files.txt`: Contents of non-ignored files.

## File Structure

```
/
├── car_game.py           # Main game script
├── car.py                # Car and part classes
├── event.py              # Event and modifiers logic
├── inventory.py          # Inventory management
├── utils.py              # Utility functions
├── constants.py          # Centralized constants
├── generate_project_info.py # Helper script for project reports
├── reports/              # Contains generated reports
├── saved_games/          # Directory for save files
└── README.md             # Project documentation
```

## Contributing

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add feature-name"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

Let me know if you'd like to customize this further or add any specific details!