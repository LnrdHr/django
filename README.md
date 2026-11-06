# Django Polls App with AI Chatbot

A modern Django polling application featuring an interactive AI chatbot powered by LangGraph, OpenAI GPT-4, Tavily search integration, and Langfuse observability. The app combines traditional polling functionality with intelligent conversational AI assistance.

<video src="https://github.com/user-attachments/assets/fd5da4b3-619d-41d8-a44e-f0b3bbc6475c"
       autoplay loop muted playsinline
       style="max-width:100%;"
       onloadedmetadata="this.playbackRate=2.0;">
</video>



## Main Features

### Polling System
- **Question Management**: Create and manage poll questions with multiple choices
- **Voting System**: Users can vote on questions with real-time result tracking
- **Results Visualization**: View detailed voting results with statistics
- **Question Detail Views**: Detailed question pages with voting forms
- **Admin Interface**: Django admin panel for managing questions and choices

### AI Chatbot Integration
- **LangGraph-Powered AI**: Advanced conversational AI using LangGraph state graphs
- **OpenAI GPT-4 Integration**: Powered by OpenAI's GPT-4-mini model
- **Web Search Capabilities**: Real-time web search using Tavily Search API
- **Memory Persistence**: Conversation history maintained across sessions
- **Interactive Chat UI**: Real-time AJAX-powered chat interface with loading states
- **Langfuse Observability**: Advanced monitoring, tracing, and analytics for AI interactions

### Modern UI/UX
- **Tailwind CSS + DaisyUI**: Modern, responsive design framework
- **Dark Theme**: Beautiful gradient backgrounds with glass-morphism effects
- **Interactive Elements**: Hover effects, smooth transitions, and animations
- **Mobile Responsive**: Optimized for all device sizes
- **Loading States**: Visual feedback for all user interactions

### Technical Features
- **RESTful API**: JSON API endpoints for frontend integration
- **AJAX Integration**: Seamless frontend-backend communication
- **Database Management**: SQLite database with Django ORM
- **Environment Configuration**: Secure API key management with `.env` files
- **Signal-based Initialization**: Automatic chatbot setup on server start
- **AI Observability**: Comprehensive tracking of AI model performance and usage

## Project Structure

```
django/
├── src/
│   ├── manage.py                 # Django management script
│   ├── db.sqlite3               # SQLite database
│   ├── .env                     # Environment variables (API keys)
│   ├── mysite/                  # Django project settings
│   │   ├── settings.py          # Main configuration
│   │   ├── urls.py             # URL routing
│   │   └── wsgi.py             # WSGI application
│   └── polls/                   # Main application
│       ├── models.py           # Database models (Question, Choice)
│       ├── views.py            # View controllers and API endpoints
│       ├── urls.py             # App URL patterns
│       ├── admin.py            # Admin interface configuration
│       ├── chatbot.py          # LangGraph AI chatbot implementation
│       ├── signals.py          # Django signals for initialization
│       ├── templates/          # HTML templates
│       │   └── polls/
│       │       ├── index.html  # Main page with chat interface
│       │       ├── detail.html # Question detail page
│       │       └── results.html # Results page
│       └── static/             # Static files (CSS)
├── package.json                # Node.js dependencies (Tailwind CSS)
├── .venv/                     # Python virtual environment
└── README.md                  # This file
```

## Quick Start Guide

### Prerequisites

Before running this application, ensure you have:

- **Python 3.8+** installed
- **Node.js 16+** installed (for Tailwind CSS)
- **Git** installed
- **OpenAI API Key** (for chatbot functionality)
- **Tavily API Key** (for web search capabilities)
- **Langfuse Account** (for AI observability and monitoring)

### API Keys Required

1. **OpenAI API Key**: Get from [OpenAI Platform](https://platform.openai.com)
2. **Tavily API Key**: Get from [Tavily](https://tavily.com)
3. **Langfuse Keys**: Get from [Langfuse Cloud](https://cloud.langfuse.com)

### Installation & Setup

#### 1. **Clone the Repository**
```bash
git clone <repository-url>
cd django
```

#### 2. **Set Up Python Virtual Environment**
```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate
```

#### 3. **Install Python Dependencies**
```bash
pip install django python-dotenv langchain langchain-openai langgraph langchain-tavily-search langfuse
```

#### 4. **Install Node.js Dependencies (for Tailwind CSS)**
```bash
npm install
```

#### 5. **Environment Configuration**
Create a `.env` file in the `src/` directory:

```bash
cd src
touch .env
```

Add your API keys to `.env`:
```env
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
LANGFUSE_SECRET_KEY=your_langfuse_secret_key_here
LANGFUSE_PUBLIC_KEY=your_langfuse_public_key_here
LANGFUSE_HOST=https://cloud.langfuse.com
```

**Important**: Never commit your `.env` file to version control!

#### 6. **Database Setup**
```bash
cd src

# Create database migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser account (optional)
python manage.py createsuperuser
```

#### 7. **Build Tailwind CSS** (Optional)
If you make CSS changes:
```bash
# From the root directory
npx tailwindcss -i ./src/polls/static/polls/input.css -o ./src/polls/static/polls/output.css --watch
```

### Running the Application

#### **Start the Development Server**
```bash
cd src
python manage.py runserver
```

#### **Access the Application**
- **Main Application**: http://127.0.0.1:8000/polls/
- **Admin Interface**: http://127.0.0.1:8000/admin/ (if superuser created)
- **Langfuse Dashboard**: https://cloud.langfuse.com (for AI monitoring)

### Using the Application

#### **Polling Features**
1. **View Questions**: Browse available poll questions on the main page
2. **Vote on Questions**: Click any question to open the voting form
3. **View Results**: After voting, see detailed results with statistics
4. **Admin Management**: Use Django admin to create/manage questions

#### **AI Chatbot Features**
1. **Ask Questions**: Type any question in the chat interface
2. **Get AI Responses**: Powered by GPT-4 with web search capabilities
3. **Real-time Interaction**: AJAX-powered chat with loading indicators
4. **Persistent Memory**: Conversation context maintained across messages
5. **Performance Monitoring**: Track AI interactions via Langfuse dashboard

## API Endpoints

### **Polling API**
- `GET /polls/api/questions/` - List all questions
- `GET /polls/api/questions/{id}/` - Get question details with choices
- `POST /polls/api/questions/{id}/vote/` - Submit a vote

### **Chatbot API**
- `POST /polls/api/chatbot/` - Send message to AI chatbot

### **Example API Usage**
```javascript
// Send message to chatbot
const response = await fetch('/polls/api/chatbot/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
    },
    body: JSON.stringify({ message: "Hello, can you help me?" })
});

const data = await response.json();
console.log(data.response); // AI response
```

## Development

### **Adding New Questions**
1. Use Django admin interface at `/admin/`
2. Or create via Django shell:
```bash
python manage.py shell
```

```python
from polls.models import Question, Choice
from django.utils import timezone

# Create question
q = Question(question_text="What's your favorite color?", pub_date=timezone.now())
q.save()

# Add choices
q.choice_set.create(choice_text="Red", correct=False)
q.choice_set.create(choice_text="Blue", correct=True)
q.choice_set.create(choice_text="Green", correct=False)
```

### **Customizing the Chatbot**
Edit `polls/chatbot.py` to modify:
- **AI Model**: Change from GPT-4-mini to other models
- **Tools**: Add or remove search capabilities
- **Memory**: Adjust conversation memory settings
- **Prompts**: Customize system prompts
- **Langfuse Integration**: Modify observability settings

### **Langfuse Observability Features**
- **Conversation Tracking**: Monitor all chatbot interactions
- **Performance Metrics**: Track response times and token usage
- **Error Monitoring**: Identify and debug AI model issues
- **Usage Analytics**: Analyze user interaction patterns
- **Cost Tracking**: Monitor OpenAI API usage and costs

### **Styling Changes**
- **Tailwind CSS**: Modify classes in templates
- **Custom CSS**: Edit `polls/static/polls/style.css`
- **DaisyUI**: Use DaisyUI components for consistent design

## Troubleshooting

### **Common Issues**

#### **"ModuleNotFoundError" for AI packages**
```bash
pip install langchain langchain-openai langgraph langchain-tavily-search langfuse
```

#### **Chatbot not responding**
1. Check `.env` file contains valid API keys (OpenAI, Tavily, Langfuse)
2. Verify internet connection for API calls
3. Check Django logs for error messages
4. Verify Langfuse configuration in dashboard

#### **Langfuse connection issues**
1. Verify `LANGFUSE_HOST` is set to `https://cloud.langfuse.com`
2. Check that `LANGFUSE_PUBLIC_KEY` and `LANGFUSE_SECRET_KEY` are correct
3. Ensure Langfuse project is properly configured

#### **CSS not loading**
1. Run `python manage.py collectstatic`
2. Ensure Tailwind CSS is built: `npx tailwindcss build`

#### **Database errors**
```bash
python manage.py makemigrations
python manage.py migrate
```

### **Getting Help**
- Check Django logs in the terminal
- Use browser developer tools (F12) to check for JavaScript errors
- Verify API responses in Network tab
- Monitor AI interactions in Langfuse dashboard

## License

This project is open source and available under the [MIT License](LICENSE).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- **Django** - Web framework
- **OpenAI** - AI model provider
- **LangGraph** - AI workflow framework
- **Langfuse** - AI observability and monitoring platform
- **Tailwind CSS + DaisyUI** - UI framework
- **Tavily** - Web search API

---

**Happy Polling!**
