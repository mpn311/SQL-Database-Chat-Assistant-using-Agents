# 🤖 SQL Database Chat Assistant

A professional Streamlit application that enables natural language interaction with SQL databases using LangChain and LLMs.

## ✨ Features

- 💬 **Natural Language Queries**: Ask questions in plain English
- 🗄️ **Multi-Database Support**: Works with SQLite and MySQL
- 🤖 **AI-Powered**: Leverages Groq's powerful LLMs
- 🔒 **Secure**: Safe database connections with read-only SQLite mode
- 📊 **Real-time Responses**: Instant answers with streaming support
- 🎨 **Modern UI**: Clean, professional interface with custom styling
- 📈 **Database Insights**: View schemas and table information

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Groq API key ([Get one here](https://console.groq.com))
- MySQL database (optional, for MySQL support)

### Installation

1. **Clone or download the project files**

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up the SQLite database** (Optional - for demo)
```bash
python sqlite.py
```

This creates a `student.db` file with sample data.

### Running the Application

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

## 📖 Usage

### Using SQLite Database

1. Select "🗄️ Use SQLite Database (student.db)" in the sidebar
2. Enter your Groq API key
3. Click outside the input field to connect
4. Start asking questions!

**Example Questions:**
- "Show me all students"
- "What's the average marks in Data Science class?"
- "List students with marks above 85"
- "How many students are in section A?"
- "Who has the highest marks?"

### Using MySQL Database

1. Select "🔗 Connect to MySQL Database" in the sidebar
2. Enter your MySQL credentials:
   - Host (e.g., localhost or IP address)
   - Username
   - Password
   - Database name
3. Enter your Groq API key
4. The app will automatically connect
5. Start querying your database!

## 🎯 Configuration Options

### Model Selection

Choose from multiple Groq models:
- **llama-3.1-70b-versatile** (Recommended) - Best for complex queries
- **llama-3.1-8b-instant** - Faster responses
- **mixtral-8x7b-32768** - Large context window
- **gemma2-9b-it** - Efficient alternative

### Advanced Settings

- **Verbose Mode**: Enable to see detailed agent reasoning
- **Max Iterations**: Control the maximum number of steps the agent can take

## 🗂️ Project Structure

```
.
├── app.py              # Main Streamlit application
├── sqlite.py           # SQLite database setup script
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── student.db         # SQLite database (created after running sqlite.py)
```

## 📊 Sample Database Schema

The included SQLite database contains a `STUDENT` table:

| Column  | Type         | Description           |
|---------|-------------|-----------------------|
| ID      | INTEGER     | Primary key (auto)    |
| NAME    | VARCHAR(25) | Student name          |
| CLASS   | VARCHAR(25) | Course/class name     |
| SECTION | VARCHAR(25) | Section identifier    |
| MARKS   | INTEGER     | Marks (0-100)         |

