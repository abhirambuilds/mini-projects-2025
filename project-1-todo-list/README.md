# ✨ To-Do List Web App

A modern, fully functional To-Do List application built with vanilla HTML, CSS, and JavaScript. Features a beautiful, responsive design with smooth animations and drag-and-drop functionality.

## 🚀 Features

### Core Functionality
- **Add Tasks**: Create new tasks with a clean input interface
- **Edit Tasks**: Click the edit button to modify existing tasks inline
- **Delete Tasks**: Remove tasks with confirmation dialog
- **Mark Complete**: Toggle task completion with animated checkboxes
- **Drag & Drop**: Reorder tasks by dragging them to new positions
 - **Due Dates**: Add an optional due date when creating tasks
 - **Time Filters**: Filter tasks by month and year

### User Experience
- **Filtering**: View All, Pending, or Completed tasks
- **Statistics**: Real-time count of total and completed tasks
- **Persistent Storage**: Tasks are saved in browser LocalStorage
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Smooth Animations**: Fade-in effects, hover states, and transitions

### Design Features
- **Modern UI**: Clean, minimal design with a neutral, non-flashy palette
- **Google Fonts**: Uses Poppins font family for excellent readability
- **Subtle Background**: Refined, understated gradient for visual appeal
- **Rounded Edges**: Modern rounded corners throughout the interface
- **Visual Feedback**: Hover effects and smooth transitions

## 🛠️ Technologies Used

- **HTML5**: Semantic markup and modern HTML features
- **CSS3**: Flexbox, Grid, animations, and responsive design
- **JavaScript ES6+**: Modern JavaScript with arrow functions, template literals, and destructuring
- **LocalStorage API**: Browser storage for data persistence
- **HTML5 Drag & Drop**: Native drag and drop functionality

## 📁 File Structure

```
To-Do List App/
├── index.html          # Main HTML file
├── style.css           # CSS styles and animations
├── script.js           # JavaScript functionality
└── README.md           # This file
```

## 🚀 How to Run

### Option 1: Direct Browser Opening (Recommended)
1. Download or clone this repository to your local machine
2. Navigate to the project folder
3. Double-click on `index.html` to open it in your default web browser
4. The app will load immediately with all functionality available

### Option 2: Using a Local Server
1. Open your terminal/command prompt
2. Navigate to the project directory
3. If you have Python installed:
   - **Python 3**: `python -m http.server 8000`
   - **Python 2**: `python -m SimpleHTTPServer 8000`
4. If you have Node.js installed:
   - Install `http-server`: `npm install -g http-server`
   - Run: `http-server`
5. Open your browser and go to `http://localhost:8000`

### Option 3: Using VS Code Live Server
1. Install the "Live Server" extension in VS Code
2. Right-click on `index.html`
3. Select "Open with Live Server"
4. The app will open in your default browser

## 💡 Usage Instructions

### Adding Tasks
- Type your task in the input field
- Press Enter or click the + button to add
- Tasks are automatically saved to LocalStorage

### Managing Tasks
- **Complete**: Click the circular checkbox to mark as done
- **Edit**: Click the edit (pencil) icon to modify task text
- **Delete**: Click the delete (trash) icon to remove tasks
- **Reorder**: Drag and drop tasks to change their order

### Filtering
- **All**: Shows all tasks (default view)
- **Pending**: Shows only incomplete tasks
- **Completed**: Shows only finished tasks

### Keyboard Shortcuts
- **Enter**: Add new task or save edits
- **Escape**: Cancel editing mode

## 🔧 Browser Compatibility

- ✅ Chrome 60+
- ✅ Firefox 55+
- ✅ Safari 12+
- ✅ Edge 79+
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

## 📱 Responsive Design

The app is fully responsive and optimized for:
- **Desktop**: Full-featured interface with hover effects
- **Tablet**: Touch-friendly interface with larger touch targets
- **Mobile**: Optimized layout with accessible buttons and gestures

## 🎨 Customization

The app uses CSS custom properties and can be easily customized:
- Colors are defined in the CSS file
- Animations can be adjusted in the keyframes section
- Font sizes and spacing can be modified for different preferences

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve the application.

---

**Enjoy organizing your tasks with this beautiful To-Do List app!** ✨

