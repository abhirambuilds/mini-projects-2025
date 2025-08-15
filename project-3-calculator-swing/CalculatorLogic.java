import java.util.LinkedList;
import java.util.List;

/**
 * CalculatorLogic class handles all mathematical operations, scientific functions, and calculation history
 * Supports chaining operations and maintains a history of recent calculations
 */
public class CalculatorLogic {
    private double storedValue;
    private double currentValue;
    private String currentOperation;
    private boolean newNumber;
    private boolean inverseMode;
    private boolean radianMode;
    private double lastAnswer;
    private List<String> calculationHistory;
    private static final int MAX_HISTORY_SIZE = 5;
    
    // Mathematical constants
    private static final double PI = Math.PI;
    private static final double E = Math.E;
    
    public CalculatorLogic() {
        reset();
    }
    
    /**
     * Resets the calculator to initial state
     */
    public void reset() {
        storedValue = 0.0;
        currentValue = 0.0;
        currentOperation = null;
        newNumber = true;
        inverseMode = false;
        radianMode = true; // Default to radians
        lastAnswer = 0.0;
        calculationHistory = new LinkedList<>();
    }
    
    /**
     * Sets the current value from UI input
     * @param value The value to set
     */
    public void setCurrentValue(double value) {
        currentValue = value;
        newNumber = true;
    }
    
    /**
     * Toggles between radians and degrees
     */
    public void toggleAngleMode() {
        radianMode = !radianMode;
    }
    
    /**
     * Gets current angle mode
     */
    public boolean isRadianMode() {
        return radianMode;
    }
    
    /**
     * Toggles inverse mode for trigonometric functions
     */
    public void toggleInverseMode() {
        inverseMode = !inverseMode;
    }
    
    /**
     * Gets current inverse mode
     */
    public boolean isInverseMode() {
        return inverseMode;
    }
    
    /**
     * Sets the last answer value
     */
    public void setLastAnswer(double value) {
        lastAnswer = value;
    }
    
    /**
     * Gets the last answer value
     */
    public double getLastAnswer() {
        return lastAnswer;
    }
    
    /**
     * Processes an operation (+, -, *, /, %)
     * @param operation The operation to perform
     * @return The current display value
     */
    public String processOperation(String operation) {
        if (currentOperation != null && !newNumber) {
            // Perform the previous operation
            performCalculation();
        }
        
        // Store the current value for the next operation
        storedValue = currentValue;
        currentOperation = operation;
        newNumber = true;
        return formatDisplay(currentValue);
    }
    
    /**
     * Performs the calculation based on current operation
     */
    private void performCalculation() {
        double result = 0.0;
        
        switch (currentOperation) {
            case "+":
                result = storedValue + currentValue;
                break;
            case "-":
                result = storedValue - currentValue;
                break;
            case "*":
                result = storedValue * currentValue;
                break;
            case "/":
                if (currentValue != 0) {
                    result = storedValue / currentValue;
                } else {
                    result = 0;
                }
                break;
            case "%":
                result = storedValue % currentValue;
                break;
            case "^":
                result = Math.pow(storedValue, currentValue);
                break;
        }
        
        currentValue = result;
        currentOperation = null;
    }
    
    /**
     * Calculates the final result
     * @return The final result as a formatted string
     */
    public String calculate() {
        if (currentOperation != null) {
            performCalculation();
        }
        lastAnswer = currentValue;
        return formatDisplay(currentValue);
    }
    
    /**
     * Calculates factorial of a number
     */
    public String factorial(double value) {
        if (value < 0 || value != (long) value) {
            return "Error";
        }
        if (value == 0 || value == 1) {
            return "1";
        }
        
        long result = 1;
        for (long i = 2; i <= (long) value; i++) {
            result *= i;
        }
        currentValue = result;
        lastAnswer = result;
        return formatDisplay(result);
    }
    
    /**
     * Calculates sine
     */
    public String sine(double value) {
        double angle = radianMode ? value : Math.toRadians(value);
        double result = inverseMode ? Math.asin(value) : Math.sin(angle);
        currentValue = result;
        lastAnswer = result;
        return formatDisplay(result);
    }
    
    /**
     * Calculates cosine
     */
    public String cosine(double value) {
        double angle = radianMode ? value : Math.toRadians(value);
        double result = inverseMode ? Math.acos(value) : Math.cos(angle);
        currentValue = result;
        lastAnswer = result;
        return formatDisplay(result);
    }
    
    /**
     * Calculates tangent
     */
    public String tangent(double value) {
        double angle = radianMode ? value : Math.toRadians(value);
        double result = inverseMode ? Math.atan(value) : Math.tan(angle);
        currentValue = result;
        lastAnswer = result;
        return formatDisplay(result);
    }
    
    /**
     * Calculates natural logarithm
     */
    public String naturalLog(double value) {
        if (value <= 0) {
            return "Error";
        }
        double result = inverseMode ? Math.exp(value) : Math.log(value);
        currentValue = result;
        lastAnswer = result;
        return formatDisplay(result);
    }
    
    /**
     * Calculates base-10 logarithm
     */
    public String log10(double value) {
        if (value <= 0) {
            return "Error";
        }
        double result = inverseMode ? Math.pow(10, value) : Math.log10(value);
        currentValue = result;
        lastAnswer = result;
        return formatDisplay(result);
    }
    
    /**
     * Calculates square root
     */
    public String squareRoot(double value) {
        if (value < 0) {
            return "Error";
        }
        double result = Math.sqrt(value);
        currentValue = result;
        lastAnswer = result;
        return formatDisplay(result);
    }
    
    /**
     * Calculates power (x^y)
     */
    public String power(double base, double exponent) {
        double result = Math.pow(base, exponent);
        currentValue = result;
        lastAnswer = result;
        return formatDisplay(result);
    }
    
    /**
     * Gets the value of π
     */
    public String getPi() {
        currentValue = PI;
        lastAnswer = PI;
        return formatDisplay(PI);
    }
    
    /**
     * Gets the value of e
     */
    public String getE() {
        currentValue = E;
        lastAnswer = E;
        return formatDisplay(E);
    }
    
    /**
     * Gets the calculation history
     * @return List of recent calculations
     */
    public List<String> getHistory() {
        return new LinkedList<>(calculationHistory);
    }
    
    /**
     * Adds a calculation to the history
     * @param expression The expression string
     * @param result The result string
     */
    public void addToHistory(String expression, String result) {
        String calculation = expression + " = " + result;
        calculationHistory.add(0, calculation);
        if (calculationHistory.size() > MAX_HISTORY_SIZE) {
            calculationHistory.remove(calculationHistory.size() - 1);
        }
    }
    
    /**
     * Formats a number for display (removes unnecessary decimal places)
     * @param value The value to format
     * @return Formatted string representation
     */
    public String formatDisplay(double value) {
        if (value == (long) value) {
            return String.format("%d", (long) value);
        } else {
            return String.format("%.8f", value).replaceAll("0*$", "").replaceAll("\\.$", "");
        }
    }
    
    /**
     * Gets the current value
     * @return Current calculator value
     */
    public double getCurrentValue() {
        return currentValue;
    }
}
