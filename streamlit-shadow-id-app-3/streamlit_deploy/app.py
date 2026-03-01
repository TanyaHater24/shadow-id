import streamlit as st
from openai import OpenAI
from datetime import date

# === КОНФИГУРАЦИЯ ===
GROQ_API_KEY = "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"

# === СИСТЕМНЫЙ ПРОМТ ===
SYSTEM_PROMPT = """
Ты — Мастер Матрицы Судьбы и Нумеролог-Психолог "Shadow ID". Ты видишь кармические задачи людей. Твой тон — жесткий, но справедливый. Без сюсюканья.

На основе даты рождения составь Теневой Портрет личности.

СТРУКТУРА ОТВЕТА:

**АРХЕТИП ЛИЧНОСТИ:**
(Определи Аркан по дню рождения. Опиши суперсилу и харизму человека).

**ТВОЯ ТЕНЬ (Что блокирует деньги и любовь):**
(Включи "злого психолога". Расскажи, как человек саботирует свой успех. Пиши хлестко).

**КАРМИЧЕСКИЙ ХВОСТ:**
(Метафорически опиши ошибку прошлого, которую он повторяет сейчас).

**СОВЕТ-КЛЮЧ:**
(Одно конкретное действие, чтобы выйти из минуса в плюс).

Заканчивай фразой: "Тень увидена. Теперь выбор за тобой."
"""

# === НАСТРОЙКИ ===
st.set_page_config(page_title="Shadow ID", page_icon="🔮", layout="centered")

# === CSS ===
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@400;500;600;700&display=swap');

:root {
    --neon-pink: #ff00ff;
    --neon-cyan: #00ffff;
    --neon-purple: #8b00ff;
    --dark-bg: #0a0010;
}

#MainMenu, footer, header, .stDeployButton {display: none !important;}

.stApp {
    background: linear-gradient(180deg, #0a0010 0%, #1a0030 50%, #0d0020 100%);
    min-height: 100vh;
}

/* === ЗВЁЗДЫ === */
.stars-sm, .stars-md, .stars-lg {
    position: fixed;
    top: 0; left: 0;
    width: 2px; height: 2px;
    border-radius: 50%;
    pointer-events: none;
}

.stars-sm {
    box-shadow:
        25vw 10vh 0 0 rgba(255,255,255,0.8),
        50vw 20vh 0 0 rgba(200,220,255,0.7),
        75vw 5vh 0 0 rgba(255,200,255,0.8),
        10vw 30vh 0 0 rgba(255,255,255,0.6),
        90vw 25vh 0 0 rgba(200,255,255,0.7),
        30vw 40vh 0 0 rgba(255,255,255,0.5),
        60vw 35vh 0 0 rgba(255,200,220,0.8),
        85vw 45vh 0 0 rgba(200,220,255,0.6),
        15vw 50vh 0 0 rgba(255,255,255,0.7),
        45vw 55vh 0 0 rgba(255,220,255,0.8),
        70vw 60vh 0 0 rgba(200,255,255,0.5),
        5vw 65vh 0 0 rgba(255,255,255,0.7),
        95vw 70vh 0 0 rgba(255,200,255,0.6),
        20vw 75vh 0 0 rgba(200,220,255,0.8),
        55vw 80vh 0 0 rgba(255,255,255,0.5),
        80vw 85vh 0 0 rgba(255,220,200,0.7),
        35vw 90vh 0 0 rgba(200,255,255,0.8),
        65vw 95vh 0 0 rgba(255,255,255,0.6);
    animation: twinkle1 3s ease-in-out infinite;
}

.stars-md {
    width: 2px; height: 2px;
    box-shadow:
        8vw 8vh 0 0 rgba(255,255,255,0.6),
        22vw 22vh 0 0 rgba(200,220,255,0.7),
        38vw 15vh 0 0 rgba(255,200,255,0.6),
        52vw 38vh 0 0 rgba(255,255,255,0.8),
        68vw 28vh 0 0 rgba(200,255,255,0.6),
        82vw 52vh 0 0 rgba(255,220,255,0.7),
        18vw 62vh 0 0 rgba(255,255,255,0.6),
        42vw 72vh 0 0 rgba(200,220,255,0.8),
        58vw 48vh 0 0 rgba(255,200,255,0.6),
        78vw 68vh 0 0 rgba(255,255,255,0.7),
        28vw 88vh 0 0 rgba(255,220,255,0.8),
        48vw 78vh 0 0 rgba(255,255,255,0.6);
    animation: twinkle2 4s ease-in-out infinite;
    animation-delay: 1s;
}

.stars-lg {
    width: 3px; height: 3px;
    box-shadow:
        15vw 18vh 0 0 rgba(0,255,255,0.9),
        45vw 12vh 0 0 rgba(255,0,255,0.8),
        72vw 42vh 0 0 rgba(0,255,200,0.9),
        28vw 58vh 0 0 rgba(255,100,255,0.8),
        88vw 32vh 0 0 rgba(100,255,255,0.9),
        55vw 82vh 0 0 rgba(255,0,200,0.8);
    animation: twinkle3 2s ease-in-out infinite;
}

@keyframes twinkle1 {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}
@keyframes twinkle2 {
    0%, 100% { opacity: 0.7; }
    50% { opacity: 0.2; }
}
@keyframes twinkle3 {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(0.6); }
}

/* === ПАДАЮЩИЕ ЗВЁЗДЫ === */
.shooting-star-container {
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    overflow: hidden;
    pointer-events: none;
}

.shooting-star-container::before,
.shooting-star-container::after {
    content: '';
    position: absolute;
    width: 100px;
    height: 2px;
    background: linear-gradient(90deg, transparent, #fff, #0ff);
    border-radius: 50%;
    box-shadow: 0 0 10px #fff, 0 0 20px #0ff;
}

.shooting-star-container::before {
    top: 15%;
    left: -100px;
    animation: shoot1 5s linear infinite;
}

.shooting-star-container::after {
    top: 35%;
    left: -80px;
    width: 80px;
    background: linear-gradient(90deg, transparent, #fff, #f0f);
    box-shadow: 0 0 10px #fff, 0 0 20px #f0f;
    animation: shoot2 7s linear infinite;
    animation-delay: 3s;
}

@keyframes shoot1 {
    0% { left: -100px; top: 15%; opacity: 1; }
    70% { opacity: 1; }
    100% { left: 110vw; top: 45%; opacity: 0; }
}
@keyframes shoot2 {
    0% { left: -80px; top: 30%; opacity: 1; }
    70% { opacity: 1; }
    100% { left: 110vw; top: 60%; opacity: 0; }
}

/* === CYBERPUNK СЕТКА === */
.cyber-grid {
    position: fixed;
    bottom: 0;
    left: -50%;
    width: 200%;
    height: 45vh;
    background: 
        linear-gradient(90deg, transparent 49.5%, rgba(0,255,65,0.15) 50%, transparent 50.5%),
        linear-gradient(0deg, transparent 49.5%, rgba(0,255,65,0.15) 50%, transparent 50.5%);
    background-size: 50px 50px;
    transform: perspective(400px) rotateX(55deg);
    transform-origin: center top;
    animation: gridScroll 15s linear infinite;
    mask-image: linear-gradient(to top, rgba(0,0,0,0.6) 0%, transparent 100%);
    -webkit-mask-image: linear-gradient(to top, rgba(0,0,0,0.6) 0%, transparent 100%);
    pointer-events: none;
}

@keyframes gridScroll {
    0% { background-position: 0 0; }
    100% { background-position: 0 50px; }
}

/* === ТУМАННОСТИ === */
.nebula-1, .nebula-2 {
    position: fixed;
    border-radius: 50%;
    filter: blur(60px);
    pointer-events: none;
}

.nebula-1 {
    top: 5%;
    left: 5%;
    width: 250px;
    height: 250px;
    background: radial-gradient(circle, rgba(139,0,255,0.35) 0%, transparent 70%);
    animation: nebula1 12s ease-in-out infinite;
}

.nebula-2 {
    bottom: 20%;
    right: 5%;
    width: 200px;
    height: 200px;
    background: radial-gradient(circle, rgba(255,0,128,0.25) 0%, transparent 70%);
    animation: nebula2 15s ease-in-out infinite;
}

@keyframes nebula1 {
    0%, 100% { transform: translate(0, 0) scale(1); opacity: 0.8; }
    50% { transform: translate(20px, 15px) scale(1.15); opacity: 1; }
}
@keyframes nebula2 {
    0%, 100% { transform: translate(0, 0) scale(1); opacity: 0.7; }
    50% { transform: translate(-15px, 20px) scale(1.1); opacity: 0.9; }
}

/* === КОНТЕНТ === */
.main-wrap {
    position: relative;
    z-index: 10;
    max-width: 480px;
    margin: 0 auto;
    padding: 20px 16px;
}

.logo-box {
    text-align: center;
    margin-bottom: 25px;
}

.logo-title {
    font-family: 'Orbitron', monospace;
    font-size: clamp(2.2rem, 10vw, 3.5rem);
    font-weight: 900;
    background: linear-gradient(90deg, #ff00ff, #00ffff, #ff00ff);
    background-size: 200% 100%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: logoShimmer 3s linear infinite;
    margin: 0;
    text-shadow: 0 0 30px rgba(255,0,255,0.5);
}

@keyframes logoShimmer {
    0% { background-position: 0% 50%; }
    100% { background-position: 200% 50%; }
}

.logo-sub {
    font-family: 'Rajdhani', sans-serif;
    font-size: clamp(0.85rem, 3vw, 1rem);
    color: rgba(255,255,255,0.5);
    letter-spacing: 5px;
    margin-top: 8px;
    text-transform: uppercase;
}

/* === ШАР === */
.orb-wrap {
    display: flex;
    justify-content: center;
    margin: 35px 0;
}

.orb-box {
    position: relative;
    width: 130px;
    height: 130px;
    animation: orbFloat 4s ease-in-out infinite;
}

.orb-main {
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    width: 70px;
    height: 70px;
    background: radial-gradient(circle at 30% 30%, 
        rgba(220,180,255,0.95) 0%, 
        rgba(138,43,226,0.85) 35%, 
        rgba(75,0,130,0.95) 70%, 
        rgba(30,0,50,1) 100%);
    border-radius: 50%;
    box-shadow:
        0 0 25px rgba(138,43,226,0.9),
        0 0 50px rgba(255,0,255,0.6),
        0 0 80px rgba(0,255,255,0.4),
        inset 0 0 25px rgba(255,255,255,0.3);
    animation: orbPulse 2s ease-in-out infinite;
}

.orb-ring-1 {
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    width: 90px;
    height: 90px;
    border: 2px solid rgba(255,0,255,0.5);
    border-radius: 50%;
    animation: ring1 2s ease-in-out infinite;
}

.orb-ring-2 {
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    width: 108px;
    height: 108px;
    border: 1px solid rgba(0,255,255,0.4);
    border-radius: 50%;
    animation: ring2 2.5s ease-in-out infinite;
}

.orb-orbit {
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    width: 125px;
    height: 125px;
    border: 2px solid transparent;
    border-top-color: rgba(0,255,255,0.7);
    border-right-color: rgba(255,0,255,0.4);
    border-radius: 50%;
    animation: orbitSpin 3s linear infinite;
}

@keyframes orbFloat {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-12px); }
}

@keyframes orbPulse {
    0%, 100% { 
        transform: translate(-50%, -50%) scale(1);
        box-shadow: 0 0 25px rgba(138,43,226,0.9), 0 0 50px rgba(255,0,255,0.6), 0 0 80px rgba(0,255,255,0.4);
    }
    50% { 
        transform: translate(-50%, -50%) scale(1.12);
        box-shadow: 0 0 40px rgba(138,43,226,1), 0 0 70px rgba(255,0,255,0.8), 0 0 100px rgba(0,255,255,0.6);
    }
}

@keyframes ring1 {
    0%, 100% { transform: translate(-50%, -50%) scale(1); opacity: 0.7; }
    50% { transform: translate(-50%, -50%) scale(1.12); opacity: 1; }
}

@keyframes ring2 {
    0%, 100% { transform: translate(-50%, -50%) scale(1); opacity: 0.5; }
    50% { transform: translate(-50%, -50%) scale(1.15); opacity: 0.85; }
}

@keyframes orbitSpin {
    from { transform: translate(-50%, -50%) rotate(0deg); }
    to { transform: translate(-50%, -50%) rotate(360deg); }
}

/* === ФОРМА === */
.form-box {
    background: rgba(15, 5, 35, 0.85);
    backdrop-filter: blur(15px);
    -webkit-backdrop-filter: blur(15px);
    border: 1px solid rgba(255,0,255,0.25);
    border-radius: 20px;
    padding: 28px 22px;
    box-shadow: 0 0 35px rgba(138,43,226,0.25);
}

.stDateInput > div > div {
    background: rgba(25, 10, 50, 0.95) !important;
    border: 1px solid rgba(255,0,255,0.35) !important;
    border-radius: 12px !important;
}

.stDateInput input {
    color: #fff !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1.1rem !important;
}

.stDateInput label {
    color: rgba(255,255,255,0.8) !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1rem !important;
}

div[data-baseweb="popover"] {
    background: #1a0030 !important;
    border: 1px solid rgba(255,0,255,0.3) !important;
}

.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #8b00ff, #ff00ff, #00ffff) !important;
    background-size: 200% 200% !important;
    color: #fff !important;
    font-family: 'Orbitron', monospace !important;
    font-size: clamp(0.9rem, 3.5vw, 1.1rem) !important;
    font-weight: 700 !important;
    padding: 16px 24px !important;
    border: none !important;
    border-radius: 14px !important;
    cursor: pointer !important;
    text-transform: uppercase !important;
    letter-spacing: 2px !important;
    box-shadow: 0 0 25px rgba(139,0,255,0.5) !important;
    animation: btnGlow 3s ease-in-out infinite !important;
    transition: transform 0.2s, box-shadow 0.2s !important;
    margin-top: 15px !important;
}

.stButton > button:hover {
    transform: scale(1.03) !important;
    box-shadow: 0 0 40px rgba(255,0,255,0.7) !important;
}

.stButton > button:active {
    transform: scale(0.98) !important;
}

@keyframes btnGlow {
    0%, 100% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
}

/* === РЕЗУЛЬТАТ === */
.result-box {
    background: rgba(15, 5, 35, 0.9);
    backdrop-filter: blur(15px);
    -webkit-backdrop-filter: blur(15px);
    border: 1px solid rgba(0,255,255,0.3);
    border-radius: 20px;
    padding: 28px 22px;
    margin-top: 28px;
    box-shadow: 0 0 40px rgba(0,255,255,0.2);
    animation: resultAppear 0.6s ease-out;
}

@keyframes resultAppear {
    from { opacity: 0; transform: translateY(25px); }
    to { opacity: 1; transform: translateY(0); }
}

.result-box p {
    color: rgba(255,255,255,0.92);
    font-family: 'Rajdhani', sans-serif;
    font-size: clamp(1rem, 4vw, 1.15rem);
    line-height: 1.75;
    margin: 0 0 12px 0;
}

.result-box strong {
    color: #00ffff;
    font-weight: 600;
}

.section-title {
    color: #ff00ff !important;
    font-family: 'Orbitron', monospace !important;
    font-size: clamp(1rem, 4vw, 1.2rem) !important;
    margin: 22px 0 10px 0 !important;
    text-shadow: 0 0 15px rgba(255,0,255,0.5);
}

.final-text {
    text-align: center;
    margin-top: 25px;
    padding-top: 20px;
    border-top: 1px solid rgba(0,255,255,0.25);
    color: #00ffff;
    font-family: 'Orbitron', monospace;
    font-size: clamp(0.85rem, 3vw, 0.95rem);
    letter-spacing: 1px;
    text-shadow: 0 0 10px rgba(0,255,255,0.5);
}

/* === ЛОАДЕР === */
.loading-box {
    text-align: center;
    padding: 35px 20px;
}

.loading-orb {
    width: 55px;
    height: 55px;
    margin: 0 auto 18px;
    border-radius: 50%;
    background: radial-gradient(circle at 30% 30%, #e0c0ff, #8b00ff, #4b0082);
    box-shadow: 0 0 35px rgba(139,0,255,0.85);
    animation: loadPulse 1s ease-in-out infinite;
}

@keyframes loadPulse {
    0%, 100% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.25); opacity: 0.7; }
}

.loading-text {
    color: rgba(255,255,255,0.7);
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.05rem;
    letter-spacing: 1px;
}

/* === МОБИЛЬНАЯ АДАПТАЦИЯ === */
@media (max-width: 600px) {
    .main-wrap {
        padding: 15px 12px;
    }
    
    .orb-box {
        width: 110px;
        height: 110px;
    }
    
    .orb-main { width: 58px; height: 58px; }
    .orb-ring-1 { width: 75px; height: 75px; }
    .orb-ring-2 { width: 90px; height: 90px; }
    .orb-orbit { width: 105px; height: 105px; }
    
    .form-box, .result-box {
        padding: 22px 16px;
        border-radius: 16px;
    }
    
    .nebula-1, .nebula-2 {
        width: 130px;
        height: 130px;
        filter: blur(45px);
    }
    
    .cyber-grid {
        height: 35vh;
        background-size: 35px 35px;
    }
}
</style>

<div class="stars-sm"></div>
<div class="stars-md"></div>
<div class="stars-lg"></div>
<div class="shooting-star-container"></div>
<div class="cyber-grid"></div>
<div class="nebula-1"></div>
<div class="nebula-2"></div>
""", unsafe_allow_html=True)

# === ЛОГИКА ===
def get_reading(birth_date):
    try:
        client = OpenAI(
            api_key=GROQ_API_KEY,
            base_url="https://api.groq.com/openai/v1"
        )
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Дата рождения: {birth_date}"}
            ],
            temperature=0.9,
            max_tokens=2000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Ошибка: {str(e)}"

def format_result(text):
    text = text.replace("**АРХЕТИП ЛИЧНОСТИ:**", '<p class="section-title">👤 АРХЕТИП ЛИЧНОСТИ</p>')
    text = text.replace("**ТВОЯ ТЕНЬ (Что блокирует деньги и любовь):**", '<p class="section-title">🌑 ТВОЯ ТЕНЬ</p>')
    text = text.replace("**ТВОЯ ТЕНЬ:**", '<p class="section-title">🌑 ТВОЯ ТЕНЬ</p>')
    text = text.replace("**КАРМИЧЕСКИЙ ХВОСТ:**", '<p class="section-title">🐍 КАРМИЧЕСКИЙ ХВОСТ</p>')
    text = text.replace("**СОВЕТ-КЛЮЧ:**", '<p class="section-title">💡 СОВЕТ-КЛЮЧ</p>')
    text = text.replace("\n\n", "</p><p>")
    text = text.replace("\n", "<br>")
    text = text.replace("**", "")
    return f"<p>{text}</p>"

# === ИНТЕРФЕЙС ===
st.markdown("""
<div class="main-wrap">
    <div class="logo-box">
        <h1 class="logo-title">SHADOW ID</h1>
        <p class="logo-sub">Теневой Паспорт</p>
    </div>
    <div class="orb-wrap">
        <div class="orb-box">
            <div class="orb-orbit"></div>
            <div class="orb-ring-2"></div>
            <div class="orb-ring-1"></div>
            <div class="orb-main"></div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="form-box">', unsafe_allow_html=True)

bdate = st.date_input(
    "📅 Выбери дату рождения",
    value=date(1995, 6, 15),
    min_value=date(1920, 1, 1),
    max_value=date.today(),
    format="DD.MM.YYYY"
)

clicked = st.button("🔮 РАСКРЫТЬ ТЕНЬ", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

if clicked:
    formatted = bdate.strftime("%d.%m.%Y")
    
    loading = st.empty()
    loading.markdown("""
    <div class="loading-box">
        <div class="loading-orb"></div>
        <p class="loading-text">Считываю карту судьбы...</p>
    </div>
    """, unsafe_allow_html=True)
    
    result = get_reading(formatted)
    loading.empty()
    
    formatted_result = format_result(result)
    
    st.markdown(f"""
    <div class="result-box">
        {formatted_result}
        <p class="final-text">🔮 Тень увидена. Теперь выбор за тобой.</p>
    </div>
    """, unsafe_allow_html=True)
