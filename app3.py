import streamlit as st
import random

# ==========================================
# PART 1: THE DATASET (QUESTIONS)
# ==========================================
def get_matrix_data():
    return [
        {"Drug": "Aspirin", "Class": "Anti-platelet", "Route": "Oral", "Indication": "Cardiac Chest Pain", "Contra": "Active or recent bleeding", "Dose": "324 mg"},
        {"Drug": "Nitroglycerin", "Class": "Nitrate", "Route": "SL", "Indication": "Cardiac Chest Pain", "Contra": "BP < 100 systolic, ED meds", "Dose": "0.4 mg"},
        {"Drug": "Epinephrine 1:1000", "Class": "Sympathomimetic", "Route": "IM", "Indication": "Anaphylaxis", "Contra": "None in true emergency", "Dose": "0.3 mg"},
        {"Drug": "Albuterol", "Class": "Bronchodilator", "Route": "Inhaled", "Indication": "Asthma/Wheezing", "Contra": "Tachycardia, Chest pain", "Dose": "2.5 mg"},
        {"Drug": "Oral Glucose", "Class": "Carbohydrate", "Route": "Buccal", "Indication": "Hypoglycemia", "Contra": "Unconscious, No airway", "Dose": "25 g"},
        {"Drug": "Activated Charcoal", "Class": "Adsorbent", "Route": "Oral", "Indication": "Poisoning/Overdose", "Contra": "Decreased LOC, Corrosives", "Dose": "1 g/kg"},
        {"Drug": "Zofran", "Class": "Anti-emetic", "Route": "Oral (ODT)", "Indication": "Nausea", "Contra": "Hypersensitivity", "Dose": "4-8 mg"},
        {"Drug": "Narcan", "Class": "Opiate Antagonist", "Route": "IM, IN", "Indication": "Opiate Overdose", "Contra": "None in true emergency", "Dose": "0.4 - 2.0 mg"},
        {"Drug": "Benadryl", "Class": "Anti-histamine", "Route": "Oral", "Indication": "Allergic Reaction", "Contra": "Hypertension, Constipation", "Dose": "25-50 mg"},
        {"Drug": "Duo-Neb", "Class": "Beta Agonist + Anticholinergic", "Route": "Inhaled", "Indication": "COPD/Asthma", "Contra": "Tachycardia", "Dose": "3.0 mL"},
        {"Drug": "Glucagon", "Class": "Hormone", "Route": "IM", "Indication": "BGL < 50, Unable to swallow", "Contra": "None in true emergency", "Dose": "1 mg"},
        {"Drug": "Duo-Dote", "Class": "Parasympatholytic", "Route": "IM", "Indication": "Organophosphate Poison", "Contra": "None in true emergency", "Dose": "2 mg Atropine"}
    ]

# ==========================================
# PART 2: APPLICATION LOGIC
# ==========================================
st.set_page_config(layout="wide", page_title="EMT Pharma Matrix")

# --- INITIALIZATION ---
if 'full_meds' not in st.session_state:
    st.session_state.full_meds = get_matrix_data()
    st.session_state.user_table = {}
    st.session_state.selected_piece = None
    st.session_state.active_meds = []
    st.session_state.active_cols = []

# --- SIDEBAR CONTROLS ---
with st.sidebar:
    st.header("⚙️ Quiz Setup")
    potential_cols = ["Drug", "Class", "Route", "Indication", "Contra", "Dose"]
    selected_cols = st.multiselect(
        "Columns to fill:",
        options=potential_cols,
        default=["Drug", "Class", "Indication", "Dose"]
    )
    num_drugs = st.slider("Number of drugs:", 1, 12, 5)
    
    if st.button("🚀 Start New Quiz", type="primary"):
        st.session_state.active_meds = random.sample(st.session_state.full_meds, num_drugs)
        st.session_state.active_cols = selected_cols
        st.session_state.user_table = {}
        st.session_state.selected_piece = None
        st.rerun()

st.title("🚑 Custom Medical Matrix")

if not st.session_state.active_meds:
    st.info("👈 Select your columns and drug count in the sidebar, then hit 'Start New Quiz'!")
else:
    # --- PARTIAL HINT BUTTON ---
    if st.button("💡 Give us a Hint (Partial Reveal)"):
        for r_idx, med_data in enumerate(st.session_state.active_meds):
            for c_name in st.session_state.active_cols:
                cell_key = (r_idx, c_name)
                current_text = st.session_state.user_table.get(cell_key, "---")
                if current_text == "---" or "..." in current_text:
                    actual_ans = str(med_data[c_name])
                    hint_len = max(3, int(len(actual_ans) * 0.3))
                    st.session_state.user_table[cell_key] = f"{actual_ans[:hint_len]}..."
        st.rerun()

    # --- 1. ANSWER POOL ---
    st.subheader("1. Pick an Answer")
    pool = []
    for col in st.session_state.active_cols:
        pool.extend([m[col] for m in st.session_state.full_meds])
    pool = sorted(list(set(pool)))

    p_cols = st.columns(5)
    for i, val in enumerate(pool):
        with p_cols[i % 5]:
            if st.button(val, key=f"pool_{i}", use_container_width=True):
                st.session_state.selected_piece = val

    if st.session_state.selected_piece:
        st.success(f"Selected: **{st.session_state.selected_piece}**")

    # --- 2. THE DYNAMIC MATRIX ---
    st.subheader("2. Complete the Table")
    m_cols = st.columns([1.5] * len(st.session_state.active_cols))
    for i, lab in enumerate(st.session_state.active_cols):
        m_cols[i].write(f"**{lab}**")

    for r_idx, med_data in enumerate(st.session_state.active_meds):
        row_ui = st.columns([1.5] * len(st.session_state.active_cols))
        for c_idx, c_name in enumerate(st.session_state.active_cols):
            cell_key = (r_idx, c_name)
            current_text = st.session_state.user_table.get(cell_key, "---")
            
            # Label the button (add icon if it's a hint)
            button_label = f"🔍 {current_text}" if "..." in current_text else current_text

            if row_ui[c_idx].button(button_label, key=f"cell_{r_idx}_{c_name}", use_container_width=True):
                if st.session_state.selected_piece:
                    st.session_state.user_table[cell_key] = st.session_state.selected_piece
                    st.session_state.selected_piece = None
                    st.rerun()

    # --- 3. GRADING ---
    st.divider()
    if st.button("Grade Matrix", type="primary"):
        score = 0
        total = len(st.session_state.active_meds) * len(st.session_state.active_cols)
        for r_idx, med_data in enumerate(st.session_state.active_meds):
            for c_name in st.session_state.active_cols:
                if st.session_state.user_table.get((r_idx, c_name)) == med_data[c_name]:
                    score += 1
                else:
                    st.error(f"❌ Row {r_idx+1}, {c_name}: Expected '{med_data[c_name]}'")
        
        st.metric("Final Score", f"{score} / {total}")
        if score == total:
            st.balloons()
            st.success("Perfect Score! You are ready for the exam.")