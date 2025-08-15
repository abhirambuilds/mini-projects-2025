/**
 * To-Do List App - JavaScript Implementation
 * 
 * This script provides a fully functional to-do list application with the following features:
 * - Add, edit, delete, and mark tasks as completed
 * - Drag-and-drop reordering of tasks
 * - LocalStorage persistence for data persistence across browser sessions
 * - Filtering: All, Pending, and Completed tasks
 * - Smooth animations and visual feedback
 * 
 * Architecture:
 * - Uses ES6+ features (const/let, arrow functions, template literals, destructuring)
 * - Modular design with separate functions for each operation
 * - Event delegation for efficient event handling
 * - LocalStorage API for data persistence
 * - HTML5 Drag and Drop API for task reordering
 */

// Global variables
let tasks = [];
let currentFilter = 'all';
let draggedElement = null;
let selectedMonth = '';
let selectedYear = '';

// DOM elements
const taskInput = document.getElementById('taskInput');
const addTaskBtn = document.getElementById('addTaskBtn');
const taskList = document.getElementById('taskList');
const emptyState = document.getElementById('emptyState');
const taskCount = document.getElementById('taskCount');
const completedCount = document.getElementById('completedCount');
const filterBtns = document.querySelectorAll('.filter-btn');
const dueDateInput = document.getElementById('dueDateInput');
const filterMonthSelect = document.getElementById('filterMonth');
const filterYearSelect = document.getElementById('filterYear');

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    loadTasksFromStorage();
    setupEventListeners();
    renderTasks();
    updateStats();
    refreshTimeFilters();
});

/**
 * Sets up all event listeners for the application
 */
function setupEventListeners() {
    // Add task button and Enter key
    addTaskBtn.addEventListener('click', addTask);
    taskInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') addTask();
    });

    // Filter buttons
    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            setFilter(btn.dataset.filter);
        });
    });

    // Month/Year filters
    if (filterMonthSelect && filterYearSelect) {
        filterMonthSelect.addEventListener('change', () => {
            selectedMonth = filterMonthSelect.value; // '' or '01'..'12'
            renderTasks();
        });
        filterYearSelect.addEventListener('change', () => {
            selectedYear = filterYearSelect.value; // '' or '2025'
            renderTasks();
        });
    }

    // Task list event delegation
    taskList.addEventListener('click', handleTaskActions);
    taskList.addEventListener('change', handleCheckboxChange);
    
    // Drag and drop events
    taskList.addEventListener('dragstart', handleDragStart);
    taskList.addEventListener('dragover', handleDragOver);
    taskList.addEventListener('drop', handleDrop);
    taskList.addEventListener('dragend', handleDragEnd);
}

/**
 * Adds a new task to the list
 */
function addTask() {
    const text = taskInput.value.trim();
    if (!text) return;

    const newTask = {
        id: Date.now().toString(),
        text: text,
        completed: false,
        dueDate: (dueDateInput && dueDateInput.value) ? dueDateInput.value : '', // YYYY-MM-DD
        createdAt: new Date().toISOString()
    };

    tasks.unshift(newTask); // Add to beginning of array
    saveTasksToStorage();
    renderTasks();
    updateStats();
    refreshTimeFilters();
    
    // Clear input and focus
    taskInput.value = '';
    taskInput.focus();
    if (dueDateInput) dueDateInput.value = '';
    
    // Show success feedback
    showTaskAddedFeedback();
}

/**
 * Shows visual feedback when a task is added
 */
function showTaskAddedFeedback() {
    addTaskBtn.style.transform = 'scale(1.2)';
    setTimeout(() => {
        addTaskBtn.style.transform = 'scale(1)';
    }, 200);
}

/**
 * Handles all task-related actions (edit, delete)
 */
function handleTaskActions(e) {
    const target = e.target;
    const taskItem = target.closest('.task-item');
    if (!taskItem) return;

    const taskId = taskItem.dataset.taskId;

    // Robust click handling using closest on buttons
    if (target.closest('.edit-btn')) {
        editTask(taskId);
    } else if (target.closest('.delete-btn')) {
        deleteTask(taskId);
    }
}

/**
 * Handles checkbox state changes
 */
function handleCheckboxChange(e) {
    if (e.target.classList.contains('task-checkbox')) {
        const taskItem = e.target.closest('.task-item');
        const taskId = taskItem.dataset.taskId;
        toggleTaskCompletion(taskId);
    }
}

/**
 * Toggles the completion status of a task
 */
function toggleTaskCompletion(taskId) {
    const task = tasks.find(t => t.id === taskId);
    if (task) {
        task.completed = !task.completed;
        saveTasksToStorage();
        renderTasks();
        updateStats();
    }
}

/**
 * Edits an existing task
 */
function editTask(taskId) {
    const task = tasks.find(t => t.id === taskId);
    if (!task) return;
    
    const taskItem = document.querySelector(`[data-task-id="${taskId}"]`);
    const taskText = taskItem.querySelector('.task-text');
    const dueBadge = taskItem.querySelector('.task-due');
    
    // Create input field for editing
    const input = document.createElement('input');
    input.type = 'text';
    input.value = task.text;
    input.className = 'edit-input';
    input.style.cssText = `
        border: 2px solid #667eea;
        border-radius: 8px;
        padding: 0.5rem;
        font-size: 1rem;
        font-family: inherit;
        width: 100%;
        outline: none;
    `;
    
    // Replace text with input
    const originalText = taskText.textContent;
    taskText.textContent = '';
    taskText.appendChild(input);
    input.focus();
    input.select();
    
    // Handle save and cancel
    const handleEdit = () => {
        const newText = input.value.trim();
        if (newText && newText !== originalText) {
            task.text = newText;
            saveTasksToStorage();
            renderTasks();
        } else {
            taskText.textContent = originalText;
        }
    };
    
    const handleCancel = () => {
        taskText.textContent = originalText;
    };
    
    input.addEventListener('blur', handleEdit);
    input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleEdit();
        } else if (e.key === 'Escape') {
            handleCancel();
        }
    });
}

/**
 * Deletes a task from the list
 */
function deleteTask(taskId) {
    if (confirm('Are you sure you want to delete this task?')) {
        tasks = tasks.filter(t => t.id !== taskId);
        saveTasksToStorage();
        renderTasks();
        updateStats();
        refreshTimeFilters();
    }
}

/**
 * Sets the current filter and updates the UI
 */
function setFilter(filter) {
    currentFilter = filter;
    
    // Update active filter button
    filterBtns.forEach(btn => {
        btn.classList.toggle('active', btn.dataset.filter === filter);
    });
    
    renderTasks();
}

/**
 * Renders all tasks based on current filter
 */
function renderTasks() {
    const filteredTasks = getFilteredTasks();
    
    if (filteredTasks.length === 0) {
        taskList.innerHTML = '';
        emptyState.style.display = 'block';
        return;
    }
    
    emptyState.style.display = 'none';
    
    taskList.innerHTML = filteredTasks.map(task => `
        <li class="task-item ${task.completed ? 'completed' : ''}" 
            data-task-id="${task.id}" 
            draggable="true">
            <div class="task-content">
                <div class="task-checkbox ${task.completed ? 'checked' : ''}"></div>
                <span class="task-text">${escapeHtml(task.text)}</span>
                ${renderDueDate(task.dueDate)}
                <div class="task-actions">
                    <button class="action-btn edit-btn" title="Edit task">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                        </svg>
                    </button>
                    <button class="action-btn delete-btn" title="Delete task">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <polyline points="3,6 5,6 21,6"></polyline>
                            <path d="M19,6v14a2,2 0 0,1 -2,2H7a2,2 0 0,1 -2,-2V6m3,0V4a2,2 0 0,1 2,-2h4a2,2 0 0,1 2,2v2"></path>
                        </svg>
                    </button>
                </div>
            </div>
        </li>
    `).join('');
    
    // Reattach event listeners for checkboxes
    attachCheckboxListeners();
}

/**
 * Gets filtered tasks based on current filter
 */
function getFilteredTasks() {
    let list = tasks;
    switch (currentFilter) {
        case 'completed':
            list = list.filter(task => task.completed);
            break;
        case 'pending':
            list = list.filter(task => !task.completed);
            break;
        default:
            break;
    }

    // Apply month/year filters if set
    if (selectedMonth || selectedYear) {
        list = list.filter(task => {
            if (!task.dueDate) return false;
            const [y, m] = task.dueDate.split('-');
            const monthOk = selectedMonth ? m === selectedMonth : true;
            const yearOk = selectedYear ? y === selectedYear : true;
            return monthOk && yearOk;
        });
    }
    return list;
}

/**
 * Attaches event listeners to checkboxes
 */
function attachCheckboxListeners() {
    const checkboxes = document.querySelectorAll('.task-checkbox');
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('click', function() {
            const taskItem = this.closest('.task-item');
            const taskId = taskItem.dataset.taskId;
            toggleTaskCompletion(taskId);
        });
    });
}

/**
 * Updates the statistics display
 */
function updateStats() {
    const totalTasks = tasks.length;
    const completedTasks = tasks.filter(task => task.completed).length;
    
    taskCount.textContent = `${totalTasks} task${totalTasks !== 1 ? 's' : ''}`;
    completedCount.textContent = `${completedTasks} completed`;
}

/**
 * Drag and Drop Implementation
 */

function handleDragStart(e) {
    draggedElement = e.target.closest('.task-item');
    if (draggedElement) {
        draggedElement.classList.add('dragging');
        e.dataTransfer.effectAllowed = 'move';
        e.dataTransfer.setData('text/html', draggedElement.outerHTML);
    }
}

function handleDragOver(e) {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
    
    const targetItem = e.target.closest('.task-item');
    if (targetItem && targetItem !== draggedElement) {
        targetItem.classList.add('drag-over');
    }
}

function handleDrop(e) {
    e.preventDefault();
    
    const targetItem = e.target.closest('.task-item');
    if (!targetItem || !draggedElement) return;
    
    // Remove drag-over styling
    document.querySelectorAll('.task-item').forEach(item => {
        item.classList.remove('drag-over');
    });
    
    // Reorder tasks
    const draggedId = draggedElement.dataset.taskId;
    const targetId = targetItem.dataset.taskId;
    
    if (draggedId !== targetId) {
        reorderTasks(draggedId, targetId);
    }
}

function handleDragEnd(e) {
    if (draggedElement) {
        draggedElement.classList.remove('dragging');
        draggedElement = null;
    }
    
    // Remove all drag-over styling
    document.querySelectorAll('.task-item').forEach(item => {
        item.classList.remove('drag-over');
    });
}

/**
 * Reorders tasks in the array and updates storage
 */
function reorderTasks(draggedId, targetId) {
    const draggedIndex = tasks.findIndex(t => t.id === draggedId);
    const targetIndex = tasks.findIndex(t => t.id === targetId);
    
    if (draggedIndex === -1 || targetIndex === -1) return;
    
    // Remove dragged task and insert at target position
    const [draggedTask] = tasks.splice(draggedIndex, 1);
    tasks.splice(targetIndex, 0, draggedTask);
    
    saveTasksToStorage();
    renderTasks();
}

/**
 * LocalStorage Operations
 */

function saveTasksToStorage() {
    try {
        localStorage.setItem('todoTasks', JSON.stringify(tasks));
    } catch (error) {
        console.error('Failed to save tasks to localStorage:', error);
    }
}

function loadTasksFromStorage() {
    try {
        const stored = localStorage.getItem('todoTasks');
        if (stored) {
            tasks = JSON.parse(stored).map(t => ({
                ...t,
                dueDate: t.dueDate || ''
            }));
        }
    } catch (error) {
        console.error('Failed to load tasks from localStorage:', error);
        tasks = [];
    }
}

/**
 * Utility Functions
 */

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function renderDueDate(dueDateStr) {
    if (!dueDateStr) return '';
    const statusClass = getDueStatusClass(dueDateStr);
    const formatted = formatDateHuman(dueDateStr);
    return `<span class="task-due ${statusClass}" title="Due ${formatted}">📅 ${formatted}</span>`;
}

function getDueStatusClass(dueDateStr) {
    try {
        const today = new Date();
        const due = new Date(dueDateStr + 'T00:00:00');
        // Normalize times for comparison
        today.setHours(0,0,0,0);
        if (due < today) return 'overdue';
        const diffDays = Math.round((due - today) / (1000*60*60*24));
        if (diffDays <= 3) return 'due-soon';
        return 'on-time';
    } catch(_) {
        return 'on-time';
    }
}

function formatDateHuman(isoDate) {
    try {
        const [y,m,d] = isoDate.split('-');
        const date = new Date(Number(y), Number(m)-1, Number(d));
        return date.toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' });
    } catch(_) {
        return isoDate;
    }
}

function refreshTimeFilters() {
    if (!filterMonthSelect || !filterYearSelect) return;

    // Preserve selections
    const prevMonth = selectedMonth || '';
    const prevYear = selectedYear || '';

    // Months
    const monthNames = ['All months','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
    filterMonthSelect.innerHTML = monthNames.map((label, idx) => {
        if (idx === 0) return `<option value="">${label}</option>`;
        const value = String(idx).padStart(2, '0');
        return `<option value="${value}">${label}</option>`;
    }).join('');

    // Years from tasks or current range
    const years = new Set();
    const currentYear = new Date().getFullYear();
    years.add(String(currentYear));
    years.add(String(currentYear + 1));
    tasks.forEach(t => {
        if (t.dueDate) years.add(t.dueDate.split('-')[0]);
    });
    const yearOptions = ['<option value="">All years</option>']
        .concat(Array.from(years).sort().map(y => `<option value="${y}">${y}</option>`));
    filterYearSelect.innerHTML = yearOptions.join('');

    // Restore selections
    filterMonthSelect.value = prevMonth;
    filterYearSelect.value = prevYear;
}

/**
 * Export functions for potential external use
 */
window.TodoApp = {
    addTask,
    deleteTask,
    editTask,
    toggleTaskCompletion,
    setFilter,
    getTasks: () => [...tasks]
};
