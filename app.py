"""
SQL Database Chat Application
A professional Streamlit application for interacting with SQL databases using natural language.
"""

import streamlit as st
from pathlib import Path
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import sqlite3
from langchain_groq import ChatGroq
import logging
from typing import Optional, Dict, Any
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Constants
LOCALDB = "USE_LOCALDB"
MYSQL = "USE_MYSQL"
DEFAULT_MODEL = "llama-3.1-70b-versatile"
CACHE_TTL = 7200  # 2 hours in seconds

# Page configuration
st.set_page_config(
    page_title="SQL Database Chat Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f0f2f6;
        margin: 1rem 0;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .error-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.markdown('<p class="main-header">🤖 SQL Database Chat Assistant</p>', unsafe_allow_html=True)
st.markdown("""
    **Transform your database queries into natural conversations!**  
    Ask questions in plain English and get instant insights from your SQL database.
""")

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Database Selection
    st.subheader("📊 Database Connection")
    radio_opt = [
        "🗄️ Use SQLite Database (student.db)",
        "🔗 Connect to MySQL Database"
    ]
    selected_opt = st.radio(
        label="Select Database Type",
        options=radio_opt,
        help="Choose between local SQLite or remote MySQL database"
    )
    
    db_type = MYSQL if radio_opt.index(selected_opt) == 1 else LOCALDB
    
    # MySQL Configuration
    mysql_config = {}
    if db_type == MYSQL:
        st.markdown("---")
        st.subheader("🔐 MySQL Credentials")
        mysql_config = {
            'host': st.text_input("Host", placeholder="localhost or IP address"),
            'user': st.text_input("Username", placeholder="root"),
            'password': st.text_input("Password", type="password"),
            'database': st.text_input("Database Name", placeholder="mydb")
        }
    
    # API Configuration
    st.markdown("---")
    st.subheader("🔑 API Configuration")
    api_key = st.text_input(
        label="Groq API Key",
        type="password",
        help="Enter your Groq API key. Get one at https://console.groq.com"
    )
    
    # Model Selection
    model_options = [
        "llama-3.1-70b-versatile",
        "llama-3.1-8b-instant",
        "mixtral-8x7b-32768",
        "gemma2-9b-it"
    ]
    selected_model = st.selectbox(
        "Select Model",
        options=model_options,
        help="Choose the LLM model for query processing"
    )
    
    # Advanced Settings
    with st.expander("⚙️ Advanced Settings"):
        verbose_mode = st.checkbox("Enable Verbose Mode", value=False)
        max_iterations = st.slider("Max Agent Iterations", 1, 20, 10)
    
    # Action Buttons
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Reconnect", use_container_width=True):
            st.cache_resource.clear()
            st.rerun()
    with col2:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state["messages"] = []
            st.rerun()
    
    # About Section
    st.markdown("---")
    st.subheader("ℹ️ About")
    st.info(
        "**SQL Chat Assistant v2.0**\n\n"
        "This application uses LangChain agents with Groq LLMs to enable "
        "natural language interaction with SQL databases.\n\n"
        "**Features:**\n"
        "- Natural language queries\n"
        "- SQLite & MySQL support\n"
        "- Real-time responses\n"
        "- Secure connections"
    )
    
    # Footer
    st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")


# Validation Functions
def validate_inputs() -> tuple[bool, Optional[str]]:
    """Validate user inputs and return status and error message if any."""
    if not api_key:
        return False, "⚠️ Please provide your Groq API key in the sidebar to continue."
    
    if db_type == MYSQL:
        required_fields = ['host', 'user', 'password', 'database']
        missing_fields = [field for field in required_fields if not mysql_config.get(field)]
        
        if missing_fields:
            return False, f"⚠️ Please provide the following MySQL details: {', '.join(missing_fields)}"
    
    return True, None


# Database Configuration
@st.cache_resource(ttl=CACHE_TTL, show_spinner=False)
def configure_database(
    db_uri: str,
    host: Optional[str] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
    database: Optional[str] = None
) -> Optional[SQLDatabase]:
    """
    Configure and return database connection.
    
    Args:
        db_uri: Database type (LOCALDB or MYSQL)
        host: MySQL host address
        user: MySQL username
        password: MySQL password
        database: MySQL database name
    
    Returns:
        SQLDatabase object or None if connection fails
    """
    try:
        if db_uri == LOCALDB:
            db_path = (Path(__file__).parent / "student.db").absolute()
            
            if not db_path.exists():
                logger.error(f"Database file not found: {db_path}")
                st.error(f"❌ Database file not found: {db_path}")
                return None
            
            creator = lambda: sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
            engine = create_engine("sqlite:///", creator=creator)
            logger.info(f"Connected to SQLite database: {db_path}")
            
        elif db_uri == MYSQL:
            connection_string = (
                f"mysql+mysqlconnector://{user}:{password}@{host}/{database}"
            )
            engine = create_engine(connection_string)
            logger.info(f"Connected to MySQL database: {database}@{host}")
        
        return SQLDatabase(engine)
    
    except SQLAlchemyError as e:
        logger.error(f"Database connection error: {str(e)}")
        st.error(f"❌ Database connection failed: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        st.error(f"❌ An unexpected error occurred: {str(e)}")
        return None


# LLM Initialization
@st.cache_resource(show_spinner=False)
def initialize_llm(_api_key: str, model: str) -> Optional[ChatGroq]:
    """
    Initialize and return the Groq LLM.
    
    Args:
        _api_key: Groq API key (prefixed with _ to prevent hashing)
        model: Model name to use
    
    Returns:
        ChatGroq object or None if initialization fails
    """
    try:
        llm = ChatGroq(
            groq_api_key=_api_key,
            model_name=model,
            streaming=True,
            temperature=0
        )
        logger.info(f"Initialized LLM with model: {model}")
        return llm
    except Exception as e:
        logger.error(f"LLM initialization error: {str(e)}")
        st.error(f"❌ Failed to initialize LLM: {str(e)}")
        return None


# Agent Creation
def create_agent(llm: ChatGroq, database: SQLDatabase, verbose: bool = False, max_iter: int = 10):
    """
    Create and return SQL agent.
    
    Args:
        llm: Language model instance
        database: SQLDatabase instance
        verbose: Enable verbose output
        max_iter: Maximum iterations for agent
    
    Returns:
        SQL agent instance
    """
    try:
        agent = create_sql_agent(
            llm=llm,
            db=database,
            verbose=verbose,
            agent_type="openai-tools",
            handle_parsing_errors=True,
            max_iterations=max_iter
        )
        logger.info("SQL agent created successfully")
        return agent
    except Exception as e:
        logger.error(f"Agent creation error: {str(e)}")
        raise


# Main Application Logic
def main():
    """Main application logic."""
    
    # Validate inputs
    is_valid, error_message = validate_inputs()
    if not is_valid:
        st.warning(error_message)
        st.stop()
    
    # Initialize components
    with st.spinner("🔄 Connecting to database and initializing AI assistant..."):
        try:
            # Initialize LLM
            llm = initialize_llm(api_key, selected_model)
            if not llm:
                st.stop()
            
            # Configure database
            if db_type == MYSQL:
                db = configure_database(
                    db_type,
                    mysql_config['host'],
                    mysql_config['user'],
                    mysql_config['password'],
                    mysql_config['database']
                )
            else:
                db = configure_database(db_type)
            
            if not db:
                st.stop()
            
            # Create agent
            agent = create_agent(llm, db, verbose_mode, max_iterations)
            
            # Success message
            st.success("✅ Connected successfully! Ready to answer your questions.")
            
        except Exception as e:
            logger.error(f"Initialization error: {str(e)}")
            st.error(f"❌ Failed to initialize application: {str(e)}")
            st.stop()
    
    # Display database info
    with st.expander("📋 Database Information", expanded=False):
        try:
            tables = db.get_usable_table_names()
            st.write(f"**Available Tables:** {', '.join(tables)}")
            
            if tables:
                selected_table = st.selectbox("View Table Schema", tables)
                if selected_table:
                    schema = db.get_table_info([selected_table])
                    st.code(schema, language="sql")
        except Exception as e:
            st.warning(f"Could not fetch database information: {str(e)}")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {
                "role": "assistant",
                "content": "👋 Hello! I'm your SQL Database Assistant. Ask me anything about your database, and I'll help you find the information you need!"
            }
        ]
    
    # Display chat history
    for idx, msg in enumerate(st.session_state.messages):
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    
    # Chat input
    user_query = st.chat_input(
        placeholder="Ask a question about your database... (e.g., 'Show me all students with marks above 80')"
    )
    
    if user_query:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.write(user_query)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("🤔 Analyzing your question and querying the database..."):
                try:
                    response = agent.run(user_query)
                    st.write(response)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": response}
                    )
                    logger.info(f"Successfully processed query: {user_query[:50]}...")
                    
                except Exception as e:
                    error_msg = f"❌ I encountered an error while processing your question: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": error_msg}
                    )
                    logger.error(f"Query processing error: {str(e)}")


# Run the application
if __name__ == "__main__":
    main()
