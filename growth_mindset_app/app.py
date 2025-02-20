import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import time
import json
import os

import uuid

# Page Config
st.set_page_config(
    page_title="Growth Mindset Tracker",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Updated CSS with enhanced typography
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');
    
    :root {
        --bg-primary: #13111C;
        --bg-secondary: #1A1625;
        --text-primary: #FFFFFF;
        --text-secondary: #E2E8F0;
        --accent-primary: #6D28D9;
        --accent-secondary: #7C3AED;
        --success: #10B981;
        --warning: #F59E0B;
    }

    .stApp {
        background: var(--bg-primary);
        font-family: 'Poppins', sans-serif;
    }

    /* Enhanced Headers */
    h1 {
        color: var(--text-primary);
        font-size: 3.2rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.5px !important;
        line-height: 1.2 !important;
        margin-bottom: 2rem !important;
        background: linear-gradient(120deg, #fff, #a8b1ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 2px 15px rgba(124, 58, 237, 0.3);
    }

    h2 {
        color: var(--text-primary);
        font-size: 2.4rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.3px !important;
        line-height: 1.3 !important;
        margin: 1.5rem 0 !important;
        background: linear-gradient(120deg, #fff, #8b94ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    h3 {
        color: var(--text-primary);
        font-size: 1.8rem !important;
        font-weight: 600 !important;
        margin: 1rem 0 !important;
    }

    /* Main Container with enhanced visibility */
    .main-container {
        background: var(--bg-secondary);
        border-radius: 20px;
        padding: 2.5rem;
        margin: 1.5rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        border: 1px solid rgba(255,255,255,0.1);
    }

    /* Enhanced Text */
    p, .streamlit-expanderHeader {
        color: var(--text-secondary);
        font-size: 1.1rem !important;
        line-height: 1.7 !important;
        font-weight: 400;
    }

    /* Enhanced Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
        border-radius: 15px;
        padding: 2rem;
        color: white;
        text-align: center;
        margin: 1rem 0;
        transition: transform 0.3s ease;
        border: 1px solid rgba(255,255,255,0.1);
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }

    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }

    .metric-value {
        font-size: 3rem !important;
        font-weight: 800 !important;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }

    .metric-label {
        font-size: 1.2rem !important;
        font-weight: 500 !important;
        opacity: 0.9;
    }

    /* Enhanced Quiz Styling */
    .quiz-question {
        font-size: 1.4rem !important;
        font-weight: 600 !important;
        color: var(--text-primary);
        margin-bottom: 1.5rem;
        line-height: 1.5;
        background: linear-gradient(120deg, #fff, #a8b1ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Enhanced Sidebar */
    section[data-testid="stSidebar"] {
        background-color: var(--bg-secondary);
        border-right: 4px solid #6D28D9;
    }
    
    section[data-testid="stSidebar"] .stRadio label {
        color: var(--text-secondary) !important;
        font-size: 1.2rem !important;
        font-weight: 500 !important;
        padding: 0.75rem 1.25rem;
        border-radius: 8px;
        transition: all 0.2s ease;
        margin: 0.3rem 0;
    }
    
    section[data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(255,255,255,0.1);
        color: var(--text-primary) !important;
    }
    
    section[data-testid="stSidebar"] h1 {
        color: var(--text-primary);
        padding: 1.5rem;
        border-bottom: 1px solid rgba(255,255,255,0.1);
        font-size: 2.4rem !important;
        text-align: center;
    }

    /* Button Enhancement */
    .stButton > button {
        width: 100% !important;
        background: linear-gradient(135deg, #6D28D9, #aa1bfc) !important;
        color: white !important;
        border: none !important;
        padding: 1rem 2rem !important;
        border-radius: 16px !important;
        font-weight: 600 !important;
        font-size: 1.2rem !important;
        letter-spacing: 0.5px !important;
        text-transform: uppercase !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 15px rgba(109, 40, 217, 0.3) !important;
        position: relative !important;
        overflow: hidden !important;
    }

    .stButton > button::before {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: -100% !important;
        width: 100% !important;
        height: 100% !important;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent) !important;
        transition: 0.5s !important;
    }

    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 25px rgba(109, 40, 217, 0.5) !important;
        background: linear-gradient(135deg, #7C3AED, #9333EA) !important;
    }

    .stButton > button:hover::before {
        left: 100% !important;
    }

    /* Form Submit Button Special Style */
    .stButton > button[kind="primaryFormSubmit"] {
        background: linear-gradient(135deg, #6D28D9, #9333EA) !important;
                color: white !important;
                border: none !important;
                padding: 0.75rem 1.5rem !important;
                border-radius: 12px !important;
                font-weight: 600 !important;
                font-size: 1rem !important;
                letter-spacing: 0.5px !important;
                text-transform: uppercase !important;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
                box-shadow: 0 4px 15px rgba(109, 40, 217, 0.3) !important;
                position: relative !important;
                overflow: hidden !important;
     }

    /* Modern Card Design */
    .modern-card {
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 24px !important;
        padding: 2rem !important;
        border: 4px solid #6D28D9 !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative !important;
        overflow: hidden !important;
    }

    .modern-card::before {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        bottom: 0 !important;
        border-radius: 24px !important;
        padding: 2px !important;
        background: linear-gradient(135deg, #6D28D9, #9333EA) !important;
        -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0) !important;
        -webkit-mask-composite: xor !important;
        mask-composite: exclude !important;
        opacity: 0 !important;
        transition: opacity 0.3s ease !important;
    }

    .modern-card:hover {
        transform: translateY(-5px) !important;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2) !important;
    }

    .modern-card:hover::before {
        opacity: 1 !important;
    }

    /* Session Form Enhancement */
    form[data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.03) !important;
        padding: 2rem !important;
        border-radius: 24px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1) !important;
        backdrop-filter: blur(10px) !important;
    }

    /* Input Field Enhancement */

            .stDateInput ,  
            .stTextInput ,.stNumberInput {
    background: transparent !important; /* Transparent background */
    border: 1px solid #6D28D9 !important; /* Purple border */
    border-radius: 12px !important;
    padding: 0.75rem !important;
    color: var(--text-primary) !important; /* Light text color */
    transition: all 0.3s ease !important;
}

.stTextInput:focus-within,
.stNumberInput:focus-within,
.stDateInput:focus-within {
    border-color: #9333EA !important; /* Slightly lighter purple on focus */
    box-shadow: 0 0 0 2px rgba(147, 51, 234, 0.2) !important; /* Glow effect */
    transform: translateY(-1px) !important;
}

    /* Goal Card Enhancement */
    .goal-card {
        background: rgba(255, 255, 255, 0.03) !important;
        border-radius: 20px !important;
        padding: 1.5rem !important;
        margin: 1rem 0 !important;
         border: 1px solid #6D28D9 !important; /* Purple border */
       
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1) !important;
        transition: all 0.3s ease !important;
        position: relative !important;
        overflow: hidden !important;
    }

    .goal-card:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2) !important;
    }

    /* Complete Button Special Style */
    .stButton > button[key^="goal_"] {
        background: linear-gradient(135deg, #059669, #10B981) !important;
        font-size: 1rem !important;
        padding: 0.5rem 1.5rem !important;
        text-transform: none !important;
    }

    /* Delete Button Special Style */
    .stButton > button[key^="delete_"] {
        background: linear-gradient(135deg, #DC2626, #EF4444) !important;
        font-size: 1rem !important;
        padding: 0.5rem 1.5rem !important;
        text-transform: none !important;
    }

    /* Session Container Enhancement */
    .session-container {
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 20px !important;
        padding: 1.5rem !important;
        margin: 1rem 0 !important;
        border: 1px solid #6D28D9 !important; /* Purple border */
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1) !important;
        transition: all 0.3s ease !important;
    }

    .session-container:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2) !important;
         border: 1px solid #6D28D9 !important; /* Purple border */
    }

    /* Progress Bar Enhancement */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary));
        height: 8px !important;
        border-radius: 4px;
         border: 1px solid #6D28D9 !important; /* Purple border */
    }

    /* Delete Button Styling */
    .stButton > button[key^="delete_"] {
        background: rgba(239, 68, 68, 0.1);
        color: #EF4444;
        padding: 0.5rem;
        border-radius: 8px;
        border: 1px solid rgba(239, 68, 68, 0.2);
        transition: all 0.2s ease;
    }

    .stButton > button[key^="delete_"]:hover {
        background: rgba(239, 68, 68, 0.2);
        transform: translateY(-2px);
    }

    /* Session Container Styling */
    .session-container {
        background: var(--bg-secondary);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border: 1px solid rgba(255,255,255,0.1);
    }

    /* Horizontal Line Styling */
    hr {
        border: none;
        border-top: 1px solid #6D28D9 !important; /* Purple border */
        margin: 0.5rem 0;
    }

    /* Log Session Button Special Style */
    .stButton > button[kind="primaryFormSubmit"],
    form[data-testid="stForm"] .stButton > button {
        background: linear-gradient(135deg, #FF3366, #FF6B98) !important;
        color: white !important;
        border: none !important;
        padding: 1rem 2rem !important;
        border-radius: 16px !important;
        font-weight: 600 !important;
        font-size: 1.2rem !important;
        letter-spacing: 0.5px !important;
        text-transform: uppercase !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative !important;
        overflow: hidden !important;
        box-shadow: 0 4px 15px rgba(255, 51, 102, 0.3),
                    0 0 0 2px rgba(255, 51, 102, 0.2) !important;
    }

    .stButton > button[kind="primaryFormSubmit"]::before,
    form[data-testid="stForm"] .stButton > button::before {
        content: '' !important;
        position: absolute !important;
        inset: -2px !important;
        background: linear-gradient(90deg, 
            #FF3366, #FF6B98, #FF99CC, #FF3366) !important;
        background-size: 400% !important;
        z-index: -1 !important;
        animation: glitterBorder 8s linear infinite !important;
        filter: blur(8px) !important;
    }

    .stButton > button[kind="primaryFormSubmit"]:hover,
    form[data-testid="stForm"] .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 25px rgba(255, 51, 102, 0.5),
                    0 0 0 3px rgba(255, 51, 102, 0.3) !important;
        background: linear-gradient(135deg, #FF4D7F, #FF85AD) !important;
    }

    /* Simple Purple Add Goal Button */
    form:has(input[type="text"]) .stButton > button {
        background: #6D28D9 !important;  /* Solid purple background */
        color: white !important;
        border: none !important;
        padding: 1rem 2rem !important;
        border-radius: 16px !important;
        font-weight: 600 !important;
        font-size: 1.2rem !important;
        letter-spacing: 0.5px !important;
        box-shadow: 0 4px 15px rgba(109, 40, 217, 0.3) !important;
        transition: all 0.3s ease !important;
    }

    form:has(input[type="text"]) .stButton > button:hover {
        background: #7C3AED !important;  /* Slightly lighter purple on hover */
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(109, 40, 217, 0.4) !important;
    }

    /* Button Animation */
    @keyframes glitterBorder {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    </style>
""", unsafe_allow_html=True)

# Data Management
def load_data():
    if not os.path.exists('data.json'):
        return {'goals': [], 'progress': [], 'metrics': {'total_hours': 0, 'completed_tasks': 0}}
    with open('data.json', 'r') as f:
        return json.load(f)

def save_data(data):
    with open('data.json', 'w') as f:
        json.dump(data, f)

# Dashboard Page
def dashboard():
    st.markdown("<h1>Growth Dashboard</h1>", unsafe_allow_html=True)
    
    data = load_data()
    
    # Key Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value">{}</div>
                <div class="metric-label">Study Hours</div>
            </div>
        """.format(data['metrics']['total_hours']), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value">{}</div>
                <div class="metric-label">Tasks Completed</div>
            </div>
        """.format(data['metrics']['completed_tasks']), unsafe_allow_html=True)
    
    with col3:
        completion_rate = (data['metrics']['completed_tasks'] / max(len(data['goals']), 1)) * 100 if data['goals'] else 0
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value">{:.1f}%</div>
                <div class="metric-label">Completion Rate</div>
            </div>
        """.format(completion_rate), unsafe_allow_html=True)

    # Progress Chart
    st.markdown("<h2>Progress Over Time</h2>", unsafe_allow_html=True)
    if data['progress']:
        df = pd.DataFrame(data['progress'])
        fig = px.line(df, x='date', y='hours', title='Daily Study Hours')
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#E2E8F0'
        )
        st.plotly_chart(fig, use_container_width=True)

# Progress Tracker Page
def progress_tracker():
    st.markdown("<h1>Track Your Progress</h1>", unsafe_allow_html=True)
    
    data = load_data()
    
    # Add new study session
    with st.form("study_session"):
        col1, col2 = st.columns([3, 1])
        with col1:
            hours = st.number_input("Study Hours", min_value=0.5, max_value=24.0, step=0.5)
        with col2:
            date = st.date_input("Date", datetime.now())
        notes = st.text_area("Session Notes")
        if st.form_submit_button("Log Session"):
            data['progress'].append({
                'date': date.strftime("%Y-%m-%d"),
                'hours': hours,
                'notes': notes,
                'id': str(uuid.uuid4())  # Add unique ID for each session
            })
            data['metrics']['total_hours'] += hours
            save_data(data)
            st.success("Session logged successfully!")
            time.sleep(1)
            st.rerun()

    # Show recent sessions with delete option
    if data['progress']:
        st.markdown("<h2>Recent Sessions</h2>", unsafe_allow_html=True)
        
        # Create a DataFrame for display
        df = pd.DataFrame(data['progress'])
        
        # Display each session with delete button
        for idx, session in enumerate(data['progress']):
            with st.container():
                col1, col2, col3, col4 = st.columns([2, 2, 3, 1])
                with col1:
                    st.markdown(f"**Date:** {session['date']}")
                with col2:
                    st.markdown(f"**Hours:** {session['hours']}")
                with col3:
                    st.markdown(f"**Notes:** {session.get('notes', '-')}")
                with col4:
                    if st.button("🗑️", key=f"delete_{idx}"):
                        # Update total hours
                        data['metrics']['total_hours'] -= session['hours']
                        # Remove session
                        data['progress'].remove(session)
                        save_data(data)
                        st.success("Session deleted successfully!")
                        time.sleep(1)
                        st.rerun()
                st.markdown("<hr>", unsafe_allow_html=True)

        # Add summary statistics
        if data['progress']:
            st.markdown("### Summary Statistics")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">{len(data['progress'])}</div>
                        <div class="metric-label">Total Sessions</div>
                    </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">{data['metrics']['total_hours']}</div>
                        <div class="metric-label">Total Hours</div>
                    </div>
                """, unsafe_allow_html=True)
            with col3:
                avg_hours = data['metrics']['total_hours'] / len(data['progress']) if data['progress'] else 0
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">{avg_hours:.1f}</div>
                        <div class="metric-label">Avg Hours/Session</div>
                    </div>
                """, unsafe_allow_html=True)

# Goals Page
def goals():
    st.markdown("<h1>Learning Goals</h1>", unsafe_allow_html=True)
    
    data = load_data()
    
    # Add new goal
    with st.form("new_goal"):
        goal = st.text_input("New Goal")
        deadline = st.date_input("Deadline")
          
        # Custom CSS for the "Add Goal" button
        st.markdown("""
            <style>
            .stButton > button[key^="Add Goal_"] {
                background: linear-gradient(135deg, #6D28D9, #9333EA) !important;
                color: white !important;
                border: none !important;
                padding: 0.75rem 1.5rem !important;
                border-radius: 12px !important;
                font-weight: 600 !important;
                font-size: 1rem !important;
                letter-spacing: 0.5px !important;
                text-transform: uppercase !important;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
                box-shadow: 0 4px 15px rgba(109, 40, 217, 0.3) !important;
                position: relative !important;
                overflow: hidden !important;
            }

            .stButton > button:hover {
                transform: translateY(-2px) !important;
                box-shadow: 0 6px 20px rgba(109, 40, 217, 0.5) !important;
                background: linear-gradient(135deg, #7C3AED, #9333EA) !important;
            }

            .stButton > button:active {
                transform: translateY(0) !important;
                box-shadow: 0 4px 15px rgba(109, 40, 217, 0.3) !important;
            }
            </style>
        """, unsafe_allow_html=True)

        if st.form_submit_button("Add Goal"):
            data['goals'].append({
                'goal': goal,
                'deadline': deadline.strftime("%Y-%m-%d"),
                'completed': False
            })
            save_data(data)
            st.success("Goal added successfully!")
            time.sleep(1)
            st.rerun()

    # Show active goals
    if data['goals']:
        st.markdown("<h2>Active Goals</h2>", unsafe_allow_html=True)
        for i, goal in enumerate(data['goals']):
            if not goal['completed']:
                col1, col2 = st.columns([4,1])
                with col1:
                    st.markdown(f"**{goal['goal']}** (Due: {goal['deadline']})")
                with col2:
                    if st.button("Complete", key=f"goal_{i}"):
                        data['goals'][i]['completed'] = True
                        data['metrics']['completed_tasks'] += 1
                        save_data(data)
                        st.rerun()

# Updated Quiz Data with fixed quotes
QUIZZES = {
    'growth_mindset': [
        {
            'question': 'What is the main characteristic of a growth mindset?',
            'options': [
                'Belief that abilities can be developed through effort',
                'Belief that talents are fixed at birth',
                'Focus on proving yourself to others',
                'Avoiding challenges to maintain success'
            ],
            'correct': 0
        },
        {
            'question': 'Which response best demonstrates a growth mindset?',
            'options': [
                "I'm not good at this",
                "I can learn to do this with practice",
                "This is too hard for me",
                "I'll never understand this"
            ],
            'correct': 1
        },
        {
            'question': 'How does a growth mindset view challenges?',
            'options': [
                'As opportunities to learn and grow',
                'As threats to avoid',
                'As proof of inadequacy',
                'As unnecessary obstacles'
            ],
            'correct': 0
        },
        {
            'question': 'What role does failure play in a growth mindset?',
            'options': [
                'It should be avoided at all costs',
                'It defines your capabilities',
                "It's a natural part of learning",
                'It means you should give up'
            ],
            'correct': 2
        },
        {
            'question': 'Which strategy best supports developing a growth mindset?',
            'options': [
                'Avoiding difficult tasks',
                'Setting challenging but achievable goals',
                "Only doing what you're already good at",
                'Comparing yourself to others'
            ],
            'correct': 1
        },
        {
            'question': 'How should feedback be viewed in a growth mindset?',
            'options': [
                'As personal criticism',
                'As something to ignore',
                'As an opportunity to improve',
                'As a sign of weakness'
            ],
            'correct': 2
        },
        {
            'question': 'What is the best way to respond to setbacks with a growth mindset?',
            'options': [
                'Give up and try something easier',
                'Analyze what went wrong and adjust strategy',
                'Blame external factors',
                'Avoid similar challenges in future'
            ],
            'correct': 1
        },
        {
            'question': 'Which statement about intelligence aligns with a growth mindset?',
            'options': [
                'Intelligence is fixed at birth',
                'Intelligence can be developed like a muscle',
                'Intelligence is determined by genetics only',
                'Intelligence cannot be changed'
            ],
            'correct': 1
        },
        {
            'question': 'How does a growth mindset affect learning?',
            'options': [
                'It makes learning unnecessary',
                'It limits learning potential',
                'It enhances learning through persistence',
                'It makes learning more stressful'
            ],
            'correct': 2
        },
        {
            'question': 'What is the relationship between effort and ability in a growth mindset?',
            'options': [
                'Effort is seen as fruitless',
                'Effort is a path to mastery',
                'Effort means you lack ability',
                'Effort should be minimized'
            ],
            'correct': 1
        }
    ]
}

# Quiz Component
def quiz_page():
    st.markdown("<h1>Knowledge Check</h1>", unsafe_allow_html=True)
    
    # Initialize session state for quiz
    if 'quiz_state' not in st.session_state:
        st.session_state.quiz_state = {
            'current_question': 0,
            'score': 0,
            'completed': False,
            'answers': []
        }
    
    quiz = QUIZZES['growth_mindset']
    
    if not st.session_state.quiz_state['completed']:
        current_q = st.session_state.quiz_state['current_question']
        
        # Progress Bar
        progress = (current_q / len(quiz)) * 100
        st.markdown(f"""
            <div class="quiz-progress">
                <div class="quiz-progress-bar" style="width: {progress}%"></div>
            </div>
        """, unsafe_allow_html=True)
        
        # Display Question
        st.markdown(f"""
            <div class="quiz-card">
                <div class="quiz-question">{quiz[current_q]['question']}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Display Options
        for i, option in enumerate(quiz[current_q]['options']):
            if st.button(option, key=f"option_{i}"):
                # Check answer
                if i == quiz[current_q]['correct']:
                    st.session_state.quiz_state['score'] += 1
                    st.markdown("""
                        <div class="quiz-result result-correct">
                            ✅ Correct! Well done!
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                        <div class="quiz-result result-incorrect">
                            ❌ Incorrect. Keep learning!
                        </div>
                    """, unsafe_allow_html=True)
                
                st.session_state.quiz_state['answers'].append(i)
                
                # Move to next question or complete quiz
                if current_q + 1 < len(quiz):
                    st.session_state.quiz_state['current_question'] += 1
                else:
                    st.session_state.quiz_state['completed'] = True
                time.sleep(1)
                st.rerun()
    
    else:
        # Show final score
        final_score = (st.session_state.quiz_state['score'] / len(quiz)) * 100
        st.markdown(f"""
            <div class="score-card">
                <div class="score-value">{final_score:.0f}%</div>
                <div class="score-label">Final Score</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Review answers
        st.markdown("<h2>Review Your Answers</h2>", unsafe_allow_html=True)
        for i, (q, a) in enumerate(zip(quiz, st.session_state.quiz_state['answers'])):
            correct = a == q['correct']
            st.markdown(f"""
                <div class="quiz-card">
                    <div class="quiz-question">{i+1}. {q['question']}</div>
                    <div class="quiz-option">Your answer: {q['options'][a]}</div>
                    <div class="quiz-option">Correct answer: {q['options'][q['correct']]}</div>
                    <div class="quiz-result {'result-correct' if correct else 'result-incorrect'}">
                        {'✅ Correct' if correct else '❌ Incorrect'}
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        if st.button("Retake Quiz"):
            st.session_state.quiz_state = {
                'current_question': 0,
                'score': 0,
                'completed': False,
                'answers': []
            }
            st.rerun()

# Main App
def main():
    st.sidebar.markdown("""
        <div style='padding: 1rem; background: var(--bg-secondary); border-radius: 10px; margin-bottom: 1rem;'>
            <h1 style='color: var(--text-primary); margin-bottom: 1rem;'>Navigation</h1>
        </div>
    """, unsafe_allow_html=True)
    
    page = st.sidebar.radio("", 
        ["Dashboard", "Progress Tracker", "Goals", "Quiz"],
        key="navigation",
        format_func=lambda x: f"📊 {x}" if x == "Dashboard"
                    else f"📈 {x}" if x == "Progress Tracker"
                    else f"🎯 {x}" if x == "Goals"
                    else f"❓ {x}")
    
    if page == "Dashboard":
        dashboard()
    elif page == "Progress Tracker":
        progress_tracker()
    elif page == "Goals":
        goals()
    elif page == "Quiz":
        quiz_page()

if __name__ == "__main__":
    main()