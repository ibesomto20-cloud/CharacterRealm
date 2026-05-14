import streamlit as st
import pandas as pd
from datetime import datetime
from contract_utils import ContractUtils
from character_utils import CharacterMemory

st.set_page_config(page_title="CharacterRealm", page_icon="🌌", layout="wide")

st.title("🌌 CharacterRealm")
st.markdown("**Persistent Decentralized AI Characters on 0G**")

if "contracts" not in st.session_state:
    st.session_state.contracts = ContractUtils()
    st.session_state.memory = CharacterMemory()
    st.session_state.characters = []
    st.session_state.chat_history = []

contracts = st.session_state.contracts
memory = st.session_state.memory

tab1, tab2, tab3, tab4, tab5 = st.tabs(["🌟 Create Character", "💬 Live Chat", "📜 My Characters", "🧠 Memory Journal", "📈 Evolution Timeline"])

# ====================== CREATE CHARACTER ======================
with tab1:
    st.subheader("Create a New Persistent AI Character")

    name = st.text_input("Character Name", placeholder="Luna Starweaver")
    personality = st.text_area("Personality & Traits",
                               placeholder="Sassy, curious, loves memes, slightly chaotic good...", height=100)
    backstory = st.text_area("Backstory / Lore",
                             placeholder="Born in a forgotten AI server farm during the 2025 bull run...", height=100)

    if st.button("🌌 Mint Character on 0G Chain", type="primary"):
        if name and personality and backstory:
            with st.spinner("Minting on-chain identity..."):
                try:
                    tx_function = contracts.get_character_contract().functions.createCharacter(
                        name.strip(), personality.strip(), backstory.strip()
                    )
                    _, tx_hash = contracts.send_transaction(tx_function)
                    st.code(tx_hash)

                    # For demo, create local object
                    char_id = len(st.session_state.characters) + 1
                    new_char = {
                        "id": char_id,
                        "name": name,
                        "personality": personality,
                        "backstory": backstory,
                        "created": datetime.now().strftime("%Y-%m-%d %H:%M")
                    }
                    st.session_state.characters.append(new_char)

                    st.success(f"🎉 {name} has been minted successfully!")
                    st.info(f"Character ID: #{char_id}")
                except Exception as e:
                    st.error(f"Failed to mint: {str(e)}")
        else:
            st.warning("Please fill all fields")

# ====================== CHAT INTERFACE ======================
with tab2:
    st.subheader("💬 Chat with Your Characters")
    if not st.session_state.characters:
        st.info("Create a character first in the Create Character tab.")
    else:
        char_list = [f"#{c['id']} — {c['name']}" for c in st.session_state.characters]
        selected = st.selectbox("Choose Character", char_list)
        char = st.session_state.characters[char_list.index(selected)]

        st.caption(f"Personality: {char['personality'][:100]}...")

        # Chat
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.write(f"**You:** {msg['content']}")
            else:
                st.write(f"**{char['name']}:** {msg['content']}")

        user_input = st.text_input("Send message to your character...", key="chat_input")
        if st.button("Send", type="primary"):
            if user_input.strip():
                st.session_state.chat_history.append({"role": "user", "content": user_input.strip()})

                # Generate smart response using Qwen3.6 API
                response = memory.generate_grok_response(char, user_input.strip())

                st.session_state.chat_history.append({"role": "character", "content": response})

                # Save conversation to persistent memory
                memory.save_memory(char["id"], f"User: {user_input} | {char['name']}: {response}")

                st.rerun()
# ====================== MY CHARACTERS ======================
with tab3:
    st.subheader("📜 My Characters")
    if st.session_state.characters:
        for char in st.session_state.characters:
            mem_count = len(memory.get_memories(char["id"]))
            with st.expander(f"#{char['id']} — {char['name']}"):
                st.write(f"**Personality:** {char['personality']}")
                st.write(f"**Backstory:** {char['backstory']}")
                st.metric("Memories Stored", mem_count)
                st.caption(f"Created: {char['created']}")
    else:
        st.info("You haven't created any characters yet.")

# ====================== MEMORY JOURNAL ======================
with tab4:
    st.subheader("🧠 Character Memory Journal")

    if not st.session_state.characters:
        st.info("Create a character first.")
    else:
        char_list = [f"#{c['id']} — {c['name']}" for c in st.session_state.characters]
        selected = st.selectbox("Select Character", char_list, key="memory_select")

        char = st.session_state.characters[char_list.index(selected)]
        memories = memory.get_memories(char["id"])

        if memories:
            st.metric("Total Memories", len(memories))
            st.caption("☁️ Memories auto-sync to 0G decentralized storage")

            relationship = memory.get_relationship_state(char["id"])
            extra_context = f"""
            Relationship stage: {relationship['stage']}
            Bond score: {relationship['score']}
            Adjust tone accordingly.
            """

            st.write("### ❤️ Relationship Meter")

            st.progress(relationship["score"] / 100)

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Bond Score", relationship["score"])
            with col2:
                st.metric("Stage", relationship["stage"])

            for mem in reversed(memories[-20:]):
                with st.expander(mem["timestamp"]):
                    st.write(mem["content"])
        else:
            st.info("No memories yet.")

# ====================== EVOLUTION TIMELINE ======================
with tab5:
    st.subheader("📈 Character Evolution Timeline")

    if not st.session_state.characters:
        st.info("Create a character first.")
    else:
        import pandas as pd

        char_list = [f"#{c['id']} — {c['name']}" for c in st.session_state.characters]
        selected = st.selectbox("Select Character", char_list, key="timeline_select")

        char = st.session_state.characters[char_list.index(selected)]

        timeline = memory.get_evolution_timeline(char["id"])
        memories = memory.get_memories(char["id"])

        if timeline:
            st.write("### Timeline Events")

            for event in timeline:
                st.markdown(f"**{event['time']}**")
                st.write(f"➡️ {event['event']}")
                st.divider()

        if memories:
            st.write("### 📊 Relationship Growth")

            scores = [
                {"Interaction": i + 1, "Score": min((i + 1) * 5, 100)}
                for i in range(len(memories))
            ]

            df = pd.DataFrame(scores)
            st.line_chart(df.set_index("Interaction"))

st.caption("CharacterRealm • 0G APAC Hackathon 2026 • Track 4")