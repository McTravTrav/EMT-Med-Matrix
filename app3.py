import streamlit as st
import random

def get_matrix_data():
    return [
        {
            "Drug": "Aspirin", 
            "Class": "Anti-platelet", 
            "Route": "Oral", 
            "Indication": "Cardiac Chest Pain", 
            "Contra": "Active/Recent bleeding", 
            "Dose": "324 mg"
        },
        {
            "Drug": "Nitroglycerin", 
            "Class": "Nitrate", 
            "Route": "SL", 
            "Indication": "Cardiac Chest Pain", 
            "Contra": "BP < 100 systolic, ED meds", 
            "Dose": "0.4 mg"
        },
        {
            "Drug": "Epinephrine 1:1000", 
            "Class": "Sympathomimetic", 
            "Route": "IM", 
            "Indication": "Anaphylaxis", 
            "Contra": "None in true emergency", 
            "Dose": "0.3 mg"
        },
        {
            "Drug": "Albuterol", 
            "Class": "Bronchodilator", 
            "Route": "Inhaled", 
            "Indication": "Asthma/Wheezing", 
            "Contra": "Tachycardia, Chest pain", 
            "Dose": "2.5 mg"
        },
        {
            "Drug": "Oral Glucose", 
            "Class": "Carbohydrate", 
            "Route": "Buccal", 
            "Indication": "Hypoglycemia", 
            "Contra": "Unconscious, No airway", 
            "Dose": "25 g"
        },
        {
            "Drug": "Activated Charcoal", 
            "Class": "Adsorbent", 
            "Route": "Oral", 
            "Indication": "Poisoning/Overdose", 
            "Contra": "Decreased LOC, Corrosives", 
            "Dose": "1 g/kg"
        },
        {
            "Drug": "Zofran", 
            "Class": "Anti-emetic", 
            "Route": "Oral (ODT)", 
            "Indication": "Nausea", 
            "Contra": "Hypersensitivity", 
            "Dose": "4-8 mg"
        },
        {
            "Drug": "Narcan", 
            "Class": "Opiate Antagonist", 
            "Route": "IM, IN", 
            "Indication": "Opiate Overdose", 
            "Contra": "None in emergency", 
            "Dose": "0.4 - 2.0 mg"
        },
        {
            "Drug": "Benadryl", 
            "Class": "Anti-histamine", 
            "Route": "Oral", 
            "Indication": "Allergic Reaction", 
            "Contra": "Asthma, Hypertension", 
            "Dose": "25-50 mg"
        },
        {
            "Drug": "Duo-Neb", 
            "Class": "Beta Agonist + Anticholinergic", 
            "Route": "Inhaled", 
            "Indication": "COPD/Asthma", 
            "Contra": "Tachycardia", 
            "Dose": "3.0 mL"
        },
        {
            "Drug": "Glucagon", 
            "Class": "Hormone", 
            "Route": "IM", 
            "Indication": "BGL < 50, No IV", 
            "Contra": "Pheochromocytoma", 
            "Dose": "1 mg"
        },
        {
            "Drug": "Duo-Dote", 
            "Class": "Parasympatholytic", 
            "Route": "IM", 
            "Indication": "Organophosphate Poison", 
            "Contra": "None in emergency", 
            "Dose": "2 mg Atropine"
        }
    ]
    # --- SESSION STATE ---
if 'matrix_init' not in st.session_state:
    st.session_state.full_meds = get_matrix_data()
    st.session_state.selected_piece = None
    st.session_state.user_table = {}
    st.session_state.quiz_size = 4  # Displaying 4 drugs makes the wide table readable
    st.session_state.active_meds = random.sample(st.session_state.full_meds, st.session_state.quiz_size)
    st.session_state.matrix_init = True

st.set_page_config(layout="wide")
st.title("🚑 Complete Medical Matrix Challenge")
st.write("1. Click an answer from the pool. 2. Click the empty cell in the table where it belongs.")

# 1. THE ANSWER POOL
st.subheader("1. Answer Pool")
categories = ["Class", "Route", "Indication", "Contra", "Dose"]
pool = []
for cat in categories:
    pool.extend([m[cat] for m in st.session_state.full_meds])
pool = sorted(list(set(pool)))

p_cols = st.columns(5)
for i, val in enumerate(pool):
    with p_cols[i % 5]:
        if st.button(val, key=f"pool_{i}", use_container_width=True):
            st.session_state.selected_piece = val

if st.session_state.selected_piece:
    st.success(f"Selected: **{st.session_state.selected_piece}**")

# 2. THE MATRIX
st.subheader("2. Match the Columns")
m_cols = st.columns([1.5, 2, 1.2, 2, 2.5, 1.2])
labels = ["Medication", "Class", "Route", "Indication", "Contraindications", "Dose"]
for i, lab in enumerate(labels):
    m_cols[i].write(f"**{lab}**")

for r_idx, med in enumerate(st.session_state.active_meds):
    row_ui = st.columns([1.5, 2, 1.2, 2, 2.5, 1.2])
    row_ui[0].warning(med["Drug"])
    
    for c_idx, c_name in enumerate(categories):
        cell_key = (r_idx, c_name)
        current_text = st.session_state.user_table.get(cell_key, "---")
        
        if row_ui[c_idx+1].button(current_text, key=f"cell_{r_idx}_{c_name}", use_container_width=True):
            if st.session_state.selected_piece:
                st.session_state.user_table[cell_key] = st.session_state.selected_piece
                st.session_state.selected_piece = None
                st.rerun()

# 3. GRADING
st.divider()
if st.button("Grade Matrix", type="primary"):
    score = 0
    total = len(st.session_state.active_meds) * 5
    for r_idx, med in enumerate(st.session_state.active_meds):
        for c_name in categories:
            if st.session_state.user_table.get((r_idx, c_name)) == med[c_name]:
                score += 1
            else:
                st.error(f"❌ {med['Drug']} {c_name}: Expected '{med[c_name]}'")
    
    st.metric("Final Score", f"{score} / {total}")
    if score == total:
        st.balloons()
        st.success("Perfect! You've mastered this set.")

if st.button("New Random Selection"):
    st.session_state.user_table = {}
    st.session_state.active_meds = random.sample(st.session_state.full_meds, st.session_state.quiz_size)
    st.rerun()