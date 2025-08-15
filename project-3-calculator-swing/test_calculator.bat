@echo off
echo Testing Scientific Calculator...
echo.
echo Compiling...
javac *.java
if %errorlevel% neq 0 (
    echo Compilation failed!
    pause
    exit /b 1
)
echo Compilation successful!
echo.
echo Starting scientific calculator...
echo.
echo Instructions:
echo 1. Click number buttons (1, 2, 3, etc.)
echo 2. Click operator buttons (+, -, ×, ÷, %)
echo 3. Click scientific function buttons (sin, cos, tan, ln, log, √, x!, etc.)
echo 4. Try constants: π (pi) and e
echo 5. Toggle modes: Rad/Deg and Inv (inverse)
echo 6. Click equals (=) to see result
echo 7. Click AC to clear
echo.
echo All scientific functions should now work properly!
echo.
java Main
pause
