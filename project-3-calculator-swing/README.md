# Scientific Calculator App (Java Swing)

A modern, responsive **Scientific Calculator** desktop application built with **Java Swing**, featuring both basic and advanced mathematical functions, a calculation history panel, and a clean, professional UI.

---

## ✨ Features

- **Basic Operations**: `+`, `-`, `×`, `÷`, `%`, `x^y`
- **Scientific Functions**: `sin`, `cos`, `tan` (Rad/Deg toggle), `ln`, `log`, factorial, square root, power
- **Constants**: π (pi), e (Euler’s number)
- **Chained Calculations**: Perform multiple operations sequentially
- **Answer Recall**: Use the last calculated result
- **History Panel**: Shows last 5 calculations in a sidebar
- **Responsive Layout**: Resizes gracefully with the window
- **Hover Effects**: Smooth button animations

---

## 🎨 Design

- **Color Scheme**:
  - Background: `#F5F5F5`
  - Operators: `#6495ED`
  - Functions: `#FFD700`
  - Constants: `#98FB98`
  - Clear: `#FF6347`
- **Typography**: Arial, clear and readable
- **Layout**: Grid-based button placement with spacing
- **UI Enhancements**: Rounded buttons, subtle shadows

---

## 📂 Project Structure
project-3-calculator-swing/
├── Main.java # Application entry point
├── CalculatorUI.java # UI layout and components
├── CalculatorLogic.java # Mathematical operations & history
└── README.md

yaml
Copy
Edit

---

## 🚀 Getting Started

### Prerequisites
- Java 8 or higher
- IDE (IntelliJ, Eclipse, VS Code) or terminal

### Run from Terminal
```bash
javac *.java
java Main
Run from IDE
Open the folder in your IDE

Run Main.java

🖥 Usage Examples
Basic Calculation

Copy
Edit
5 + 3 = 8
Scientific Functions

cpp
Copy
Edit
sin(30) = 0.5  (Degree mode)
π × 2 = 6.283185307
Advanced

bash
Copy
Edit
2^3 = 8
ln(e) = 1
🎯 Customization
Colors: Update color constants in CalculatorUI.java

Fonts: Change font styles in UI setup

History Limit: Adjust MAX_HISTORY_SIZE in CalculatorLogic.java

📜 License
This project is open source under the MIT License.

Built with ❤️ in Java Swing