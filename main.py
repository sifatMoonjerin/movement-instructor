import time
import pandas as pd
import streamlit as st
from pathlib import Path

# variables
movement_options = {
    "Leg Movements": ["LEG UP", "LEG DOWN"],
    "Ankle Movements": ["ANKLE UP", "ANKLE DOWN"],
    "Leg Up Only": ["LEG UP"],
    "Leg Down Only": ["LEG DOWN"],
    "Ankle Up Only": ["ANKLE UP"],
    "Ankle Down Only": ["ANKLE DOWN"]
}

# helper functions
def custom_write(placeholder, text, fw = 300):
    placeholder.markdown(
        f"""
        <div style="display: flex; justify-content: center; align-items: center;">
            <p style="font-size: 48px; font-weight: {fw}; color: darkblue; word-spacing: 10px">{text}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

def handle_moves(placeholder):
    start_time = time.time()
    idx = 0
    total_moves = len(movement_options[st.session_state.moves])
    
    while time.time() - start_time < st.session_state.duration:
        move = movement_options[st.session_state.moves][idx]

        custom_write(placeholder, move, 600)
        
        timestamp = int(time.time() * 1000)
        st.session_state.records.append([st.session_state.user_code, move, st.session_state.type, timestamp])
        time.sleep(3)
        
        custom_write(instruction_placeholder, "")
        time.sleep(2)
        idx = (idx + 1) % total_moves

def go_to_next_step():
    st.session_state.step += 1        

# state init
if "step" not in st.session_state:
    st.session_state.step = 0
if "user_code" not in st.session_state:
    st.session_state.user_code = ''
if "moves" not in st.session_state:
    st.session_state.moves = ''
if "type" not in st.session_state:
    st.session_state.type = 0
if "duration" not in st.session_state:
    st.session_state.duration = 0
if "records" not in st.session_state:
    st.session_state.records = []


# app
st.title("")

if st.session_state.step == 0:
    st.session_state.user_code = st.text_input("Enter User code:")

if st.session_state.step == 1:
    st.session_state.moves = st.selectbox("Choose a movement type:", list(movement_options.keys()))
    if st.session_state.moves in ["Leg Movements", "Ankle Movements"]:
        st.session_state.type = "Execution"
        st.session_state.duration = 60
    else:
        st.session_state.type = "Imagination"
        st.session_state.duration = 30

if st.session_state.step == 2:
    instruction_placeholder = st.empty()
    custom_write(instruction_placeholder, "Get Ready...")
    time.sleep(3)
    handle_moves(instruction_placeholder)
    custom_write(instruction_placeholder, "Session Completed!")
    
if st.session_state.step == 3:
    df = pd.DataFrame(st.session_state.records, columns=["User", "Move", "Type", "Timestamp"])
    
    file_name = f"{st.session_state.user_code}_{st.session_state.moves}_{st.session_state.type}.csv"
    
    if st.secrets["IS_LOCAL"]:
        file_path = Path(f"./data/{st.session_state.user_code}/{file_name}")    
        file_path.parent.mkdir(parents=True, exist_ok=True)

        csv_data = df.to_csv(file_path, index=False)
        st.success(f"Timestamps saved in {file_path}")
    
    csv_data = df.to_csv(index=False)
    st.download_button(
        label="Download CSV",
        data=csv_data,
        file_name=file_name,
        mime="text/csv",
    )
    
if st.session_state.step < 3:
    st.markdown("""
        <style>
        .stButton>button {
            position: fixed;
            bottom: 40px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 9999;
        }
        </style>
    """, unsafe_allow_html=True)
    st.button("Next Step", on_click=go_to_next_step)

