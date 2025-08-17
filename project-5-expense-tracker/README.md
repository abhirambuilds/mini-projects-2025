💰 Expense Tracker - Desktop Application

A powerful and user-friendly desktop expense tracking application built with Python Tkinter, featuring income management, realistic Indian family sample data, advanced filtering, and CSV persistence.

✨ Features
📊 Financial Overview

Fixed Monthly Income: Manage a fixed salary (default ₹45,000/month)

Real-time Summary: Shows income, expenses, and balance in Rupees (₹)

Auto-Calculation: Balance updates instantly when transactions are added

Visual Indicators: Green = income, Red = expenses

💳 Transaction Management

Add Transactions: Record description, amount, category, and date

Income Tracking: Salary, Side Income, Interest, or Other

Expense Categories: Rent, Groceries, School Fees, Electricity, Transport, Healthcare, Shopping, Entertainment, Bills, Education, Miscellaneous

Validation: Ensures correct input for date and amount

🔍 Smart Filtering

Category Filter: Show only selected categories

Date Filter: Filter by day, month, or year

Combined Filters: Apply multiple filters at once

Quick Reset: Easily clear filters to see all data

📈 Data Visualization

Pie Chart: Breakdown of expenses by category

Bar Chart: Monthly spending trend across 12 months

Dynamic Updates: Charts refresh as transactions change

💾 Data Persistence

CSV Storage: All transactions stored in transactions.csv

Sample Data: Comes preloaded with 1 year of realistic middle-class Indian family income & expenses

Auto-Save: No data loss — everything is saved instantly

🎨 User Interface

Modern Tkinter UI with frames and summary cards

Hover Effects on buttons

Alternating Row Colors in transaction table

Responsive Layout with scrollable transaction history

₹ Currency Support everywhere

🚀 Installation
Prerequisites

Python 3.7+

pip (Python package manager)

Steps
# Step 1: Clone the repo
git clone <repository-url>
cd project-5-expense-tracker

# Step 2: Install dependencies
pip install -r requirements.txt

# Step 3: Run the app
python main.py

📁 Project Structure
project-5-expense-tracker/
├── main.py              # Main Tkinter app
├── transactions.csv     # Transaction data (auto-created)
├── demo.py              # Generates 1 year of sample data
├── requirements.txt     # Dependencies
└── README.md            # Documentation

🎯 Usage Guide
Adding a Transaction

Select Type (Income / Expense)

Enter Description (e.g., "Electricity Bill")

Enter Amount in ₹ (e.g., 2500)

Choose Category (Rent, Groceries, etc.)

Select Date (YYYY-MM-DD)

Click Add Transaction

Editing & Filtering

Edit: Double-click a row to modify transaction

Filter: Choose category, month, or year → results update instantly

Clear Filter: Show all transactions again

Sample Data

Run the demo script to auto-fill with 1 year of realistic transactions:

python demo.py


This generates:

Monthly Salary: ₹45,000

Rent: ₹12,000/month

Groceries: ₹4,000–₹6,000/month

School Fees: ₹6,000/month

Bills (Electricity/Water/Internet): ₹1,000–₹3,000/month

Transport & Miscellaneous daily expenses

Savings & Entertainment variations

Charts

Pie Chart → Expense breakdown by category

Bar Chart → Income vs Expenses per month

📊 CSV Format
date,description,amount,category,type
2025-01-01,Monthly Salary,45000,Salary Income,Income
2025-01-02,House Rent,12000,Rent,Expense
2025-01-05,Groceries,4500,Groceries,Expense

🔧 Customization

Change Salary → Edit self.monthly_salary in main.py

Add Categories → Update categories list in main.py

Colors & Fonts → Modify in create_widgets()

🐛 Troubleshooting

No charts showing → Install matplotlib: pip install matplotlib

CSV error → Delete corrupted transactions.csv (auto recreated)

App won’t start → Ensure Python 3.7+ and Tkinter installed

🚀 Future Improvements

Multi-user support

Budget limits per category

Export reports to PDF/Excel

Dark mode

AI-based expense predictions

📄 License

This project is open-source under the MIT License.

🙏 Acknowledgments

Built with Python Tkinter

Charts powered by Matplotlib

Inspired by real Indian middle-class family expense patterns

Track, Save & Plan Smarter – with your Expense Tracker 💰📊