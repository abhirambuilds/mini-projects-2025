"""
Expense Tracker - Desktop Application
A comprehensive expense tracking application built with Python Tkinter.

Features:
- Track income and expenses in Rupees (₹)
- Monthly salary income management
- Category-based expense tracking
- Advanced filtering and visualization
- CSV data persistence
- Sample data for 1 year of transactions

Usage: python main.py
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import os
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import defaultdict
import calendar

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("💰 Expense Tracker")
        self.root.geometry("1600x1000")
        self.root.configure(bg="#f8f9fa")  # Light background
        
        # Set matplotlib style for cleaner charts
        try:
            plt.style.use('seaborn-v0_8-whitegrid')
        except:
            plt.style.use('seaborn-whitegrid')
        plt.rcParams['font.size'] = 10
        plt.rcParams['axes.titlesize'] = 12
        plt.rcParams['axes.labelsize'] = 10
        
        # Data storage
        self.transactions = []
        self.csv_file = "transactions.csv"
        self.categories = [
            "Groceries", "Rent", "School Fees", "Electricity", "Travel", 
            "Savings", "Entertainment", "Healthcare", "Shopping", "Bills",
            "Transport", "Education", "Miscellaneous"
        ]
        
        # Income categories
        self.income_categories = ["Salary Income", "Side Income", "Interest", "Other"]
        
        # Monthly salary (fixed)
        self.monthly_salary = 50000
        
        # Load existing transactions
        self.load_transactions()
        
        # Create GUI
        self.create_widgets()
        self.update_display()
        
    def create_widgets(self):
        # Create main scrollable canvas
        self.main_canvas = tk.Canvas(self.root, bg="#f0f8ff")  # Cooler light blue background
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.main_canvas.yview)
        self.scrollable_frame = tk.Frame(self.main_canvas, bg="#f0f8ff")
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
        )
        
        self.main_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.main_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Main title with better styling and center alignment
        title_frame = tk.Frame(self.scrollable_frame, bg="#f0f8ff")
        title_frame.pack(fill="x", pady=(20, 15))
        
        title_label = tk.Label(
            title_frame, 
            text="💰 Expense Tracker", 
            font=("Segoe UI", 32, "bold"), 
            bg="#f0f8ff", 
            fg="#1e3a8a"
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="Smart Financial Management & Analytics",
            font=("Segoe UI", 14),
            bg="#f0f8ff",
            fg="#3b82f6"
        )
        subtitle_label.pack(pady=(8, 0))
        
        # Summary frame with better design
        self.create_summary_frame()
        
        # Input frame with improved styling
        self.create_input_frame()
        
        # Filter frame with better layout
        self.create_filter_frame()
        
        # Transactions table (moved above charts)
        self.create_transactions_table()
        
        # Charts frame (moved below transactions)
        self.create_charts_frame()
        
        # Buttons frame with better organization
        self.create_buttons_frame()
        
        # Pack canvas and scrollbar
        self.main_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mouse wheel to scroll
        self.root.bind("<MouseWheel>", self._on_mousewheel)
        
    def _on_mousewheel(self, event):
        self.main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
    def create_summary_frame(self):
        summary_frame = tk.Frame(self.scrollable_frame, bg="#ffffff", relief="flat", bd=0)
        summary_frame.pack(fill="x", padx=30, pady=15)
        
        # Summary title with better styling and center alignment
        summary_title = tk.Label(
            summary_frame, 
            text="📊 Financial Summary", 
            font=("Segoe UI", 20, "bold"), 
            bg="#ffffff", 
            fg="#1e3a8a"
        )
        summary_title.pack(pady=(20, 15))
        
        # Summary values frame with grid layout
        summary_values = tk.Frame(summary_frame, bg="#ffffff")
        summary_values.pack(pady=(0, 20))
        
        # Create summary cards with cooler colors
        self.create_summary_card(summary_values, "Total Income", "₹0.00", "#10b981", 0, 0)
        self.create_summary_card(summary_values, "Total Expenses", "₹0.00", "#ef4444", 0, 1)
        self.create_summary_card(summary_values, "Balance", "₹0.00", "#3b82f6", 0, 2)
        self.create_summary_card(summary_values, "Monthly Salary", f"₹{self.monthly_salary:,.2f}", "#f59e0b", 0, 3)
        
    def create_summary_card(self, parent, title, value, color, row, col):
        """Create a styled summary card with center alignment"""
        card_frame = tk.Frame(parent, bg="#f8fafc", relief="flat", bd=0)
        card_frame.grid(row=row, column=col, padx=12, pady=6, sticky="ew")
        
        # Title with center alignment
        title_label = tk.Label(
            card_frame,
            text=title,
            font=("Segoe UI", 12, "bold"),
            bg="#f8fafc",
            fg="#475569"
        )
        title_label.pack(pady=(12, 6))
        
        # Value with center alignment
        value_label = tk.Label(
            card_frame,
            text=value,
            font=("Segoe UI", 18, "bold"),
            bg="#f8fafc",
            fg=color
        )
        value_label.pack(pady=(0, 12))
        
        # Store reference for updating
        if title == "Total Income":
            self.income_label = value_label
        elif title == "Total Expenses":
            self.expenses_label = value_label
        elif title == "Balance":
            self.balance_label = value_label
        elif title == "Monthly Salary":
            self.salary_label = value_label
        
    def create_input_frame(self):
        input_frame = tk.Frame(self.scrollable_frame, bg="#ffffff", relief="flat", bd=0)
        input_frame.pack(fill="x", padx=30, pady=15)
        
        # Input title with better styling and center alignment
        input_title = tk.Label(
            input_frame, 
            text="➕ Add New Transaction", 
            font=("Segoe UI", 18, "bold"), 
            bg="#ffffff", 
            fg="#1e3a8a"
        )
        input_title.pack(pady=(20, 15))
        
        # Input fields frame with better layout and center alignment
        input_fields = tk.Frame(input_frame, bg="#ffffff")
        input_fields.pack(pady=15)
        
        # Transaction type with center alignment
        tk.Label(input_fields, text="Type:", bg="#ffffff", font=("Segoe UI", 11, "bold"), fg="#374151").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.type_var = tk.StringVar(value="Expense")
        self.type_combo = ttk.Combobox(input_fields, textvariable=self.type_var, values=["Expense", "Income"], width=15, state="readonly")
        self.type_combo.grid(row=0, column=1, padx=10, pady=10)
        self.type_combo.bind("<<ComboboxSelected>>", self.on_type_change)
        
        # Description with center alignment
        tk.Label(input_fields, text="Description:", bg="#ffffff", font=("Segoe UI", 11, "bold"), fg="#374151").grid(row=0, column=2, padx=10, pady=10, sticky="e")
        self.description_entry = tk.Entry(input_fields, width=35, font=("Segoe UI", 11), relief="flat", bd=2, bg="#f1f5f9", fg="#1f2937")
        self.description_entry.grid(row=0, column=3, padx=10, pady=10)
        
        # Amount with center alignment
        tk.Label(input_fields, text="Amount (₹):", bg="#ffffff", font=("Segoe UI", 11, "bold"), fg="#374151").grid(row=0, column=4, padx=10, pady=10, sticky="e")
        self.amount_entry = tk.Entry(input_fields, width=20, font=("Segoe UI", 11), relief="flat", bd=2, bg="#f1f5f9", fg="#1f2937")
        self.amount_entry.grid(row=0, column=5, padx=10, pady=10)
        
        # Category with center alignment
        tk.Label(input_fields, text="Category:", bg="#ffffff", font=("Segoe UI", 11, "bold"), fg="#374151").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.category_var = tk.StringVar(value=self.categories[0])
        self.category_combo = ttk.Combobox(input_fields, textvariable=self.category_var, values=self.categories, width=20, state="readonly")
        self.category_combo.grid(row=1, column=1, padx=10, pady=10)
        
        # Date with center alignment
        tk.Label(input_fields, text="Date:", bg="#ffffff", font=("Segoe UI", 11, "bold"), fg="#374151").grid(row=1, column=2, padx=10, pady=10, sticky="e")
        self.date_entry = tk.Entry(input_fields, width=20, font=("Segoe UI", 11), relief="flat", bd=2, bg="#f1f5f9", fg="#1f2937")
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.date_entry.grid(row=1, column=3, padx=10, pady=10)
        
        # Add button with better styling and center alignment
        add_button = tk.Button(
            input_fields, 
            text="➕ Add Transaction", 
            command=self.add_transaction,
            bg="#10b981", 
            fg="white", 
            font=("Segoe UI", 12, "bold"),
            relief="flat",
            padx=30,
            pady=10,
            cursor="hand2"
        )
        add_button.grid(row=1, column=4, columnspan=2, padx=20, pady=10)
        
        # Bind hover effects
        add_button.bind("<Enter>", lambda e: add_button.configure(bg="#059669"))
        add_button.bind("<Leave>", lambda e: add_button.configure(bg="#10b981"))
        
    def on_type_change(self, event=None):
        """Update category options based on transaction type"""
        if self.type_var.get() == "Income":
            self.category_combo['values'] = self.income_categories
            self.category_var.set(self.income_categories[0])
        else:
            self.category_combo['values'] = self.categories
            self.category_var.set(self.categories[0])
        
    def create_filter_frame(self):
        filter_frame = tk.Frame(self.scrollable_frame, bg="#ffffff", relief="flat", bd=0)
        filter_frame.pack(fill="x", padx=30, pady=15)
        
        # Filter title with better styling and center alignment
        filter_title = tk.Label(
            filter_frame, 
            text="🔍 Filter Transactions", 
            font=("Segoe UI", 18, "bold"), 
            bg="#ffffff", 
            fg="#1e3a8a"
        )
        filter_title.pack(pady=(20, 15))
        
        # Filter controls frame with better layout and center alignment
        filter_controls = tk.Frame(filter_frame, bg="#ffffff")
        filter_controls.pack(pady=15)
        
        # Category filter with center alignment
        tk.Label(filter_controls, text="Category:", bg="#ffffff", font=("Segoe UI", 11, "bold"), fg="#374151").pack(side="left", padx=10)
        self.filter_category_var = tk.StringVar(value="All")
        filter_category_combo = ttk.Combobox(filter_controls, textvariable=self.filter_category_var, values=["All"] + self.categories + self.income_categories, width=20, state="readonly")
        filter_category_combo.pack(side="left", padx=10)
        
        # Month filter with center alignment
        tk.Label(filter_controls, text="Month:", bg="#ffffff", font=("Segoe UI", 11, "bold"), fg="#374151").pack(side="left", padx=10)
        self.filter_month_var = tk.StringVar(value="All")
        months = ["All"] + [calendar.month_name[i] for i in range(1, 13)]
        filter_month_combo = ttk.Combobox(filter_controls, textvariable=self.filter_month_var, values=months, width=20, state="readonly")
        filter_month_combo.pack(side="left", padx=10)
        
        # Year filter with center alignment
        tk.Label(filter_controls, text="Year:", bg="#ffffff", font=("Segoe UI", 11, "bold"), fg="#374151").pack(side="left", padx=10)
        self.filter_year_var = tk.StringVar(value="All")
        current_year = datetime.now().year
        years = ["All"] + [str(year) for year in range(current_year-1, current_year+2)]
        filter_year_combo = ttk.Combobox(filter_controls, textvariable=self.filter_year_var, values=years, width=15, state="readonly")
        filter_year_combo.pack(side="left", padx=10)
        
        # Apply filter button with better styling and center alignment
        apply_filter_button = tk.Button(
            filter_controls, 
            text="🔍 Apply Filter", 
            command=self.apply_filter,
            bg="#f59e0b", 
            fg="white", 
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            padx=25,
            pady=8,
            cursor="hand2"
        )
        apply_filter_button.pack(side="left", padx=20)
        
        # Clear filter button with better styling and center alignment
        clear_filter_button = tk.Button(
            filter_controls, 
            text="🔄 Clear Filter", 
            command=self.clear_filter,
            bg="#3b82f6", 
            fg="white", 
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            padx=25,
            pady=8,
            cursor="hand2"
        )
        clear_filter_button.pack(side="left", padx=10)
        
        # Bind hover effects
        apply_filter_button.bind("<Enter>", lambda e: apply_filter_button.configure(bg="#d97706"))
        apply_filter_button.bind("<Leave>", lambda e: apply_filter_button.configure(bg="#f59e0b"))
        clear_filter_button.bind("<Enter>", lambda e: clear_filter_button.configure(bg="#2563eb"))
        clear_filter_button.bind("<Leave>", lambda e: clear_filter_button.configure(bg="#3b82f6"))
        
    def create_transactions_table(self):
        """Create transactions table (moved above charts)"""
        table_frame = tk.Frame(self.scrollable_frame, bg="#ffffff", relief="flat", bd=0)
        table_frame.pack(fill="both", expand=True, padx=30, pady=15)
        
        # Table title with better styling and center alignment
        table_title = tk.Label(
            table_frame, 
            text="📋 Transaction History", 
            font=("Segoe UI", 18, "bold"), 
            bg="#ffffff", 
            fg="#1e3a8a"
        )
        table_title.pack(pady=(20, 15))
        
        # Create Treeview with scrollbar
        tree_frame = tk.Frame(table_frame, bg="#ffffff")
        tree_frame.pack(fill="both", expand=True, padx=15, pady=10)
        
        # Treeview with better styling
        columns = ("Date", "Description", "Amount (₹)", "Category", "Type")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=12)
        
        # Configure columns with better widths and center alignment
        for col in columns:
            self.tree.heading(col, text=col)
            if col == "Amount (₹)":
                self.tree.column(col, width=150, anchor="center")
            elif col == "Date":
                self.tree.column(col, width=130, anchor="center")
            elif col == "Description":
                self.tree.column(col, width=320, anchor="center")
            elif col == "Category":
                self.tree.column(col, width=160, anchor="center")
            else:
                self.tree.column(col, width=130, anchor="center")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind double-click to edit
        self.tree.bind("<Double-1>", self.edit_transaction)
        
        # Configure alternating row colors with cooler colors
        self.tree.tag_configure("oddrow", background="#f8fafc")
        self.tree.tag_configure("evenrow", background="#ffffff")
        
    def create_charts_frame(self):
        """Create charts frame (moved below transactions)"""
        charts_frame = tk.Frame(self.scrollable_frame, bg="#ffffff", relief="flat", bd=0)
        charts_frame.pack(fill="x", padx=30, pady=15)
        
        # Charts title with better styling and center alignment
        charts_title = tk.Label(
            charts_frame, 
            text="📊 Financial Analytics", 
            font=("Segoe UI", 18, "bold"), 
            bg="#ffffff", 
            fg="#1e3a8a"
        )
        charts_title.pack(pady=(20, 15))
        
        # Charts container (side by side)
        charts_container = tk.Frame(charts_frame, bg="#ffffff")
        charts_container.pack(pady=10)
        
        # Pie chart frame with center alignment
        pie_frame = tk.Frame(charts_container, bg="#ffffff")
        pie_frame.pack(side="left", padx=20)
        
        pie_title = tk.Label(pie_frame, text="Expense Breakdown by Category", font=("Segoe UI", 14, "bold"), bg="#ffffff", fg="#1e3a8a")
        pie_title.pack(pady=(0, 15))
        
        # Create matplotlib figure for pie chart with better styling
        self.fig_pie, self.ax_pie = plt.subplots(figsize=(8, 6), facecolor='#ffffff')
        self.canvas_pie = FigureCanvasTkAgg(self.fig_pie, pie_frame)
        self.canvas_pie.get_tk_widget().pack()
        
        # Bar chart frame with center alignment
        bar_frame = tk.Frame(charts_container, bg="#ffffff")
        bar_frame.pack(side="right", padx=20)
        
        bar_title = tk.Label(bar_frame, text="Monthly Income vs Expenses", font=("Segoe UI", 14, "bold"), bg="#ffffff", fg="#1e3a8a")
        bar_title.pack(pady=(0, 15))
        
        # Create matplotlib figure for bar chart with better styling
        self.fig_bar, self.ax_bar = plt.subplots(figsize=(10, 6), facecolor='#ffffff')
        self.canvas_bar = FigureCanvasTkAgg(self.fig_bar, bar_frame)
        self.canvas_bar.get_tk_widget().pack()
        
    def create_buttons_frame(self):
        """Create buttons frame with better organization and center alignment"""
        buttons_frame = tk.Frame(self.scrollable_frame, bg="#f0f8ff")
        buttons_frame.pack(fill="x", padx=30, pady=20)
        
        # Left side buttons with center alignment
        left_buttons = tk.Frame(buttons_frame, bg="#f0f8ff")
        left_buttons.pack(side="left")
        
        # Save button with better styling
        save_button = tk.Button(
            left_buttons, 
            text="💾 Save to CSV", 
            command=self.save_transactions,
            bg="#10b981", 
            fg="white", 
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            padx=25,
            pady=10,
            cursor="hand2"
        )
        save_button.pack(side="left", padx=8)
        
        # Load button with better styling
        load_button = tk.Button(
            left_buttons, 
            text="📂 Load from CSV", 
            command=self.load_from_file,
            bg="#3b82f6", 
            fg="white", 
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            padx=25,
            pady=10,
            cursor="hand2"
        )
        load_button.pack(side="left", padx=8)
        
        # Export button with better styling
        export_button = tk.Button(
            left_buttons, 
            text="📤 Export Report", 
            command=self.export_report,
            bg="#f59e0b", 
            fg="white", 
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            padx=25,
            pady=10,
            cursor="hand2"
        )
        export_button.pack(side="left", padx=8)
        
        # Generate sample data button with better styling
        sample_button = tk.Button(
            left_buttons, 
            text="🎲 Generate Sample Data", 
            command=self.generate_sample_data,
            bg="#8b5cf6", 
            fg="white", 
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            padx=25,
            pady=10,
            cursor="hand2"
        )
        sample_button.pack(side="left", padx=8)
        
        # Right side button with better styling
        clear_all_button = tk.Button(
            buttons_frame, 
            text="🗑️ Clear All", 
            command=self.clear_all_transactions,
            bg="#ef4444", 
            fg="white", 
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            padx=25,
            pady=10,
            cursor="hand2"
        )
        clear_all_button.pack(side="right", padx=8)
        
        # Bind hover effects for all buttons with cooler colors
        for button in [save_button, load_button, export_button, sample_button, clear_all_button]:
            original_color = button.cget("bg")
            button.bind("<Enter>", lambda e, b=button, c=original_color: b.configure(bg=self.get_hover_color(c)))
            button.bind("<Leave>", lambda e, b=button, c=original_color: b.configure(bg=c))
    
    def get_hover_color(self, original_color):
        """Get hover color based on original color with cooler colors"""
        color_map = {
            "#10b981": "#059669",  # Green
            "#3b82f6": "#2563eb",  # Blue
            "#f59e0b": "#d97706",  # Orange
            "#8b5cf6": "#7c3aed",  # Purple
            "#ef4444": "#dc2626"   # Red
        }
        return color_map.get(original_color, original_color)

    def add_transaction(self):
        description = self.description_entry.get().strip()
        amount_str = self.amount_entry.get().strip()
        category = self.category_var.get()
        transaction_type = self.type_var.get()
        date_str = self.date_entry.get().strip()
        
        # Validation
        if not description:
            messagebox.showerror("Error", "Please enter a description")
            return
            
        try:
            amount = float(amount_str)
            if amount <= 0:
                messagebox.showerror("Error", "Amount must be greater than 0")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")
            return
            
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid date (YYYY-MM-DD)")
            return
            
        # Create transaction
        transaction = {
            "date": date_obj.strftime("%Y-%m-%d"),
            "description": description,
            "amount": amount,
            "category": category,
            "type": transaction_type
        }
        
        self.transactions.append(transaction)
        
        # Clear input fields
        self.description_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        
        # Update display
        self.update_display()
        self.save_transactions()
        
        messagebox.showinfo("Success", "Transaction added successfully!")
        
    def edit_transaction(self, event):
        selection = self.tree.selection()
        if not selection:
            return
            
        item = self.tree.item(selection[0])
        values = item['values']
        
        # Create edit dialog with better styling and center alignment
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Transaction")
        edit_window.geometry("550x500")
        edit_window.configure(bg="#ffffff")
        edit_window.resizable(False, False)
        
        # Center the window
        edit_window.transient(self.root)
        edit_window.grab_set()
        
        # Title with center alignment
        title_label = tk.Label(
            edit_window, 
            text="✏️ Edit Transaction", 
            font=("Segoe UI", 20, "bold"), 
            bg="#ffffff", 
            fg="#1e3a8a"
        )
        title_label.pack(pady=(25, 30))
        
        # Edit fields container with center alignment
        fields_frame = tk.Frame(edit_window, bg="#ffffff")
        fields_frame.pack(pady=15, padx=35, fill="x")
        
        # Description with center alignment
        tk.Label(fields_frame, text="Description:", bg="#ffffff", font=("Segoe UI", 12, "bold"), fg="#374151").pack(anchor="w", pady=(0, 8))
        desc_entry = tk.Entry(fields_frame, width=50, font=("Segoe UI", 11), relief="flat", bd=2, bg="#f1f5f9", fg="#1f2937")
        desc_entry.insert(0, values[1])
        desc_entry.pack(fill="x", pady=(0, 20))
        
        # Amount with center alignment
        tk.Label(fields_frame, text="Amount (₹):", bg="#ffffff", font=("Segoe UI", 12, "bold"), fg="#374151").pack(anchor="w", pady=(0, 8))
        amount_entry = tk.Entry(fields_frame, width=50, font=("Segoe UI", 11), relief="flat", bd=2, bg="#f1f5f9", fg="#1f2937")
        # Remove ₹ symbol and commas for editing
        amount_str = values[2].replace("₹", "").replace(",", "")
        amount_entry.insert(0, amount_str)
        amount_entry.pack(fill="x", pady=(0, 20))
        
        # Category with center alignment
        tk.Label(fields_frame, text="Category:", bg="#ffffff", font=("Segoe UI", 12, "bold"), fg="#374151").pack(anchor="w", pady=(0, 8))
        cat_var = tk.StringVar(value=values[3])
        if values[4] == "Income":
            cat_combo = ttk.Combobox(fields_frame, textvariable=cat_var, values=self.income_categories, state="readonly", width=47)
        else:
            cat_combo = ttk.Combobox(fields_frame, textvariable=cat_var, values=self.categories, state="readonly", width=47)
        cat_combo.pack(fill="x", pady=(0, 20))
        
        # Type with center alignment
        tk.Label(fields_frame, text="Type:", bg="#ffffff", font=("Segoe UI", 12, "bold"), fg="#374151").pack(anchor="w", pady=(0, 8))
        type_var = tk.StringVar(value=values[4])
        type_combo = ttk.Combobox(fields_frame, textvariable=type_var, values=["Income", "Expense"], state="readonly", width=47)
        type_combo.pack(fill="x", pady=(0, 20))
        
        # Date with center alignment
        tk.Label(fields_frame, text="Date:", bg="#ffffff", font=("Segoe UI", 12, "bold"), fg="#374151").pack(anchor="w", pady=(0, 8))
        date_entry = tk.Entry(fields_frame, width=50, font=("Segoe UI", 11), relief="flat", bd=2, bg="#f1f5f9", fg="#1f2937")
        date_entry.insert(0, values[0])
        date_entry.pack(fill="x", pady=(0, 30))
        
        # Buttons frame with center alignment
        buttons_frame = tk.Frame(edit_window, bg="#ffffff")
        buttons_frame.pack(pady=25)
        
        # Save button with better styling
        def save_changes():
            try:
                new_amount = float(amount_entry.get())
                if new_amount <= 0:
                    messagebox.showerror("Error", "Amount must be greater than 0")
                    return
                    
                # Update transaction
                index = self.tree.index(selection[0])
                self.transactions[index]["description"] = desc_entry.get()
                self.transactions[index]["amount"] = new_amount
                self.transactions[index]["category"] = cat_var.get()
                self.transactions[index]["type"] = type_var.get()
                self.transactions[index]["date"] = date_entry.get()
                
                self.update_display()
                self.save_transactions()
                edit_window.destroy()
                messagebox.showinfo("Success", "Transaction updated successfully!")
                
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid amount")
        
        save_btn = tk.Button(
            buttons_frame, 
            text="💾 Save Changes", 
            command=save_changes, 
            bg="#10b981", 
            fg="white",
            font=("Segoe UI", 12, "bold"),
            relief="flat",
            padx=30,
            pady=10,
            cursor="hand2"
        )
        save_btn.pack(side="left", padx=15)
        
        # Cancel button with better styling
        cancel_btn = tk.Button(
            buttons_frame, 
            text="❌ Cancel", 
            command=edit_window.destroy, 
            bg="#ef4444", 
            fg="white",
            font=("Segoe UI", 12, "bold"),
            relief="flat",
            padx=30,
            pady=10,
            cursor="hand2"
        )
        cancel_btn.pack(side="left", padx=15)
        
        # Bind hover effects with cooler colors
        save_btn.bind("<Enter>", lambda e: save_btn.configure(bg="#059669"))
        save_btn.bind("<Leave>", lambda e: save_btn.configure(bg="#10b981"))
        cancel_btn.bind("<Enter>", lambda e: cancel_btn.configure(bg="#dc2626"))
        cancel_btn.bind("<Leave>", lambda e: cancel_btn.configure(bg="#ef4444"))
        
    def apply_filter(self):
        category_filter = self.filter_category_var.get()
        month_filter = self.filter_month_var.get()
        year_filter = self.filter_year_var.get()
        
        # Clear current display
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Apply filters
        filtered_transactions = []
        for transaction in self.transactions:
            # Category filter
            if category_filter != "All" and transaction["category"] != category_filter:
                continue
                
            # Month filter
            if month_filter != "All":
                transaction_date = datetime.strptime(transaction["date"], "%Y-%m-%d")
                if calendar.month_name[transaction_date.month] != month_filter:
                    continue
                    
            # Year filter
            if year_filter != "All":
                transaction_date = datetime.strptime(transaction["date"], "%Y-%m-%d")
                if str(transaction_date.year) != year_filter:
                    continue
            
            filtered_transactions.append(transaction)
        
        # Display filtered transactions
        self.display_transactions(filtered_transactions)
        
    def clear_filter(self):
        self.filter_category_var.set("All")
        self.filter_month_var.set("All")
        self.filter_year_var.set("All")
        self.update_display()
        
    def display_transactions(self, transactions):
        # Clear current display
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add transactions with alternating colors
        for i, transaction in enumerate(transactions):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            self.tree.insert("", "end", values=(
                transaction["date"],
                transaction["description"],
                f"₹{transaction['amount']:,.2f}",
                transaction["category"],
                transaction["type"]
            ), tags=(tag,))
            
    def update_display(self):
        # Update transactions table
        self.display_transactions(self.transactions)
        
        # Update summary
        total_income = sum(t["amount"] for t in self.transactions if t["type"] == "Income")
        total_expenses = sum(t["amount"] for t in self.transactions if t["type"] == "Expense")
        balance = total_income - total_expenses
        
        self.income_label.config(text=f"Total Income: ₹{total_income:,.2f}")
        self.expenses_label.config(text=f"Total Expenses: ₹{total_expenses:,.2f}")
        self.balance_label.config(text=f"Balance: ₹{balance:,.2f}")
        
        # Update charts
        self.update_pie_chart()
        self.update_bar_chart()
        
    def update_pie_chart(self):
        # Clear previous chart
        self.ax_pie.clear()
        
        # Get expense data by category
        expense_data = defaultdict(float)
        for transaction in self.transactions:
            if transaction["type"] == "Expense":
                expense_data[transaction["category"]] += transaction["amount"]
        
        if not expense_data:
            self.ax_pie.text(0.5, 0.5, "No expense data", ha="center", va="center", 
                            transform=self.ax_pie.transAxes, fontsize=16, color='#1e3a8a')
            self.ax_pie.set_title("Expense Breakdown by Category", color='#1e3a8a', fontsize=16, pad=25)
        else:
            # Create pie chart with better styling
            categories = list(expense_data.keys())
            amounts = list(expense_data.values())
            
            # Color scheme - cooler bright colors
            colors = ['#ef4444', '#3b82f6', '#f59e0b', '#10b981', '#8b5cf6', 
                     '#06b6d4', '#84cc16', '#f97316', '#ec4899', '#6366f1',
                     '#14b8a6', '#fbbf24', '#a855f7']
            
            # Create pie chart with better formatting
            wedges, texts, autotexts = self.ax_pie.pie(
                amounts, 
                labels=categories, 
                autopct='%1.1f%%', 
                colors=colors[:len(categories)],
                startangle=90,
                textprops={'fontsize': 10, 'color': '#1e3a8a'},
                wedgeprops={'edgecolor': '#ffffff', 'linewidth': 3}
            )
            
            # Style the chart
            self.ax_pie.set_title("Expense Breakdown by Category", color='#1e3a8a', fontsize=16, pad=25)
            
            # Style the percentage text
            for autotext in autotexts:
                autotext.set_color('#1e3a8a')
                autotext.set_fontweight('bold')
                autotext.set_fontsize(11)
            
            # Style the category labels
            for text in texts:
                text.set_color('#1e3a8a')
                text.set_fontsize(10)
                text.set_fontweight('bold')
        
        # Set background color
        self.ax_pie.set_facecolor('#ffffff')
        self.fig_pie.patch.set_facecolor('#ffffff')
        
        self.canvas_pie.draw()
        
    def update_bar_chart(self):
        # Clear previous chart
        self.ax_bar.clear()
        
        # Get monthly data
        monthly_data = defaultdict(lambda: {"income": 0, "expenses": 0})
        
        for transaction in self.transactions:
            date_obj = datetime.strptime(transaction["date"], "%Y-%m-%d")
            month_key = f"{date_obj.year}-{date_obj.month:02d}"
            
            if transaction["type"] == "Income":
                monthly_data[month_key]["income"] += transaction["amount"]
            else:
                monthly_data[month_key]["expenses"] += transaction["amount"]
        
        if not monthly_data:
            self.ax_bar.text(0.5, 0.5, "No data available", ha="center", va="center", 
                            transform=self.ax_bar.transAxes, fontsize=16, color='#1e3a8a')
            self.ax_bar.set_title("Monthly Income vs Expenses", color='#1e3a8a', fontsize=16, pad=25)
        else:
            # Sort months
            sorted_months = sorted(monthly_data.keys())
            months = [f"{datetime.strptime(m, '%Y-%m').strftime('%b %Y')}" for m in sorted_months]
            income_values = [monthly_data[m]["income"] for m in sorted_months]
            expense_values = [monthly_data[m]["expenses"] for m in sorted_months]
            
            # Create bar chart with better styling
            x = range(len(months))
            width = 0.35
            
            # Create bars with cooler colors and styling
            income_bars = self.ax_bar.bar([i - width/2 for i in x], income_values, width, 
                                        label='Income', color='#10b981', alpha=0.9, 
                                        edgecolor='#ffffff', linewidth=2)
            expense_bars = self.ax_bar.bar([i + width/2 for i in x], expense_values, width, 
                                         label='Expenses', color='#ef4444', alpha=0.9,
                                         edgecolor='#ffffff', linewidth=2)
            
            # Style the chart
            self.ax_bar.set_xlabel('Month', color='#1e3a8a', fontsize=12)
            self.ax_bar.set_ylabel('Amount (₹)', color='#1e3a8a', fontsize=12)
            self.ax_bar.set_title('Monthly Income vs Expenses', color='#1e3a8a', fontsize=16, pad=25)
            self.ax_bar.set_xticks(x)
            self.ax_bar.set_xticklabels(months, rotation=45, ha='right', color='#1e3a8a', fontsize=10)
            
            # Add legend with better styling
            legend = self.ax_bar.legend(loc='upper right', frameon=True, 
                                      facecolor='#f8fafc', edgecolor='#e2e8f0',
                                      fontsize=11)
            legend.get_texts()[0].set_color('#1e3a8a')
            legend.get_texts()[1].set_color('#1e3a8a')
            
            # Add grid with better styling
            self.ax_bar.grid(True, alpha=0.4, color='#cbd5e1', linestyle='-', linewidth=1)
            
            # Format y-axis labels with better formatting
            self.ax_bar.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'₹{x:,.0f}'))
            
            # Style y-axis labels
            self.ax_bar.tick_params(axis='y', colors='#1e3a8a', labelsize=10)
            
            # Add value labels on bars for better readability
            for i, (income_bar, expense_bar) in enumerate(zip(income_bars, expense_bars)):
                # Income value label
                if income_values[i] > 0:
                    height = income_bar.get_height()
                    self.ax_bar.text(income_bar.get_x() + income_bar.get_width()/2., height + 1000,
                                   f'₹{income_values[i]:,.0f}', ha="center", va="bottom",
                                   fontsize=9, color='#1e3a8a')
                
                # Expense value label
                if expense_values[i] > 0:
                    height = expense_bar.get_height()
                    self.ax_bar.text(expense_bar.get_x() + expense_bar.get_width()/2., height + 1000,
                                   f'₹{expense_values[i]:,.0f}', ha="center", va="bottom",
                                   fontsize=9, color='#1e3a8a')
            
            # Adjust layout to prevent label cutoff
            self.fig_bar.tight_layout()
        
        # Set background color
        self.ax_bar.set_facecolor('#ffffff')
        self.fig_bar.patch.set_facecolor('#ffffff')
        
        self.canvas_bar.draw()
        
    def generate_sample_data(self):
        """Generate 1 year of sample data"""
        if messagebox.askyesno("Confirm", "This will replace all existing data with 1 year of sample transactions. Continue?"):
            self.transactions = []
            
            # Generate data for the past 12 months
            end_date = datetime.now()
            start_date = end_date - timedelta(days=365)
            
            current_date = start_date
            while current_date <= end_date:
                # Add monthly salary on the 1st of each month
                if current_date.day == 1:
                    self.transactions.append({
                        "date": current_date.strftime("%Y-%m-%d"),
                        "description": "Monthly Salary",
                        "amount": self.monthly_salary,
                        "category": "Salary Income",
                        "type": "Income"
                    })
                
                # Add some side income (random)
                if current_date.day == 15 and current_date.month % 3 == 0:
                    side_income = 5000 + (current_date.month * 1000)  # Varies by month
                    self.transactions.append({
                        "date": current_date.strftime("%Y-%m-%d"),
                        "description": "Freelance Project",
                        "amount": side_income,
                        "category": "Side Income",
                        "type": "Income"
                    })
                
                # Add regular expenses
                self.add_regular_expenses(current_date)
                
                # Add some random expenses
                if current_date.day % 3 == 0:  # Every 3rd day
                    self.add_random_expense(current_date)
                
                current_date += timedelta(days=1)
            
            self.update_display()
            self.save_transactions()
            messagebox.showinfo("Success", f"Generated {len(self.transactions)} sample transactions for 1 year!")
    
    def add_regular_expenses(self, date):
        """Add regular monthly expenses"""
        if date.day == 1:  # Rent on 1st
            self.transactions.append({
                "date": date.strftime("%Y-%m-%d"),
                "description": "House Rent",
                "amount": 15000,
                "category": "Rent",
                "type": "Expense"
            })
        
        if date.day == 5:  # Electricity bill
            electricity_amount = 2000 + (date.month * 100)  # Varies by month
            self.transactions.append({
                "date": date.strftime("%Y-%m-%d"),
                "description": "Electricity Bill",
                "amount": electricity_amount,
                "category": "Electricity",
                "type": "Expense"
            })
        
        if date.day == 10:  # School fees
            self.transactions.append({
                "date": date.strftime("%Y-%m-%d"),
                "description": "School Fees",
                "amount": 8000,
                "category": "School Fees",
                "type": "Expense"
            })
        
        if date.day == 15:  # Groceries
            grocery_amount = 3000 + (date.month * 200)  # Varies by month
            self.transactions.append({
                "date": date.strftime("%Y-%m-%d"),
                "description": "Monthly Groceries",
                "amount": grocery_amount,
                "category": "Groceries",
                "type": "Expense"
            })
    
    def add_random_expense(self, date):
        """Add random daily expenses"""
        import random
        
        expense_types = [
            ("Travel", 200, 800),
            ("Entertainment", 500, 2000),
            ("Shopping", 1000, 5000),
            ("Healthcare", 300, 1500),
            ("Miscellaneous", 100, 500)
        ]
        
        expense_type, min_amount, max_amount = random.choice(expense_types)
        amount = random.randint(min_amount, max_amount)
        
        self.transactions.append({
            "date": date.strftime("%Y-%m-%d"),
            "description": f"Daily {expense_type}",
            "amount": amount,
            "category": expense_type,
            "type": "Expense"
        })
        
    def save_transactions(self):
        try:
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=["date", "description", "amount", "category", "type"])
                writer.writeheader()
                writer.writerows(self.transactions)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save transactions: {str(e)}")
            
    def load_transactions(self):
        if os.path.exists(self.csv_file):
            try:
                with open(self.csv_file, 'r', newline='', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    self.transactions = []
                    for row in reader:
                        row["amount"] = float(row["amount"])
                        self.transactions.append(row)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load transactions: {str(e)}")
                self.transactions = []
        else:
            self.transactions = []
            
    def load_from_file(self):
        filename = filedialog.askopenfilename(
            title="Select CSV file",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r', newline='', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    self.transactions = []
                    for row in reader:
                        row["amount"] = float(row["amount"])
                        self.transactions.append(row)
                    
                self.update_display()
                messagebox.showinfo("Success", f"Loaded {len(self.transactions)} transactions from {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {str(e)}")
                
    def export_report(self):
        if not self.transactions:
            messagebox.showwarning("Warning", "No transactions to export")
            return
            
        filename = filedialog.asksaveasfilename(
            title="Save Report",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                # Create detailed report
                report_data = []
                for transaction in self.transactions:
                    report_data.append({
                        "Date": transaction["date"],
                        "Description": transaction["description"],
                        "Amount (₹)": transaction["amount"],
                        "Category": transaction["category"],
                        "Type": transaction["type"]
                    })
                
                # Add summary rows
                total_income = sum(t["amount"] for t in self.transactions if t["type"] == "Income")
                total_expenses = sum(t["amount"] for t in self.transactions if t["type"] == "Expense")
                balance = total_income - total_expenses
                
                report_data.extend([
                    {},
                    {"Date": "", "Description": "SUMMARY", "Amount (₹)": "", "Category": "", "Type": ""},
                    {"Date": "", "Description": "Total Income", "Amount (₹)": total_income, "Category": "", "Type": ""},
                    {"Date": "", "Description": "Total Expenses", "Amount (₹)": total_expenses, "Category": "", "Type": ""},
                    {"Date": "", "Description": "Balance", "Amount (₹)": balance, "Category": "", "Type": ""}
                ])
                
                # Save report
                with open(filename, 'w', newline='', encoding='utf-8') as file:
                    if report_data:
                        writer = csv.DictWriter(file, fieldnames=report_data[0].keys())
                        writer.writeheader()
                        writer.writerows(report_data)
                
                messagebox.showinfo("Success", f"Report exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export report: {str(e)}")
                
    def clear_all_transactions(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all transactions? This action cannot be undone."):
            self.transactions = []
            self.update_display()
            self.save_transactions()
            messagebox.showinfo("Success", "All transactions cleared")

def main():
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()

if __name__ == "__main__":
    main()
