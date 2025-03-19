import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from PIL import Image

st.title("Border Dispute: Wakanda vs. Atlantis")

st.write(
    "Wakanda and Atlantis face a critical decision regarding their border dispute."
    "Choose your country's strategy:"
)

payoff_matrix = {
    ("Cooperate", "Cooperate"): {
        "Wakanda": {"value": 3, "description": "De-escalation, reduced military spending, improved diplomacy."},
        "Atlantis": {"value": 3, "description": "De-escalation, reduced military spending, improved diplomacy."},
    },
    ("Cooperate", "Defect"): {
        "Wakanda": {"value": 0, "description": "Vulnerable border, loss of strategic advantage, potential for exploitation."},
        "Atlantis": {"value": 4, "description": "Significant strategic advantage, potential for territorial gain, increased military power."},
    },
    ("Defect", "Cooperate"): {
        "Wakanda": {"value": 4, "description": "Significant strategic advantage, potential for territorial gain, increased military power."},
        "Atlantis": {"value": 0, "description": "Vulnerable border, loss of strategic advantage, potential for exploitation."},
    },
    ("Defect", "Defect"): {
        "Wakanda": {"value": 1, "description": "Increased tensions, heightened military presence, risk of armed conflict."},
        "Atlantis": {"value": 1, "description": "Increased tensions, heightened military presence, risk of armed conflict."},
    },
}

st.subheader("Payoff Matrix:")
df = pd.DataFrame(
    {
        "Atlantis Cooperates": [
            f"Wakanda: {payoff_matrix[('Cooperate', 'Cooperate')]['Wakanda']['value']}<br>{payoff_matrix[('Cooperate', 'Cooperate')]['Wakanda']['description']}",
            f"Wakanda: {payoff_matrix[('Defect', 'Cooperate')]['Wakanda']['value']}<br>{payoff_matrix[('Defect', 'Cooperate')]['Wakanda']['description']}",
        ],
        "Atlantis Defects": [
            f"Wakanda: {payoff_matrix[('Cooperate', 'Defect')]['Wakanda']['value']}<br>{payoff_matrix[('Cooperate', 'Defect')]['Wakanda']['description']}",
            f"Wakanda: {payoff_matrix[('Defect', 'Defect')]['Wakanda']['value']}<br>{payoff_matrix[('Defect', 'Defect')]['Wakanda']['description']}",
        ],
    },
    index=["Wakanda Cooperates", "Wakanda Defects"],
)
st.markdown(df.to_html(escape=False), unsafe_allow_html=True)

st.subheader("About the Game:")
st.write(
    "This game simulates a simplified geopolitical scenario where two countries,"
    " Wakanda and Atlantis, must choose between cooperation and defection."
    " The outcomes represent potential benefits and costs associated with each choice."
)

st.subheader("Countries in Conflict!")
col1, col2 = st.columns(2)
display_height = 200

try:
    wakanda_image = Image.open("assets/Wakanda.jpg")
    atlantis_image = Image.open("assets/Atlantis.jpg")

    wakanda_aspect_ratio = wakanda_image.width / wakanda_image.height
    wakanda_display_width = int(display_height * wakanda_aspect_ratio)
    wakanda_resized = wakanda_image.resize((wakanda_display_width, display_height))

    atlantis_aspect_ratio = atlantis_image.width / atlantis_image.height
    atlantis_display_width = int(display_height * atlantis_aspect_ratio)
    atlantis_resized = atlantis_image.resize((atlantis_display_width, display_height))

    with col1:
        st.image(wakanda_resized, caption="Wakanda", width=wakanda_display_width)
        st.write("Wakanda: A technologically advanced nation with a strong commitment to isolationism.")

    with col2:
        st.image(atlantis_resized, caption="Atlantis", width=atlantis_display_width)
        st.write("Atlantis: An underwater kingdom with powerful military capabilities and ambitions for expansion.")

except FileNotFoundError:
    st.error("Image files not found. Please check the file paths.")

rounds = st.slider("Number of rounds", min_value=1, max_value=50, value=1)
st.session_state.rounds = rounds

wakanda_strategy = st.selectbox("Wakanda's Strategy:", ["Always Cooperate", "Always Defect", "Tit-for-Tat", "Grim Trigger", "Forgiving", "Mixed Strategies"])
atlantis_strategy = st.selectbox("Atlantis' Strategy:", ["Always Cooperate", "Always Defect", "Tit-for-Tat", "Grim Trigger", "Forgiving", "Mixed Strategies"])

def get_strategy_choice(strategy, history, player):
    if strategy == "Always Cooperate":
        return "Cooperate"
    elif strategy == "Always Defect":
        return "Defect"
    elif strategy == "Tit-for-Tat":
        if not history:
            return "Cooperate"
        else:
            if player == "Wakanda":
                return history[-1]["Atlantis Choice"]
            else:
                return history[-1]["Wakanda Choice"]
    elif strategy == "Grim Trigger":
        if not history:
            return "Cooperate"
        else:
            if player == "Wakanda":
                if "Defect" in [h["Atlantis Choice"] for h in history]:
                    return "Defect"
                else:
                    return "Cooperate"
            else:
                if "Defect" in [h["Wakanda Choice"] for h in history]:
                    return "Defect"
                else:
                    return "Cooperate"
    elif strategy == "Forgiving":
        if not history:
            return "Cooperate"
        else:
            if player == "Wakanda":
                if history[-1]["Atlantis Choice"] == "Defect" and len(history) > 1 and history[-2]["Atlantis Choice"] == "Defect":
                    return "Defect"
                else:
                    return "Cooperate"
            else:
                if history[-1]["Wakanda Choice"] == "Defect" and len(history) > 1 and history[-2]["Wakanda Choice"] == "Defect":
                    return "Defect"
                else:
                    return "Cooperate"
    else:
        import random
        return random.choice(["Cooperate", "Defect"])

if st.button("Start"):
    wakanda_results = []
    atlantis_results = []
    round_details = []
    history = []

    for round_num in range(rounds):
        wakanda_choice = get_strategy_choice(wakanda_strategy, history, "Wakanda")
        atlantis_choice = get_strategy_choice(atlantis_strategy, history, "Atlantis")

        outcome = payoff_matrix[(wakanda_choice, atlantis_choice)]
        wakanda_results.append(outcome["Wakanda"]["value"])
        atlantis_results.append(outcome["Atlantis"]["value"])

        round_details.append({
            "Round": round_num + 1,
            "Wakanda Choice": wakanda_choice,
            "Atlantis Choice": atlantis_choice,
            "Wakanda Value": outcome["Wakanda"]["value"],
            "Atlantis Value": outcome["Atlantis"]["value"],
            "Wakanda Description": outcome["Wakanda"]["description"],
            "Atlantis Description": outcome["Atlantis"]["description"]
        })
        history.append(round_details[-1])

    st.subheader("Round-by-Round Results:")
    st.dataframe(pd.DataFrame(round_details), width = 1500)

    st.subheader("Overall Results:")
    st.write(f"Wakanda's Total Value: {sum(wakanda_results)}")
    st.write(f"Atlantis' Total Value: {sum(atlantis_results)}")

    st.subheader("Outcome Visualization (Stacked Area Chart):")

    cumulative_wakanda = [sum(wakanda_results[:i+1]) for i in range(len(wakanda_results))]
    cumulative_atlantis = [sum(atlantis_results[:i+1]) for i in range(len(atlantis_results))]

    fig = go.Figure()
    fig.add_trace(go.Scatter(y=cumulative_wakanda, name='Wakanda', fill='tozeroy'))
    fig.add_trace(go.Scatter(y=cumulative_atlantis, name='Atlantis', fill='tozeroy'))
    st.plotly_chart(fig)

st.write(f"The conflict will be resolved for {rounds} round(s).")