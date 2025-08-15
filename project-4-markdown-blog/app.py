from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
import markdown
import re

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Register markdown filter for Jinja2
@app.template_filter('markdown')
def markdown_filter(text):
    return markdown.markdown(text)

def sanitize_filename(title):
    """Convert title to a safe filename"""
    # Remove special characters and replace spaces with hyphens
    safe_name = re.sub(r'[^\w\s-]', '', title)
    safe_name = re.sub(r'[-\s]+', '-', safe_name)
    safe_name = safe_name.strip('-').lower()
    return safe_name + '.md'

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Like model for tracking post likes
class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_filename = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    # Ensure one user can like a post only once
    __table_args__ = (db.UniqueConstraint('user_id', 'post_filename', name='unique_user_post_like'),)
    
    user = db.relationship('User', backref='likes')

# Posts directory
POSTS_DIR = 'posts'

def get_posts():
    """Get all posts"""
    posts = []
    try:
        if not os.path.exists(POSTS_DIR):
            print(f"Posts directory {POSTS_DIR} does not exist")
            return posts
        
        for filename in os.listdir(POSTS_DIR):
            if filename.endswith('.md'):
                post = get_post(filename)
                if post:
                    try:
                        # Add like count and user like status
                        post['like_count'] = Like.query.filter_by(post_filename=filename).count()
                        if session.get('user_id'):
                            post['user_liked'] = Like.query.filter_by(
                                user_id=session['user_id'], 
                                post_filename=filename
                            ).first() is not None
                        else:
                            post['user_liked'] = False
                        posts.append(post)
                    except Exception as e:
                        print(f"Error processing likes for {filename}: {e}")
                        # Still add the post without like info
                        post['like_count'] = 0
                        post['user_liked'] = False
                        posts.append(post)
        
        # Sort posts by creation time (newest first)
        posts.sort(key=lambda x: os.path.getctime(os.path.join(POSTS_DIR, x['filename'])), reverse=True)
        return posts
    except Exception as e:
        print(f"Error reading posts: {e}")
        return posts

def get_post(filename):
    """Get a single post by filename"""
    try:
        filepath = os.path.join(POSTS_DIR, filename)
        if not os.path.exists(filepath):
            print(f"Post file {filepath} does not exist")
            return None
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract author from first line if it starts with "Author: "
        lines = content.split('\n')
        author = None
        if lines and lines[0].startswith('Author: '):
            author = lines[0].replace('Author: ', '').strip()
            # Remove author line and get the rest of the content
            content = '\n'.join(lines[1:]).strip()
        
        # Extract title from first non-empty line (after author)
        title = None
        for line in lines[1:]:
            if line.strip():
                if line.strip().startswith('# '):
                    title = line.strip().replace('# ', '')
                else:
                    title = line.strip()
                break
        
        if not title:
            title = filename.replace('.md', '').replace('-', ' ').title()
        
        # Add like count and user like status
        try:
            like_count = Like.query.filter_by(post_filename=filename).count()
            user_liked = False
            if session.get('user_id'):
                user_liked = Like.query.filter_by(
                    user_id=session['user_id'], 
                    post_filename=filename
                ).first() is not None
        except Exception as e:
            print(f"Error getting like info for {filename}: {e}")
            like_count = 0
            user_liked = False
        
        return {
            'filename': filename,
            'title': title,
            'content': content,
            'author': author,
            'like_count': like_count,
            'user_liked': user_liked,
            'author_username': author  # Add this for easier access
        }
    except Exception as e:
        print(f"Error reading post {filename}: {e}")
        return None

def is_admin():
    """Check if current user is admin"""
    if session.get('user_id'):
        user = User.query.get(session['user_id'])
        return user and user.is_admin
    return False

@app.route('/')
def index():
    """Homepage - displays all posts with previews"""
    posts = get_posts()
    return render_template('index.html', posts=posts)

@app.route('/post/<filename>')
def post(filename):
    """Display individual post"""
    post_data = get_post(filename)
    if post_data:
        # Convert Markdown to HTML
        html_content = markdown.markdown(post_data['content'])
        return render_template('post.html', post=post_data, html_content=html_content)
    else:
        flash('Post not found', 'error')
        return redirect(url_for('index'))

@app.route('/create', methods=['GET', 'POST'])
def create_post():
    """Create new blog post"""
    if not session.get('user_id'):
        flash('Please log in to create posts', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        
        if not title or not content:
            flash('Title and content are required', 'error')
            return render_template('create.html')
        
        # Create filename from title
        filename = sanitize_filename(title)
        
        # Get current user
        user = User.query.get(session['user_id'])
        username = user.username if user else 'Unknown'
        
        # Add author information at the top of the content
        full_content = f"Author: {username}\n\n# {title}\n\n{content}"
        
        # Save post to file
        post_path = os.path.join(POSTS_DIR, filename)
        try:
            with open(post_path, 'w', encoding='utf-8') as f:
                f.write(full_content)
            flash('Post created successfully!', 'success')
            return redirect(url_for('post', filename=filename))
        except Exception as e:
            flash(f'Error creating post: {str(e)}', 'error')
    
    return render_template('create.html')

@app.route('/edit/<filename>', methods=['GET', 'POST'])
def edit_post(filename):
    """Edit existing blog post - admin only"""
    if not is_admin():
        flash('Only administrators can edit posts', 'error')
        return redirect(url_for('index'))
    
    post = get_post(filename)
    if not post:
        flash('Post not found', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        
        if not title or not content:
            flash('Title and content are required', 'error')
            return render_template('edit.html', post=post)
        
        # Preserve the original author
        author = post.get('author', 'Unknown')
        
        # Create new filename if title changed
        new_filename = sanitize_filename(title)
        
        # Add author information at the top of the content
        full_content = f"Author: {author}\n\n# {title}\n\n{content}"
        
        try:
            # If filename changed, delete old file and create new one
            if new_filename != filename:
                old_path = os.path.join(POSTS_DIR, filename)
                new_path = os.path.join(POSTS_DIR, new_filename)
                
                # Delete old file
                if os.path.exists(old_path):
                    os.remove(old_path)
                
                # Create new file
                with open(new_path, 'w', encoding='utf-8') as f:
                    f.write(full_content)
                
                flash('Post updated successfully!', 'success')
                return redirect(url_for('post', filename=new_filename))
            else:
                # Update existing file
                filepath = os.path.join(POSTS_DIR, filename)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(full_content)
                
                flash('Post updated successfully!', 'success')
                return redirect(url_for('post', filename=filename))
                
        except Exception as e:
            flash(f'Error updating post: {str(e)}', 'error')
    
    return render_template('edit.html', post=post)

@app.route('/delete/<filename>', methods=['POST'])
def delete_post(filename):
    """Delete a blog post - admin or post author only"""
    if not session.get('user_id'):
        flash('Please log in to delete posts', 'error')
        return redirect(url_for('index'))
    
    # Get the post to check ownership
    post = get_post(filename)
    if not post:
        flash('Post not found', 'error')
        return redirect(url_for('index'))
    
    # Check if user is admin or the post author
    user = User.query.get(session['user_id'])
    is_author = post.get('author_username') == user.username
    
    if not user.is_admin and not is_author:
        flash('You can only delete your own posts or need admin privileges', 'error')
        return redirect(url_for('index'))
    
    filepath = os.path.join(POSTS_DIR, filename)
    if os.path.exists(filepath):
        os.remove(filepath)
        
        # Delete associated likes
        likes = Like.query.filter_by(post_filename=filename).all()
        for like in likes:
            db.session.delete(like)
        db.session.commit()
        
        if user.is_admin:
            flash('Post deleted successfully by admin!', 'success')
        else:
            flash('Your post has been deleted successfully!', 'success')
    else:
        flash('Post not found', 'error')
    
    return redirect(url_for('index'))

@app.route('/search')
def search():
    """Search posts by title"""
    query = request.args.get('q', '').strip()
    posts = []
    
    if query:
        all_posts = get_posts()
        for post in all_posts:
            if query.lower() in post['title'].lower():
                posts.append(post)
    else:
        posts = get_posts()
    
    return render_template('search.html', posts=posts, query=query)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if session.get('user_id'):
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()
        
        # Validation
        if not username or not email or not password:
            flash('All fields are required', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long', 'error')
            return render_template('register.html')
        
        # Check if username or email already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists', 'error')
            return render_template('register.html')
        
        # Create new user
        user = User(username=username, email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if session.get('user_id'):
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        if not username or not password:
            flash('Username and password are required', 'error')
            return render_template('login.html')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['is_admin'] = user.is_admin
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('index'))

@app.route('/profile')
def profile():
    """User profile page"""
    if not session.get('user_id'):
        flash('Please log in to view your profile', 'error')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    return render_template('profile.html', user=user)

@app.route('/change-password', methods=['GET', 'POST'])
def change_password():
    """Change user password"""
    if not session.get('user_id'):
        flash('Please log in to change your password', 'error')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    
    if request.method == 'POST':
        current_password = request.form.get('current_password', '').strip()
        new_password = request.form.get('new_password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()
        
        if not current_password or not new_password or not confirm_password:
            flash('All fields are required', 'error')
            return render_template('change_password.html')
        
        if not user.check_password(current_password):
            flash('Current password is incorrect', 'error')
            return render_template('change_password.html')
        
        if new_password != confirm_password:
            flash('New passwords do not match', 'error')
            return render_template('change_password.html')
        
        if len(new_password) < 6:
            flash('New password must be at least 6 characters long', 'error')
            return render_template('change_password.html')
        
        # Update password
        user.set_password(new_password)
        db.session.commit()
        
        flash('Password changed successfully!', 'success')
        return redirect(url_for('profile'))
    
    return render_template('change_password.html')

@app.route('/admin/users')
def admin_users():
    """Admin panel - view all users"""
    if not is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('index'))
    
    users = User.query.all()
    return render_template('admin_users.html', users=users)

@app.route('/admin/user/<int:user_id>/toggle-admin', methods=['POST'])
def toggle_admin_status(user_id):
    """Toggle admin status for a user"""
    if not is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('index'))
    
    user = User.query.get_or_404(user_id)
    
    # Prevent admin from removing their own admin status
    if user.id == session['user_id']:
        flash('You cannot modify your own admin status', 'error')
        return redirect(url_for('admin_users'))
    
    user.is_admin = not user.is_admin
    db.session.commit()
    
    status = 'granted' if user.is_admin else 'revoked'
    flash(f'Admin privileges {status} for user {user.username}', 'success')
    return redirect(url_for('admin_users'))

@app.route('/admin/user/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Delete a user (admin only)"""
    if not is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('index'))
    
    user = User.query.get_or_404(user_id)
    
    # Prevent admin from deleting themselves
    if user.id == session['user_id']:
        flash('You cannot delete your own account', 'error')
        return redirect(url_for('admin_users'))
    
    username = user.username
    db.session.delete(user)
    db.session.commit()
    
    flash(f'User {username} has been deleted', 'success')
    return redirect(url_for('admin_users'))

@app.route('/like/<filename>', methods=['POST'])
def like_post(filename):
    """Like a post"""
    if not session.get('user_id'):
        return jsonify({'error': 'Please log in to like posts'}), 401
    
    # Validate filename
    if not filename or not filename.endswith('.md'):
        return jsonify({'error': 'Invalid post filename'}), 400
    
    try:
        # Check if post exists
        post = get_post(filename)
        if not post:
            return jsonify({'error': 'Post not found'}), 404
        
        # Check if user already liked this post
        existing_like = Like.query.filter_by(
            user_id=session['user_id'], 
            post_filename=filename
        ).first()
        
        if existing_like:
            # Unlike the post
            db.session.delete(existing_like)
            db.session.commit()
            return jsonify({'liked': False, 'message': 'Post unliked'})
        else:
            # Like the post
            new_like = Like(
                user_id=session['user_id'],
                post_filename=filename
            )
            db.session.add(new_like)
            db.session.commit()
            return jsonify({'liked': True, 'message': 'Post liked'})
            
    except Exception as e:
        db.session.rollback()
        print(f"Like error for {filename}: {str(e)}")  # Debug print
        
        # Check if it's a database schema issue
        if "no such table" in str(e).lower():
            return jsonify({'error': 'Database schema issue. Please contact administrator.'}), 500
        elif "foreign key constraint" in str(e).lower():
            return jsonify({'error': 'User or post not found in database.'}), 500
        else:
            return jsonify({'error': f'Database error: {str(e)}'}), 500

@app.route('/post/<filename>/likes')
def get_post_likes(filename):
    """Get like count for a post"""
    try:
        like_count = Like.query.filter_by(post_filename=filename).count()
        return jsonify({'likes': like_count})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/debug/db')
def debug_db():
    """Debug database status"""
    if not session.get('user_id') or not session.get('is_admin'):
        return jsonify({'error': 'Admin access required'}), 403
    
    try:
        # Check if tables exist
        tables = []
        for table in db.metadata.tables.keys():
            tables.append(table)
        
        # Check Like table specifically
        like_count = 0
        try:
            like_count = Like.query.count()
        except Exception as e:
            like_count = f"Error: {str(e)}"
        
        # Check User table
        user_count = 0
        try:
            user_count = User.query.count()
        except Exception as e:
            user_count = f"Error: {str(e)}"
        
        return jsonify({
            'tables': tables,
            'like_count': like_count,
            'user_count': user_count,
            'session_user_id': session.get('user_id'),
            'session_username': session.get('username')
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def init_db():
    """Initialize database and create admin user"""
    with app.app_context():
        try:
            # Check if tables exist
            inspector = db.inspect(db.engine)
            existing_tables = inspector.get_table_names()
            
            if not existing_tables:
                # Only create tables if they don't exist
                db.create_all()
                print("Tables created: User, Like")
            else:
                print(f"Tables already exist: {existing_tables}")
            
            # Create admin user if it doesn't exist
            admin = User.query.filter_by(username='admin').first()
            if not admin:
                admin = User(
                    username='admin',
                    email='admin@example.com',
                    is_admin=True
                )
                admin.set_password('admin123')
                db.session.add(admin)
                db.session.commit()
                print("Admin user created: username=admin, password=admin123")
            else:
                print("Admin user already exists")
            
            print("Database initialized successfully!")
            
        except Exception as e:
            print(f"Database initialization error: {e}")
            # If there's an error, try to recreate tables
            try:
                db.drop_all()
                db.create_all()
                print("Tables recreated due to error")
                
                # Create admin user
                admin = User(
                    username='admin',
                    email='admin@example.com',
                    is_admin=True
                )
                admin.set_password('admin123')
                db.session.add(admin)
                db.session.commit()
                print("Admin user created: username=admin, password=admin123")
                
            except Exception as e2:
                print(f"Failed to recreate tables: {e2}")
                raise

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
