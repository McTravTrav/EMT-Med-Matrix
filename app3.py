import streamlit as st
import random

def get_matrix_data():
    return [
        {"Drug": "Aspirin", "Class": "Anti-platelet", "Route": "Oral", "Indication": "Cardiac Chest Pain", "Contra": "Active or recent bleeding", "Dose": "324 mg"},
        {"Drug": "Nitroglycerin", "Class": "Nitrate", "Route": "SL", "Indication": "Cardiac Chest Pain", "Contra": "BP < 100 systolic, ED meds", "Dose": "0.4 mg"},
        {"Drug": "Epinephrine 1:1000", "Class": "Sympathomimetic", "Route": "IM", "Indication": "Anaphylactic Reaction", "Contra": "None in true emergency", "Dose": "0.3 mg"},
        {"Drug": "Albuterol", "Class": "Bronchodilator", "Route": "Inhaled", "Indication": "Asthma/Wheezing", "Contra": "Tachycardia, Cardiac chest pain", "Dose": "2.5 mg"},
        {"Drug": "Oral Glucose", "Class": "Carbohydrate", "Route": "Buccal", "Indication": "Hypoglycemia", "Contra": "Decreased LOC, airway risk", "Dose": "25 g"},
        {"Drug": "Activated Charcoal", "Class": "Adsorbent", "Route": "Oral", "Indication": "Oral poisoning/overdose", "Contra": "Decreased LOC, corrosives", "Dose": "1 g/kg"},
        {"Drug": "Zofran", "Class": "Anti-emetic", "Route": "Oral (ODT)", "Indication": "Nausea", "Contra": "Allergic, Pregnant", "Dose": "4-8 mg"},
        {"Drug": "Narcan", "Class": "Opiate Antagonist", "Route": "IM, IN", "Indication": "Opiate Overdose", "Contra": "None in true emergency", "Dose": "0.4 - 2.0 mg"},
        {"Drug": "Benadryl", "Class": "Anti-histamine", "Route": "Oral", "Indication": "Allergic Reaction", "Contra": "Hypertension, Constipation", "Dose": "25-50 mg"},
        {"Drug": "Duo-Neb", "Class": "Beta Agonist + Anticholinergic", "Route": "Inhaled", "Indication": "COPD/Asthma", "Contra": "None in true emergency", "Dose": "3.0 mL"},
        {"Drug": "Glucagon", "Class": "Hormone", "Route": "IM", "Indication": "BGL < 50, Unable to swallow", "Contra": "None in true emergency", "Dose": "1 mg"},
        {"Drug": "Duo-Dote", "Class": "Parasympatholytic", "Route": "IM", "Indication": "Organophosphate Poison", "Contra": "None in true emergency", "Dose": "2 mg Atropine"}
    ]
st.set_page_config(layout="wide", page_title="EMT Smart-Matrix")

# --- INITIALIZATION ---
if 'full_meds' not in st.session_state:
    st.session_state.full_meds = get_matrix_data()
    st.session_state.user_table = {}
    st.session_state.selected_piece = None
    st.session_state.active_meds = []
    st.session_state.quiz_cols = []

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Quiz Settings")
    all_possible = ["Drug", "Class", "Route", "Indication", "Contra", "Dose"]
    
    # User selects which columns will be BLANK/QUIZZED
    selected_for_quiz = st.multiselect(
        "Which columns do you want to ANSWER?",
        options=all_possible,
        default=["Drug", "Dose"]
    )
    
    num_rows = st.slider("Number of drugs:", 1, 12, 5)
    
    if st.button("🚀 Start/Reset Quiz", type="primary"):
        st.session_state.active_meds = random.sample(st.session_state.full_meds, num_rows)
        st.session_state.quiz_cols = selected_for_quiz
        st.session_state.user_table = {}
        st.session_state.selected_piece = None
        st.rerun()

st.title("🚑 Smart-Reveal Medical Matrix")
st.write("Columns selected in the sidebar are **blank buttons**. Other columns are **visible info** to help you.")

if not st.session_state.active_meds:
    st.info("Select the columns you want to test yourself on in the sidebar!")
else:
    # 1. HINT
    if st.button("💡 Partial Hint"):
        for r_idx, med in enumerate(st.session_state.active_meds):
            for col in st.session_state.quiz_cols:
                ans = str(med[col])
                hint = f"{ans[:3]}..."
                st.session_state.user_table[(r_idx, col)] = hint
        st.rerun()

    # 2. ANSWER POOL (Only contains items for the QUIZZED columns)
    st.subheader("1. Answer Pool")
    pool = []
    for col in st.session_state.quiz_cols:
        pool.extend([m[col] for m in st.session_state.full_meds])
    pool = sorted(list(set(pool)))

    p_cols = st.columns(4)
    for i, val in enumerate(pool):
        with p_cols[i % 4]:
            if st.button(val, key=f"p_{i}", use_container_width=True):
                st.session_state.selected_piece = val

    if st.session_state.selected_piece:
        st.success(f"Selected: **{st.session_state.selected_piece}**")

    # 3. THE MATRIX
    st.subheader("2. Complete the Matrix")
    
    # Always show all 6 columns
    master_cols = ["Drug", "Class", "Route", "Indication", "Contra", "Dose"]
    grid_ui = st.columns([1.5, 1.5, 1, 2, 2, 1.2]) # Custom widths
    
    # Headers
    for i, name in enumerate(master_cols):
        grid_ui[i].write(f"**{name}**")

    # Rows
    for r_idx, med_data in enumerate(st.session_state.active_meds):
        row_ui = st.columns([1.5, 1.5, 1, 2, 2, 1.2])
        
        for c_idx, c_name in enumerate(master_cols):
            # IF THIS COLUMN IS IN THE QUIZ LIST -> Show a Button
            if c_name in st.session_state.quiz_cols:
                cell_key = (r_idx, c_name)
                user_val = st.session_state.user_table.get(cell_key, "---")
                
                if row_ui[c_idx].button(user_val, key=f"c_{r_idx}_{c_idx}", use_container_width=True):
                    if st.session_state.selected_piece:
                        st.session_state.user_table[cell_key] = st.session_state.selected_piece
                        st.session_state.selected_piece = None
                        st.rerun()
            
            # IF THIS COLUMN IS NOT IN THE QUIZ LIST -> Just show the data
            else:
                row_ui[c_idx].info(med_data[c_name])

    # 4. GRADING
    st.divider()
    if st.button("Grade Matrix", type="primary"):
        score = 0
        total_cells = len(st.session_state.active_meds) * len(st.session_state.quiz_cols)
        
        for r_idx, med in enumerate(st.session_state.active_meds):
            for col in st.session_state.quiz_cols:
                if st.session_state.user_table.get((r_idx, col)) == med[col]:
                    score += 1
                else:
                    st.error(f"❌ Incorrect for {med['Drug']} ({col})")
        
        st.metric("Score", f"{score} / {total_cells}")
        if score == total_cells:
            st.balloons()