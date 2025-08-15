import javax.swing.*;
import javax.swing.border.EmptyBorder;
import javax.swing.border.TitledBorder;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.awt.geom.RoundRectangle2D;
import java.awt.image.BufferedImage;

/**
 * CalculatorUI class handles the scientific calculator user interface
 * Features a modern, sleek design with gradients, shadows, and professional styling
 */
public class CalculatorUI extends JFrame {
    private JTextField displayField;
    private JTextArea historyArea;
    private CalculatorLogic logic;
    private StringBuilder currentInput;
    private StringBuilder expression;
    private boolean waitingForNumber;
    private JPanel buttonPanel;
    private JButton radDegButton;
    private JButton invButton;
    
    // Ultra-modern color scheme with gradients
    private static final Color BACKGROUND_GRADIENT_TOP = new Color(18, 18, 18);
    private static final Color BACKGROUND_GRADIENT_BOTTOM = new Color(32, 32, 32);
    private static final Color DISPLAY_BACKGROUND = new Color(15, 15, 15);
    private static final Color DISPLAY_BORDER = new Color(60, 60, 60);
    private static final Color DISPLAY_TEXT = new Color(255, 255, 255);
    
    // Button colors with modern feel
    private static final Color NUMBER_BUTTON_COLOR = new Color(45, 45, 45);
    private static final Color NUMBER_BUTTON_HOVER = new Color(60, 60, 60);
    private static final Color OPERATOR_BUTTON_COLOR = new Color(0, 122, 255);
    private static final Color OPERATOR_BUTTON_HOVER = new Color(0, 102, 235);
    private static final Color EQUALS_BUTTON_COLOR = new Color(88, 86, 214);
    private static final Color EQUALS_BUTTON_HOVER = new Color(108, 106, 234);
    private static final Color FUNCTION_BUTTON_COLOR = new Color(255, 149, 0);
    private static final Color FUNCTION_BUTTON_HOVER = new Color(255, 169, 20);
    private static final Color CONSTANT_BUTTON_COLOR = new Color(52, 199, 89);
    private static final Color CONSTANT_BUTTON_HOVER = new Color(72, 219, 109);
    private static final Color CLEAR_BUTTON_COLOR = new Color(255, 59, 48);
    private static final Color CLEAR_BUTTON_HOVER = new Color(255, 79, 68);
    private static final Color MODE_BUTTON_COLOR = new Color(175, 82, 222);
    private static final Color MODE_BUTTON_HOVER = new Color(195, 102, 242);
    
    // Text colors
    private static final Color BUTTON_TEXT_COLOR = new Color(255, 255, 255);
    private static final Color HISTORY_TEXT_COLOR = new Color(200, 200, 200);
    private static final Color HISTORY_BACKGROUND = new Color(25, 25, 25);
    
    public CalculatorUI() {
        logic = new CalculatorLogic();
        currentInput = new StringBuilder();
        expression = new StringBuilder();
        waitingForNumber = true;
        
        setupFrame();
        createComponents();
        layoutComponents();
        setupEventHandlers();
        
        pack();
        setLocationRelativeTo(null);
    }
    
    /**
     * Sets up the main frame properties
     */
    private void setupFrame() {
        setTitle("Scientific Calculator Pro");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setResizable(true);
        setMinimumSize(new Dimension(900, 700));
        getContentPane().setBackground(BACKGROUND_GRADIENT_TOP);
        
        // Set custom window icon (optional)
        try {
            setIconImage(createWindowIcon());
        } catch (Exception e) {
            // Ignore if icon creation fails
        }
    }
    
    /**
     * Creates a custom window icon
     */
    private Image createWindowIcon() {
        BufferedImage icon = new BufferedImage(32, 32, BufferedImage.TYPE_INT_ARGB);
        Graphics2D g2d = icon.createGraphics();
        g2d.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        
        // Draw a calculator icon
        g2d.setColor(OPERATOR_BUTTON_COLOR);
        g2d.fillRoundRect(4, 4, 24, 24, 6, 6);
        g2d.setColor(BUTTON_TEXT_COLOR);
        g2d.setFont(new Font("Arial", Font.BOLD, 16));
        g2d.drawString("∑", 8, 20);
        
        g2d.dispose();
        return icon;
    }
    
    /**
     * Creates all UI components
     */
    private void createComponents() {
        // Display field with modern styling
        displayField = new JTextField("0") {
            @Override
            protected void paintComponent(Graphics g) {
                Graphics2D g2d = (Graphics2D) g.create();
                g2d.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
                
                // Create gradient background
                GradientPaint gradient = new GradientPaint(0, 0, DISPLAY_BACKGROUND, getWidth(), getHeight(), new Color(20, 20, 20));
                g2d.setPaint(gradient);
                g2d.fillRoundRect(0, 0, getWidth(), getHeight(), 15, 15);
                
                // Draw border
                g2d.setColor(DISPLAY_BORDER);
                g2d.setStroke(new BasicStroke(2));
                g2d.drawRoundRect(1, 1, getWidth()-2, getHeight()-2, 15, 15);
                
                // Draw text
                g2d.setColor(DISPLAY_TEXT);
                g2d.setFont(new Font("Segoe UI", Font.BOLD, 32));
                FontMetrics fm = g2d.getFontMetrics();
                String text = getText();
                int textX = getWidth() - fm.stringWidth(text) - 20;
                int textY = (getHeight() + fm.getAscent()) / 2 - 5;
                g2d.drawString(text, textX, textY);
                
                g2d.dispose();
            }
        };
        displayField.setOpaque(false);
        displayField.setEditable(false);
        displayField.setBorder(BorderFactory.createEmptyBorder());
        displayField.setPreferredSize(new Dimension(0, 80));
        
        // History area with modern styling
        historyArea = new JTextArea() {
            @Override
            protected void paintComponent(Graphics g) {
                Graphics2D g2d = (Graphics2D) g.create();
                g2d.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
                
                // Create gradient background
                GradientPaint gradient = new GradientPaint(0, 0, HISTORY_BACKGROUND, getWidth(), getHeight(), new Color(30, 30, 30));
                g2d.setPaint(gradient);
                g2d.fillRoundRect(0, 0, getWidth(), getHeight(), 15, 15);
                
                g2d.dispose();
                super.paintComponent(g);
            }
        };
        historyArea.setFont(new Font("Segoe UI", Font.PLAIN, 14));
        historyArea.setEditable(false);
        historyArea.setForeground(HISTORY_TEXT_COLOR);
        historyArea.setCaretColor(HISTORY_TEXT_COLOR);
        historyArea.setBorder(BorderFactory.createCompoundBorder(
            BorderFactory.createTitledBorder(
                BorderFactory.createLineBorder(MODE_BUTTON_COLOR, 2),
                "History (Last 5)",
                TitledBorder.CENTER,
                TitledBorder.TOP,
                new Font("Segoe UI", Font.BOLD, 14),
                MODE_BUTTON_COLOR
            ),
            new EmptyBorder(10, 15, 10, 15)
        ));
    }
    
    /**
     * Lays out all components using BorderLayout and GridBagLayout
     */
    private void layoutComponents() {
        setLayout(new BorderLayout(20, 20));
        
        // Add padding around the main content
        JPanel mainPanel = new JPanel(new BorderLayout(20, 20)) {
            @Override
            protected void paintComponent(Graphics g) {
                Graphics2D g2d = (Graphics2D) g.create();
                g2d.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
                
                // Create gradient background
                GradientPaint gradient = new GradientPaint(0, 0, BACKGROUND_GRADIENT_TOP, 0, getHeight(), BACKGROUND_GRADIENT_BOTTOM);
                g2d.setPaint(gradient);
                g2d.fillRect(0, 0, getWidth(), getHeight());
                
                g2d.dispose();
            }
        };
        mainPanel.setOpaque(false);
        mainPanel.setBorder(new EmptyBorder(25, 25, 25, 25));
        
        // Top panel for display
        JPanel displayPanel = new JPanel(new BorderLayout());
        displayPanel.setOpaque(false);
        displayPanel.add(displayField, BorderLayout.CENTER);
        
        // Center panel for calculator buttons
        buttonPanel = createButtonPanel();
        
        // Right panel for history
        JPanel historyPanel = new JPanel(new BorderLayout());
        historyPanel.setOpaque(false);
        historyPanel.setPreferredSize(new Dimension(280, 0));
        historyPanel.add(historyArea, BorderLayout.CENTER);
        
        // Add components to main panel
        mainPanel.add(displayPanel, BorderLayout.NORTH);
        mainPanel.add(buttonPanel, BorderLayout.CENTER);
        mainPanel.add(historyPanel, BorderLayout.EAST);
        
        add(mainPanel, BorderLayout.CENTER);
    }
    
    /**
     * Creates the button panel with all scientific calculator buttons
     * @return JPanel containing all buttons
     */
    private JPanel createButtonPanel() {
        JPanel panel = new JPanel(new GridBagLayout()) {
            @Override
            protected void paintComponent(Graphics g) {
                Graphics2D g2d = (Graphics2D) g.create();
                g2d.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
                
                // Create subtle gradient background
                GradientPaint gradient = new GradientPaint(0, 0, new Color(35, 35, 35), 0, getHeight(), new Color(40, 40, 40));
                g2d.setPaint(gradient);
                g2d.fillRoundRect(0, 0, getWidth(), getHeight(), 20, 20);
                
                g2d.dispose();
            }
        };
        panel.setOpaque(false);
        panel.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
        
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.fill = GridBagConstraints.BOTH;
        gbc.insets = new Insets(4, 4, 4, 4);
        
        // Button definitions: [text, row, col, width, height, type]
        Object[][] buttonDefs = {
            // Row 1
            {"Rad", 0, 0, 2, 1, "mode"},
            {"x!", 0, 2, 1, 1, "function"},
            {"(", 0, 3, 1, 1, "function"},
            {")", 0, 4, 1, 1, "function"},
            {"%", 0, 5, 1, 1, "operator"},
            {"AC", 0, 6, 1, 1, "clear"},
            
            // Row 2
            {"Inv", 1, 0, 1, 1, "mode"},
            {"sin", 1, 1, 1, 1, "function"},
            {"ln", 1, 2, 1, 1, "function"},
            {"7", 1, 3, 1, 1, "number"},
            {"8", 1, 4, 1, 1, "number"},
            {"9", 1, 5, 1, 1, "number"},
            {"÷", 1, 6, 1, 1, "operator"},
            
            // Row 3
            {"π", 2, 0, 1, 1, "constant"},
            {"cos", 2, 1, 1, 1, "function"},
            {"log", 2, 2, 1, 1, "function"},
            {"4", 2, 3, 1, 1, "number"},
            {"5", 2, 4, 1, 1, "number"},
            {"6", 2, 5, 1, 1, "number"},
            {"×", 2, 6, 1, 1, "operator"},
            
            // Row 4
            {"e", 3, 0, 1, 1, "constant"},
            {"tan", 3, 1, 1, 1, "function"},
            {"√", 3, 2, 1, 1, "function"},
            {"1", 3, 3, 1, 1, "number"},
            {"2", 3, 4, 1, 1, "number"},
            {"3", 3, 5, 1, 1, "number"},
            {"-", 3, 6, 1, 1, "operator"},
            
            // Row 5
            {"Ans", 4, 0, 1, 1, "function"},
            {"EXP", 4, 1, 1, 1, "function"},
            {"xʸ", 4, 2, 1, 1, "function"},
            {"0", 4, 3, 2, 1, "number"},
            {".", 4, 5, 1, 1, "number"},
            {"=", 4, 6, 1, 1, "equals"},
            {"+", 4, 7, 1, 1, "operator"}
        };
        
        for (Object[] def : buttonDefs) {
            String text = (String) def[0];
            int row = Integer.parseInt(def[1].toString());
            int col = Integer.parseInt(def[2].toString());
            int width = Integer.parseInt(def[3].toString());
            int height = Integer.parseInt(def[4].toString());
            String type = (String) def[5];
            
            JButton button = createStyledButton(text, type);
            
            gbc.gridx = col;
            gbc.gridy = row;
            gbc.gridwidth = width;
            gbc.gridheight = height;
            gbc.weightx = 1.0;
            gbc.weighty = 1.0;
            
            panel.add(button, gbc);
        }
        
        return panel;
    }
    
    /**
     * Creates a styled button with modern design, gradients, and hover effects
     * @param text Button text
     * @param type Button type (number, operator, equals, clear, function, constant, mode)
     * @return Styled JButton
     */
    private JButton createStyledButton(String text, String type) {
        JButton button = new JButton(text) {
            @Override
            protected void paintComponent(Graphics g) {
                Graphics2D g2d = (Graphics2D) g.create();
                g2d.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
                
                // Get button colors based on type
                Color[] colors = getButtonColors(type);
                Color baseColor = colors[0];
                Color hoverColor = colors[1];
                
                // Create gradient background
                GradientPaint gradient = new GradientPaint(0, 0, baseColor, getWidth(), getHeight(), hoverColor);
                g2d.setPaint(gradient);
                g2d.fillRoundRect(2, 2, getWidth()-4, getHeight()-4, 12, 12);
                
                // Add subtle shadow
                g2d.setColor(new Color(0, 0, 0, 30));
                g2d.fillRoundRect(4, 4, getWidth()-4, getHeight()-4, 12, 12);
                
                // Draw text with shadow effect
                g2d.setColor(new Color(0, 0, 0, 50));
                g2d.setFont(new Font("Segoe UI", Font.BOLD, 16));
                FontMetrics fm = g2d.getFontMetrics();
                int textX = (getWidth() - fm.stringWidth(getText())) / 2 + 1;
                int textY = (getHeight() + fm.getAscent()) / 2 + 1;
                g2d.drawString(getText(), textX, textY);
                
                // Draw main text
                g2d.setColor(BUTTON_TEXT_COLOR);
                g2d.drawString(getText(), textX-1, textY-1);
                
                g2d.dispose();
            }
        };
        
        button.setPreferredSize(new Dimension(70, 60));
        button.setOpaque(false);
        button.setContentAreaFilled(false);
        button.setBorderPainted(false);
        button.setFocusPainted(false);
        button.setCursor(new Cursor(Cursor.HAND_CURSOR));
        
        // Special handling for Rad/Deg button
        if (text.equals("Rad")) {
            radDegButton = button;
            updateRadDegButton();
        }
        
        // Special handling for Inv button
        if (text.equals("Inv")) {
            invButton = button;
            updateInvButton();
        }
        
        // Add hover effects
        button.addMouseListener(new MouseAdapter() {
            @Override
            public void mouseEntered(MouseEvent e) {
                button.repaint();
            }
            
            @Override
            public void mouseExited(MouseEvent e) {
                button.repaint();
            }
        });
        
        return button;
    }
    
    /**
     * Gets button colors based on type
     */
    private Color[] getButtonColors(String type) {
        switch (type) {
            case "operator":
                return new Color[]{OPERATOR_BUTTON_COLOR, OPERATOR_BUTTON_HOVER};
            case "equals":
                return new Color[]{EQUALS_BUTTON_COLOR, EQUALS_BUTTON_HOVER};
            case "clear":
                return new Color[]{CLEAR_BUTTON_COLOR, CLEAR_BUTTON_HOVER};
            case "function":
                return new Color[]{FUNCTION_BUTTON_COLOR, FUNCTION_BUTTON_HOVER};
            case "constant":
                return new Color[]{CONSTANT_BUTTON_COLOR, CONSTANT_BUTTON_HOVER};
            case "mode":
                return new Color[]{MODE_BUTTON_COLOR, MODE_BUTTON_HOVER};
            default: // number
                return new Color[]{NUMBER_BUTTON_COLOR, NUMBER_BUTTON_HOVER};
        }
    }
    
    /**
     * Updates the Rad/Deg button appearance
     */
    private void updateRadDegButton() {
        if (radDegButton != null) {
            if (logic.isRadianMode()) {
                radDegButton.setText("Rad");
            } else {
                radDegButton.setText("Deg");
            }
            radDegButton.repaint();
        }
    }
    
    /**
     * Updates the Inv button appearance
     */
    private void updateInvButton() {
        if (invButton != null) {
            invButton.repaint();
        }
    }
    
    /**
     * Sets up event handlers for all buttons
     */
    private void setupEventHandlers() {
        // Add action listeners to all buttons in the button panel
        for (Component comp : buttonPanel.getComponents()) {
            if (comp instanceof JButton) {
                JButton button = (JButton) comp;
                button.addActionListener(new ButtonActionListener());
            }
        }
    }
    
    /**
     * Action listener for all calculator buttons
     */
    private class ButtonActionListener implements ActionListener {
        @Override
        public void actionPerformed(ActionEvent e) {
            String command = e.getActionCommand();
            
            switch (command) {
                case "AC":
                    clear();
                    break;
                case "=":
                    calculate();
                    break;
                case "+":
                case "-":
                case "%":
                case "÷":
                case "×":
                    processOperator(command);
                    break;
                case ".":
                    processDecimal();
                    break;
                case "Rad":
                case "Deg":
                    toggleAngleMode();
                    break;
                case "Inv":
                    toggleInverseMode();
                    break;
                case "x!":
                    processFactorial();
                    break;
                case "sin":
                    processSine();
                    break;
                case "cos":
                    processCosine();
                    break;
                case "tan":
                    processTangent();
                    break;
                case "ln":
                    processNaturalLog();
                    break;
                case "log":
                    processLog10();
                    break;
                case "√":
                    processSquareRoot();
                    break;
                case "xʸ":
                    processPower();
                    break;
                case "π":
                    processPi();
                    break;
                case "e":
                    processE();
                    break;
                case "Ans":
                    processAnswer();
                    break;
                case "EXP":
                    processExponent();
                    break;
                case "(":
                case ")":
                    processParenthesis(command);
                    break;
                default:
                    if (command.matches("\\d")) {
                        processNumber(command);
                    }
                    break;
            }
            
            updateHistory();
        }
    }
    
    /**
     * Toggles angle mode (Radians/Degrees)
     */
    private void toggleAngleMode() {
        logic.toggleAngleMode();
        updateRadDegButton();
    }
    
    /**
     * Toggles inverse mode
     */
    private void toggleInverseMode() {
        logic.toggleInverseMode();
        updateInvButton();
    }
    
    /**
     * Processes factorial
     */
    private void processFactorial() {
        if (currentInput.length() > 0) {
            double number = Double.parseDouble(currentInput.toString());
            String result = logic.factorial(number);
            displayField.setText(result);
            currentInput.setLength(0);
            waitingForNumber = true;
        } else if (expression.length() > 0) {
            // Use the current result from logic
            double number = logic.getCurrentValue();
            String result = logic.factorial(number);
            displayField.setText(result);
            currentInput.setLength(0);
            waitingForNumber = true;
        }
    }
    
    /**
     * Processes sine
     */
    private void processSine() {
        if (currentInput.length() > 0) {
            double number = Double.parseDouble(currentInput.toString());
            String result = logic.sine(number);
            displayField.setText(result);
            currentInput.setLength(0);
            waitingForNumber = true;
        } else if (expression.length() > 0) {
            // Use the current result from logic
            double number = logic.getCurrentValue();
            String result = logic.sine(number);
            displayField.setText(result);
            currentInput.setLength(0);
            waitingForNumber = true;
        }
    }
    
    /**
     * Processes cosine
     */
    private void processCosine() {
        if (currentInput.length() > 0) {
            double number = Double.parseDouble(currentInput.toString());
            String result = logic.cosine(number);
            displayField.setText(result);
            currentInput.setLength(0);
            waitingForNumber = true;
        } else if (expression.length() > 0) {
            // Use the current result from logic
            double number = logic.getCurrentValue();
            String result = logic.cosine(number);
            displayField.setText(result);
            currentInput.setLength(0);
            waitingForNumber = true;
        }
    }
    
    /**
     * Processes tangent
     */
    private void processTangent() {
        if (currentInput.length() > 0) {
            double number = Double.parseDouble(currentInput.toString());
            String result = logic.tangent(number);
            displayField.setText(result);
            currentInput.setLength(0);
            waitingForNumber = true;
        } else if (expression.length() > 0) {
            // Use the current result from logic
            double number = logic.getCurrentValue();
            String result = logic.tangent(number);
            currentInput.setLength(0);
            waitingForNumber = true;
        }
    }
    
    /**
     * Processes natural logarithm
     */
    private void processNaturalLog() {
        if (currentInput.length() > 0) {
            double number = Double.parseDouble(currentInput.toString());
            String result = logic.naturalLog(number);
            displayField.setText(result);
            currentInput.setLength(0);
            waitingForNumber = true;
        } else if (expression.length() > 0) {
            // Use the current result from logic
            double number = logic.getCurrentValue();
            String result = logic.naturalLog(number);
            displayField.setText(result);
            currentInput.setLength(0);
            waitingForNumber = true;
        }
    }
    
    /**
     * Processes base-10 logarithm
     */
    private void processLog10() {
        if (currentInput.length() > 0) {
            double number = Double.parseDouble(currentInput.toString());
            String result = logic.log10(number);
            displayField.setText(result);
            currentInput.setLength(0);
            waitingForNumber = true;
        } else if (expression.length() > 0) {
            // Use the current result from logic
            double number = logic.getCurrentValue();
            String result = logic.log10(number);
            displayField.setText(result);
            currentInput.setLength(0);
            waitingForNumber = true;
        }
    }
    
    /**
     * Processes square root
     */
    private void processSquareRoot() {
        if (currentInput.length() > 0) {
            double number = Double.parseDouble(currentInput.toString());
            String result = logic.squareRoot(number);
            displayField.setText(result);
            currentInput.setLength(0);
            waitingForNumber = true;
        } else if (expression.length() > 0) {
            // Use the current result from logic
            double number = logic.getCurrentValue();
            String result = logic.squareRoot(number);
            displayField.setText(result);
            currentInput.setLength(0);
            waitingForNumber = true;
        }
    }
    
    /**
     * Processes power (x^y)
     */
    private void processPower() {
        if (currentInput.length() > 0) {
            double base = Double.parseDouble(currentInput.toString());
            logic.setCurrentValue(base);
            currentInput.setLength(0);
            waitingForNumber = true;
        } else if (expression.length() > 0) {
            // Use the current result from logic
            double base = logic.getCurrentValue();
            logic.setCurrentValue(base);
            currentInput.setLength(0);
            waitingForNumber = true;
        }
    }
    
    /**
     * Processes π constant
     */
    private void processPi() {
        String result = logic.getPi();
        displayField.setText(result);
        currentInput.setLength(0);
        waitingForNumber = true;
        // Add to expression for display
        if (expression.length() > 0) {
            expression.append(" ");
        }
        expression.append("π");
        updateDisplay();
    }
    
    /**
     * Processes e constant
     */
    private void processE() {
        String result = logic.getE();
        displayField.setText(result);
        currentInput.setLength(0);
        waitingForNumber = true;
        // Add to expression for display
        if (expression.length() > 0) {
            expression.append(" ");
        }
        expression.append("e");
        updateDisplay();
    }
    
    /**
     * Processes answer recall
     */
    private void processAnswer() {
        double answer = logic.getLastAnswer();
        if (answer != 0.0) {
            String result = logic.formatDisplay(answer);
            displayField.setText(result);
            currentInput.setLength(0);
            waitingForNumber = true;
            // Add to expression for display
            if (expression.length() > 0) {
                expression.append(" ");
            }
            expression.append("Ans");
            updateDisplay();
        }
    }
    
    /**
     * Processes exponent notation
     */
    private void processExponent() {
        if (currentInput.length() > 0) {
            currentInput.append("E");
            updateDisplay();
        }
    }
    
    /**
     * Processes parentheses
     */
    private void processParenthesis(String parenthesis) {
        if (expression.length() > 0) {
            expression.append(" ");
        }
        expression.append(parenthesis);
        updateDisplay();
    }
    
    /**
     * Processes number input
     * @param number The number to process
     */
    private void processNumber(String number) {
        if (waitingForNumber) {
            currentInput.setLength(0);
            waitingForNumber = false;
        }
        currentInput.append(number);
        
        // Update display to show the current expression
        updateDisplay();
    }
    
    /**
     * Processes decimal point input
     */
    private void processDecimal() {
        if (waitingForNumber) {
            currentInput.setLength(0);
            currentInput.append("0");
            waitingForNumber = false;
        }
        if (currentInput.indexOf(".") == -1) {
            currentInput.append(".");
            updateDisplay();
        }
    }
    
    /**
     * Processes operator input
     * @param operator The operator to process
     */
    private void processOperator(String operator) {
        if (currentInput.length() > 0) {
            // Add the current number to the expression
            if (expression.length() > 0) {
                expression.append(" ");
            }
            expression.append(currentInput.toString());
            
            // Add the operator to the expression
            expression.append(" ").append(operator);
            
            // Set the current value in logic and process the operation
            double number = Double.parseDouble(currentInput.toString());
            logic.setCurrentValue(number);
            logic.processOperation(convertOperator(operator));
            currentInput.setLength(0);
            waitingForNumber = true;
            
            // Update display
            updateDisplay();
        } else if (expression.length() > 0 && waitingForNumber) {
            // Continue from previous result - add operator to expression
            expression.append(" ").append(operator);
            
            // Process the operation using the current result
            logic.processOperation(convertOperator(operator));
            waitingForNumber = true;
            
            // Update display
            updateDisplay();
        }
    }
    
    /**
     * Converts display operators to internal operators
     * @param displayOperator The display operator
     * @return Internal operator string
     */
    private String convertOperator(String displayOperator) {
        switch (displayOperator) {
            case "×": return "*";
            case "÷": return "/";
            default: return displayOperator;
        }
    }
    
    /**
     * Performs the calculation
     */
    private void calculate() {
        if (currentInput.length() > 0) {
            // Add the final number to the expression
            if (expression.length() > 0) {
                expression.append(" ");
            }
            expression.append(currentInput.toString());
            
            // Set the current value in logic
            double number = Double.parseDouble(currentInput.toString());
            logic.setCurrentValue(number);
            currentInput.setLength(0);
        }
        
        // Get the final expression string
        String finalExpression = expression.toString();
        
        // Calculate the result
        String result = logic.calculate();
        
        // Add to history
        logic.addToHistory(finalExpression, result);
        
        // Display the result
        displayField.setText(result);
        
        // Keep the result for chaining operations
        expression.setLength(0);
        expression.append(result);
        waitingForNumber = true;
        
        // Update history display
        updateHistory();
    }
    
    /**
     * Clears the calculator
     */
    private void clear() {
        logic.reset();
        currentInput.setLength(0);
        expression.setLength(0);
        displayField.setText("0");
        waitingForNumber = true;
        updateHistory();
        updateRadDegButton();
        updateInvButton();
    }
    
    /**
     * Updates the display to show the current expression
     */
    private void updateDisplay() {
        StringBuilder display = new StringBuilder();
        
        // Add the expression
        if (expression.length() > 0) {
            display.append(expression);
        }
        
        // Add the current input
        if (currentInput.length() > 0) {
            if (display.length() > 0) {
                display.append(" ");
            }
            display.append(currentInput.toString());
        }
        
        // If nothing to display, show 0
        if (display.length() == 0) {
            display.append("0");
        }
        
        displayField.setText(display.toString());
    }
    
    /**
     * Updates the history display
     */
    private void updateHistory() {
        StringBuilder historyText = new StringBuilder();
        for (String calculation : logic.getHistory()) {
            historyText.append(calculation).append("\n");
        }
        historyArea.setText(historyText.toString());
    }
}
