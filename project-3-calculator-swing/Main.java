import javax.swing.SwingUtilities;

/**
 * Main class for the Calculator Application
 * Launches the calculator with a modern dark theme
 */
public class Main {
    public static void main(String[] args) {
        // Launch the calculator on the Event Dispatch Thread
        SwingUtilities.invokeLater(() -> {
            CalculatorUI calculator = new CalculatorUI();
            calculator.setVisible(true);
        });
    }
}
