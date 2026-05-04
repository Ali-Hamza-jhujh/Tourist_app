# Tourist_app
# 🌍 Pakistan Tourism Web App

A full-stack Django web application for exploring tourist destinations across Pakistan — featuring city guides, hotel booking, a photo gallery, an AI chatbot, and more.

---

## ✨ Features

- 🏙️ **City Explorer** — Browse famous tourist cities of Pakistan with images and detail pages
- 🏛️ **Attraction Pages** — Dedicated pages per city (e.g. Bahawalpur) with tourist spots, descriptions, and fullscreen image modals
- 🖼️ **Photo Gallery** — Community-uploaded tourist spot photos grouped by city with fullscreen viewer
- 🏨 **Hotel Listings** — View available hotels per city with pricing and cart/booking system
- 🤖 **AI Chatbot** — Chat interface powered by a backend API for travel queries and city info
- 👥 **About Page** — Team profiles, mission, vision, and partnership info
- 📱 **Responsive Design** — Works across desktop and mobile screens

---

## 🗂️ Project Structure

```
├── templates/
│   ├── base.htm                  # Base layout template
│   ├── dashboard.html            # Home — city cards grid
│   ├── bahawalpur.html           # Bahawalpur attractions page
│   ├── gallery.html              # Community photo gallery
│   ├── hostel_list.html          # Hotel listings per city
│   ├── about.html                # About page with team info
│   └── chatbot.html              # AI chatbot interface
│
├── static/
│   └── images/                   # Static images (cities, attractions, team)
│
├── models.py                     # City, TouristSpot, Hotel models
├── views.py                      # Page views & chatbot API
├── urls.py                       # URL routing
└── manage.py
```

---

## 🖼️ Pages Overview

| Page | Description |
|---|---|
| **Dashboard** | Grid of Pakistani cities with clickable cards |
| **City Page** (e.g. Bahawalpur) | Tourist attractions with images & fullscreen modal |
| **Gallery** | Spots uploaded by users, grouped by city |
| **Hotel List** | Hotels for a selected city with booking form |
| **Chatbot** | AI-powered chat for travel help |
| **About** | Team, mission, vision & contact CTA |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Django 4.x
- pip

---

### 🔧 Installation

```bash
# Clone the repository
git clone https://github.com/your-username/pakistan-tourism-app.git
cd pakistan-tourism-app

# Create a virtual environment
python -m venv env
source env/bin/activate        # On Windows: env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

### ⚙️ Configuration

Create a `.env` file or update `settings.py` with:

```env
SECRET_KEY=your_django_secret_key
DEBUG=True
ALLOWED_HOSTS=*
DATABASE_URL=sqlite:///db.sqlite3
CHATBOT_API_KEY=your_ai_api_key
```

---

### 🗄️ Database Setup

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser   # to access admin panel
```

---

### ▶️ Run the App

```bash
python manage.py runserver
```

Visit: `http://127.0.0.1:8000`

---

## 🤖 Chatbot

The chatbot is powered by a `/chatbot-api/` POST endpoint. It accepts a JSON body:

```json
{ "message": "Tell me about Derawar Fort" }
```

And returns:

```json
{ "reply": "Derawar Fort is a majestic desert fort in the Cholistan Desert..." }
```

You can connect it to any AI backend (OpenAI, Gemini, custom NLP model, etc.) in your `views.py`.

---

## 📦 Key Django Models

```python
# City model
class City(models.Model):
    city = models.CharField(max_length=100)
    image = models.ImageField(upload_to='cities/')

# Tourist Spot model
class TouristSpot(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='spots/')
    yourname = models.CharField(max_length=100, blank=True)
    extra_details = models.TextField(blank=True)

# Hotel model
class Hotel(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='hotels/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django (Python) |
| Frontend | HTML, CSS, Bootstrap, Vanilla JS |
| Database | SQLite / PostgreSQL |
| AI Chatbot | Custom API endpoint (pluggable) |
| Templating | Django Templates |
| Media | Django Static & Media Files |

---

## 🏙️ Tourist Cities Covered

- **Bahawalpur** — Noor Mahal, Derawar Fort, Cholistan Desert, Lal Suhanra, Abbasi Mosque, and more
- More cities dynamically loaded from the database via the admin panel

---

## 👥 Team

| Name | Role |
|---|---|
| **Ali Hamza** | Founder & Full Stack Developer |
| **Ali Zain** | Tour Guide Expert |

---

## 📸 Screenshots

> Add screenshots of your dashboard, city page, gallery, and chatbot here.

---

## 🤝 Contributing

Contributions, local tour guide partnerships, and new city data are welcome!

1. Fork the repo
2. Create a feature branch: `git checkout -b feature/add-lahore-page`
3. Commit your changes: `git commit -m "Add Lahore attractions page"`
4. Push and open a Pull Request

---

## 📄 License

This project is open source. See [LICENSE](LICENSE) for details.

---

> Built with ❤️ to showcase the beauty of Pakistan 🇵🇰
