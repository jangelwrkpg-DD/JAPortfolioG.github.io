import re
import os

featured = [
    "Logos/Ink Studio_Brand.jpg",
    "Fotos/Italianini.jpg",
    "Caratulas/ENERGY FLOW.jpg",
    "Publicidad/Publicidad_Cartelon_70x100.png",
    "Fotos/Sunshine.jpg",
    "Caratulas/Starlight-Portada.png"
]

folders = {
    "branding": "Logos",
    "photography": "Fotos",
    "covers": "Caratulas",
    "advertising": "Publicidad"
}

index_path = 'index.html'

grid_html = ""

for category, f_dir in folders.items():
    if not os.path.exists(f_dir): continue
    files = sorted([f for f in os.listdir(f_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
    for f in files:
        rel_path = f"{f_dir}/{f}"
        is_featured = "true" if rel_path.replace("\\", "/") in featured else "false"
        title = f.rsplit('.', 1)[0].replace('_', ' ').replace('-', ' ')
        
        card = f'''
                <!-- Project Card: {category} -->
                <article class="project-card" data-category="{category}" data-featured="{is_featured}">
                    <div class="card-image-wrap">
                        <img src="{rel_path}" class="card-img" alt="{title}" />
                        <div class="card-overlay">
                            <span>Ver Detalles</span>
                        </div>
                    </div>
                    <div class="card-info">
                        <span class="project-category">{category}</span>
                        <h3>{title}</h3>
                    </div>
                </article>'''
        grid_html += card

with open(index_path, 'r', encoding='utf-8') as file:
    content = file.read()

# Make the logo clickable & redirect to home
if 'Mi logo v3.png' in content:
    content = content.replace('<img src="Mi logo v3.png" alt="José Ángel Logo" />', '<a href="#home"><img src="Mi logo V1.png" alt="José Ángel Logo - Home" /></a>')

# Change "All" to "Featured"
if 'data-filter="all">All</button>' in content:
    content = content.replace('data-filter="all">All</button>', 'data-filter="featured">Featured</button>')

# Fix the resume button
resume_pattern = r'<a href="assets/resume\.pdf"[^>]*>Download Resume <i[^>]*></i></a>'
if re.search(resume_pattern, content):
    content = re.sub(resume_pattern, r'<a href="#" onclick="alert(\'Currículum (Resume) no disponible temporalmente. Por favor contáctame.\'); return false;" class="btn btn-outline">Download Resume <i class="fas fa-arrow-down"></i></a>', content)

# Replace the portfolio grid block entirely
grid_pattern = r'<div class="portfolio-grid">.*?</section>'
if re.search(grid_pattern, content, flags=re.DOTALL):
    content = re.sub(
        grid_pattern,
        f'<div class="portfolio-grid">{grid_html}\n            </div>\n        </section>',
        content,
        flags=re.DOTALL
    )

with open(index_path, 'w', encoding='utf-8') as file:
    file.write(content)

print("index.html successfully updated!")
