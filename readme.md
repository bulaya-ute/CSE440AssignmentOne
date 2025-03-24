# Chinese Wall Model App

This project implements a graphical representation of the **Chinese Wall Model** for access control using **Kivy** and **KivyMD**. The application demonstrates interactive card selection, line drawing between selected cards, and dynamic resizing support.

## Prerequisites
Ensure you have the following installed:
- Python 3.8 or higher
- pip (Python package installer)

## Installation
1. Clone the repository:

   ```bash
   git clone https://github.com/bulaya-ute/CSE440AssignmentOne
   cd CSE440AssignmentOne
   ```

2. Install the required dependencies from `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

## Running the Application
To run the application, use the following command:

```bash
python main.py
```

## Usage
- Click on any two cards to draw a line between them.
- The app automatically handles resizing and adjusts line positions accordingly.
- Clicking on a selected card again will deselect it.

## Troubleshooting
If you encounter issues with `kivymd` or `kivy` installations, try updating your dependencies:

```bash
pip install --upgrade kivy kivymd
```

## Future Improvements
- Implementing enhanced UI features for better user interaction.
- Adding more flexible COI logic for improved Chinese Wall model demonstration.

## License
This project is licensed under the [MIT License](LICENSE).

## Contributions
Contributions are welcome! Feel free to submit issues or pull requests for enhancements and bug fixes.