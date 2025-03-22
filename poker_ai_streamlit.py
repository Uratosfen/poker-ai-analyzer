import streamlit as st
import openai
import json

# === Налаштування API ===
openai.api_key = st.secrets.get("OPENAI_API_KEY")

# === Інтерфейс ===
st.title("🧠 Poker AI Помічник")
st.markdown("Завантаж свою стратегію і роздачі — отримай аналіз з GPT")

# === Завантаження файлів ===
strategy_file = st.file_uploader("📄 Завантаж файл стратегії (JSON)", type=["json"])
hands_file = st.file_uploader("🃏 Завантаж файл роздач (TXT)", type=["txt"])

if strategy_file and hands_file:
    strategy_data = json.load(strategy_file)
    strategy_text = json.dumps(strategy_data, indent=2)
    hands_text = hands_file.read().decode("utf-8")
    hands = hands_text.strip().split("\n\n")

    st.success("✅ Файли завантажені. Починаємо аналіз...")

    for i, hand in enumerate(hands):
        if not hand.strip():
            continue

        st.subheader(f"Роздача {i+1}")
        st.code(hand, language="text")

        with st.spinner("Аналізуємо..."):
            prompt = f"""
            Analyze the following poker hand based on the player's strategy below.

            Player's Strategy:
            {strategy_text}

            Poker Hand:
            {hand}

            Identify any deviations from the strategy, label them as 'mistakes', and suggest better lines.
            """

            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a professional poker coach."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                )
                analysis = response.choices[0].message["content"]
                st.markdown(f"**Аналіз:**\n\n{analysis}")
            except Exception as e:
                st.error(f"❌ Помилка аналізу: {e}")
else:
    st.info("⬆️ Завантаж обидва файли для початку аналізу.")