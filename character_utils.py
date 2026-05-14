import os
import json
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI
from og_sync import OGSync

load_dotenv()


class CharacterMemory:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_dir = os.path.join(self.base_dir, "data", "characters")
        os.makedirs(self.data_dir, exist_ok=True)

        # Initialize LLM
        self.client = OpenAI(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1"
        )
        self.use_ai = True

    def save_memory(self, character_id: int, memory_text: str):
        try:
            filename = os.path.join(self.data_dir, f"char_{character_id}_memories.json")
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    memories = json.load(f)
            except:
                memories = []

            memories.append({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "content": memory_text
            })

            with open(filename, "w", encoding="utf-8") as f:
                json.dump(memories, f, indent=2)
            sync = OGSync()
            synced, result = sync.upload_file(filename)

            return synced
        except:
            return False

    def get_memories(self, character_id: int):
        try:
            filename = os.path.join(self.data_dir, f"char_{character_id}_memories.json")
            with open(filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []

    def generate_grok_response(self, character, user_input):
        """Use Arcee Trinity Large Preview (free model)"""
        if not self.use_ai:
            return f"*thinks* As {character['name']}, I find that fascinating..."

        try:
            past_memories = self.get_memories(character["id"])
            recent_context = "\n".join([m["content"][:120] for m in past_memories[-6:]])

            response = self.client.chat.completions.create(
                model="openrouter/free",  # Free & strong model
                messages=[
                    {"role": "system", "content": f"""
You are {character['name']}, a living, autonomous AI character with deep memory and personality.

Core Personality: {character['personality']}
Backstory: {character['backstory']}

Recent memories from previous conversations:
{recent_context}

Rules:
- Always stay in character. Never break role.
- Be natural, emotional, and engaging.
- Reference past conversations when relevant.
- Show personality in every response.
- Keep responses 2-4 sentences max unless asked for more.
- Use contractions and natural speech.
                    """},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.88,
                max_tokens=200,
                top_p=0.95
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"API error: {e}")
            return f"*smiles* That's an interesting thought. Tell me more..."

    def get_relationship_state(self, character_id: int):
        memories = self.get_memories(character_id)

        score = min(len(memories) * 5, 100)

        if score <= 20:
            stage = "Stranger"
        elif score <= 40:
            stage = "Acquaintance"
        elif score <= 60:
            stage = "Friend"
        elif score <= 80:
            stage = "Trusted Ally"
        else:
            stage = "Soulmate"

        return {
            "score": score,
            "stage": stage
        }

    def get_evolution_timeline(self, character_id: int):
        memories = self.get_memories(character_id)
        timeline = []

        if not memories:
            return timeline

        # Character created
        first_time = memories[0]["timestamp"]
        timeline.append({
            "time": first_time,
            "event": "Character began its journey"
        })

        # Memory milestones
        for idx, mem in enumerate(memories):
            if idx == 0:
                timeline.append({
                    "time": mem["timestamp"],
                    "event": "First conversation remembered"
                })

            if idx == 4:
                timeline.append({
                    "time": mem["timestamp"],
                    "event": "Became Acquaintance"
                })

            if idx == 9:
                timeline.append({
                    "time": mem["timestamp"],
                    "event": "Became Friend"
                })

            if idx == 15:
                timeline.append({
                    "time": mem["timestamp"],
                    "event": "Became Trusted Ally"
                })

            if idx == 20:
                timeline.append({
                    "time": mem["timestamp"],
                    "event": "Reached Soulmate stage"
                })

        return timeline