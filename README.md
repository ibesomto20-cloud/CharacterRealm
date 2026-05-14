# CharacterRealm

CharacterRealm is a decentralized AI character platform built on 0G Labs, where users can create persistent AI personalities that evolve, remember interactions, and maintain sovereign identity across sessions.

Unlike traditional chatbots, CharacterRealm characters develop relationships, preserve memories, and synchronize their identity and state using decentralized infrastructure.

---

## 🌌 Vision

Most AI characters today are temporary. They lose context, forget users, and reset when apps restart.

CharacterRealm introduces:

- Persistent AI identities
- Long-term memory
- Character evolution over time
- Relationship tracking
- Decentralized synchronization via 0G

This creates truly living digital companions.

---

## ✨ Core Features

### 🎭 Create Unique AI Characters

Users can create characters with:

- Name
- Personality
- Background story
- Custom identity

Each character becomes an independent AI persona.

---

## 🧠 Persistent Memory Journal

Every interaction is stored in a character-specific memory vault.

Characters remember:

- previous conversations
- user preferences
- shared experiences
- important context

This allows ongoing, evolving interactions.

---

## ❤️ Relationship Meter

Each character tracks its bond with the user.

Stages include:

- Stranger
- Acquaintance
- Friend
- Trusted Ally
- Soulmate

The relationship strengthens through continued interaction.

---

## 📈 Character Evolution Timeline

Characters develop over time.

The timeline records milestones such as:

- first conversation
- memory growth
- relationship changes
- key interaction events

This creates a visible life history for each AI character.

---

## ☁️ 0G Memory Sync

Character memories are synchronized to decentralized storage on 0G.

This ensures:

- portability
- persistence across devices
- resilience against local file loss
- sovereign ownership of AI state

---

## 🏗 Architecture

```text
User
 ↓
Create Character
 ↓
Chat with Character
 ↓
Store Memory Locally
 ↓
Sync Memory to 0G
 ↓
Track Relationship
 ↓
Build Evolution Timeline
```

---

## ⚙ Tech Stack

- Python
- OpenRouter LLM API
- OpenAI SDK
- 0G Storage
- Web3.py
- JSON local persistence
- dotenv
- requests

---

## 🚀 How It Works

### Character Creation

Users create AI characters with custom personalities.

Each character gets:

- unique ID
- local memory file
- decentralized backup capability

---

### Live Interaction

Users chat with characters in real time.

Character responses are generated using:

[OpenRouter API](https://openrouter.ai?utm_source=chatgpt.com)

with:

```python
model="openrouter/free"
```

---

### Memory Persistence

Each message is appended to the character’s memory vault:

```text
data/characters/char_{id}_memories.json
```

---

### Decentralized Sync

After memory updates:

1. local vault updates  
2. file syncs to 0G  
3. decentralized persistence achieved  

---

## 🔐 Why CharacterRealm Matters

CharacterRealm transforms AI companions into sovereign digital entities.

This enables:

- decentralized AI identity
- persistent companionship
- transferable character ownership
- user-controlled memory

---

## 📊 Current Features Implemented

✅ AI character creation  
✅ live chat  
✅ persistent memory  
✅ relationship meter  
✅ evolution timeline  
✅ decentralized 0G sync  
✅ memory journal  

---

## 🛣 Roadmap

Future upgrades:

- character trait mutation  
- multi-user shared characters  
- NFT-based character ownership  
- cross-device recovery  
- decentralized personality marketplace  
- emotional sentiment tracking  
- agent-to-agent interaction  
