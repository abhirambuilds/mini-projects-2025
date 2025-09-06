# K Abhiram Reddy — Personal Portfolio

A simple, responsive personal portfolio website built with HTML, CSS and JavaScript.  
It showcases my profile as a B.Tech CSE student at SRM KTR (2024–2028), projects, skills and contact info — aimed at internship applications and recruiter review.

---

## Quick overview
- **What:** Static portfolio site (single-page) with Home, About, Skills, Projects and Contact sections.  
- **Goal:** Present projects clearly, make resume easy to download, and provide contact links for recruiters.

---

## Features
- Hero section with a short tagline and action buttons (Download Resume, View Projects).
- About section with a short bio and highlights.
- Skills section (technical + soft skills).
- Projects grid with links to GitHub repos and screenshots.
- Contact form (client-side validation) and social links.
- Mobile-first responsive layout and subtle animations.

---

## Technologies
- **HTML5** — Semantic structure  
- **CSS3** — Responsive layout, transitions, grid/flexbox  
- **JavaScript (ES6+)** — Interactivity and form handling  
- **Google Fonts** — *Poppins*  
- **Font Awesome** — Icons

---

## Project structure
project-2-portfolio-website/
├── index.html # Main page
├── styles.css # Styles and animations
├── script.js # Interactive behavior
├── assets/
│ ├── avatar.png
│ ├── project1.png
│ └── Resume_Abhiram_Reddy.pdf
└── README.md


---

## Getting started (local)
1. Clone the repo:
   ```bash
   git clone https://github.com/abhirambuilds/mini-projects-2025.git


Open the project folder and double-click index.html to view in browser, or serve locally:

# optional: simple local server (Python 3)
python -m http.server 8000
# then open http://localhost:8000

How to update content

Edit index.html to change name, tagline, bio, and project cards.

Replace assets/avatar.png or assets/Resume_Abhiram_Reddy.pdf with your latest files.

Update project links and screenshots in the Projects section (in index.html).

Modify styles in styles.css (colors, fonts, spacing).

Make the "Download Resume" button work

Place your resume PDF at assets/Resume_Abhiram_Reddy.pdf, then use this anchor in index.html:

<a href="assets/Resume_Abhiram_Reddy.pdf"
   download="Kolakalapudi_Abhiram_Reddy_Resume.pdf"
   title="Download resume (PDF)">
  Download Resume
</a>


This forces the browser to download the PDF. Keep the file name exactly as above or update the href to match your file name.

Deployment

GitHub Pages: Push the repo and enable Pages in repo settings (branch: main, folder: /root).

Netlify / Vercel: Connect your repo and deploy as a static site (automatic builds).

No build step required — this is a static site.

Tips for a stronger portfolio

Pin 3–4 best projects on GitHub and link to them from the Projects section.

Add 1–2 screenshots or a short GIF per project (show the app or key plot).

Keep the resume PDF up to date and ensure the Download link works in an incognito window.

Keep commit messages clear when you update projects.

License

MIT — feel free to reuse and adapt the code.

Contact

Kolakalapudi Abhiram Reddy
Email: k.abhiram9999@gmail.com

GitHub: https://github.com/abhirambuilds