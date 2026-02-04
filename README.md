# 🤖 SQL Database Chat Assistant

A professional Streamlit application that enables natural language interaction with SQL databases using LangChain and Groq LLMs.

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

## 🔧 Customization

### Adding Your Own Database

**For SQLite:**
1. Place your `.db` file in the project directory
2. Update the database path in `app.py` (line ~150)

**For MySQL:**
Simply use the connection form in the sidebar

### Modifying the UI

The application uses custom CSS in `app.py` (lines ~35-60). Modify the styles to match your branding.

## 🛡️ Security Best Practices

1. **Never commit API keys** to version control
2. **Use environment variables** for sensitive data:
   ```python
   import os
   api_key = os.getenv("GROQ_API_KEY")
   ```
3. **SQLite read-only mode**: The app uses read-only mode by default for SQLite
4. **Validate inputs**: All user inputs are validated before processing

## 🐛 Troubleshooting

### Common Issues

**"Database file not found"**
- Run `python sqlite.py` to create the database
- Ensure `student.db` is in the same directory as `app.py`

**"Failed to initialize LLM"**
- Check your Groq API key is correct
- Ensure you have internet connectivity
- Verify your API key has sufficient credits

**"MySQL connection failed"**
- Verify MySQL server is running
- Check credentials are correct
- Ensure the database exists
- Check firewall settings allow connections

**"Import errors"**
- Run `pip install -r requirements.txt` again
- Ensure you're using Python 3.8+

## 📝 Example Queries

Here are some example natural language queries you can try:

### Basic Queries
- "How many students are there?"
- "Show me all students in Data Science class"
- "List students in section B"

### Aggregate Queries
- "What's the average marks?"
- "Calculate the average marks by class"
- "Show the total number of students per section"

### Filtering & Sorting
- "Find students with marks greater than 90"
- "Show top 5 students by marks"
- "List all students who failed (marks < 40)"

### Complex Queries
- "Which class has the highest average marks?"
- "Show students who scored above the class average"
- "Compare average marks between sections"

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## 📄 License

This project is provided as-is for educational and commercial use.

## 🙏 Acknowledgments

- **Streamlit** - For the amazing web framework
- **LangChain** - For the agent framework
- **Groq** - For fast LLM inference
- **SQLAlchemy** - For database abstraction

## 📧 Support

For issues and questions:
1. Check the troubleshooting section
2. Review existing GitHub issues
3. Create a new issue with detailed information

## 🔄 Updates

**Version 2.0** (Current)
- ✅ Professional UI with custom styling
- ✅ Enhanced error handling
- ✅ Database schema viewer
- ✅ Multiple model support
- ✅ Advanced configuration options
- ✅ Comprehensive logging
- ✅ Improved security

---

**Made with ❤️ using Streamlit, LangChain, and Groq**
