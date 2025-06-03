import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json

# Initialize session state
if 'quit_date' not in st.session_state:
    st.session_state.quit_date = None
if 'cigarettes_per_day' not in st.session_state:
    st.session_state.cigarettes_per_day = None
if 'price_per_pack' not in st.session_state:
    st.session_state.price_per_pack = None

def calculate_savings():
    if st.session_state.quit_date and st.session_state.cigarettes_per_day and st.session_state.price_per_pack:
        days_since_quit = (datetime.now() - st.session_state.quit_date).days
        packs_saved = days_since_quit * st.session_state.cigarettes_per_day / 20
        total_savings = packs_saved * st.session_state.price_per_pack
        return days_since_quit, packs_saved, total_savings
    return 0, 0, 0

def main():
    st.title("Quit Smoking Tracker")
    st.write("""
    Welcome to your smoking cessation journey! This app helps you track your progress 
    and visualize the benefits of quitting smoking.
    """)

    # Input section
    st.header("Your Quit Details")
    
    col1, col2 = st.columns(2)
    with col1:
        quit_date = st.date_input(
            "When did you quit smoking?",
            value=st.session_state.quit_date if st.session_state.quit_date else None
        )
        
    with col2:
        cigarettes_per_day = st.number_input(
            "How many cigarettes did you smoke per day?",
            min_value=1,
            max_value=100,
            value=st.session_state.cigarettes_per_day if st.session_state.cigarettes_per_day else 20
        )
    
    price_per_pack = st.number_input(
        "What was the price of a pack of cigarettes?",
        min_value=0.0,
        value=st.session_state.price_per_pack if st.session_state.price_per_pack else 10.0
    )

    # Save inputs to session state
    if quit_date:
        st.session_state.quit_date = quit_date
    st.session_state.cigarettes_per_day = cigarettes_per_day
    st.session_state.price_per_pack = price_per_pack

    # Results section
    st.header("Your Progress")
    if st.session_state.quit_date:
        days_since_quit, packs_saved, total_savings = calculate_savings()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Days Smoke-Free", f"{days_since_quit} days")
        with col2:
            st.metric("Packs Saved", f"{packs_saved:.1f} packs")
        with col3:
            st.metric("Money Saved", f"${total_savings:.2f}")

        # Additional statistics
        st.subheader("Additional Statistics")
        st.write(f"- Hours smoke-free: {days_since_quit * 24}")
        st.write(f"- Minutes smoke-free: {days_since_quit * 24 * 60}")
        
        # Motivational message
        st.subheader("Motivation")
        if days_since_quit < 7:
            st.write("Great job! You're making progress every day. Keep it up!")
        elif days_since_quit < 30:
            st.write("You've made it through the first week! Your body is already starting to heal.")
        elif days_since_quit < 90:
            st.write("You're over a month smoke-free! Your lung function is improving.")
        else:
            st.write("Congratulations! You're making a significant positive change in your life.")
    else:
        st.write("Please enter your quit date to start tracking your progress.")

if __name__ == "__main__":
    main()
