import streamlit as st
from datetime import datetime
import os
import base64
import json
import streamlit.components.v1 as components

# ==========================
# CONFIG
# ==========================
st.set_page_config(
    page_title="H",
    page_icon="🎂",
    layout="wide"
)

# ==========================
# SESSION
# ==========================
if "login" not in st.session_state:
    st.session_state.login = False

# ========================== 
# CSS
# ==========================
st.markdown("""
<style>

.stApp{
    min-height:100vh;
    padding:18px 14px 24px;
    background:#000000;
    color:white;
}

.stTextInput input,
.stDateInput input{
    color:white !important;
    background:#101010 !important;
    border-radius:14px !important;
    border:1px solid rgba(255,255,255,0.12) !important;
    padding:14px !important;
}

.stTextInput label,
.stDateInput label{
    color:white !important;
    font-size:15px;
    margin-bottom:8px;
}

.stTextInput input::placeholder,
.stDateInput input::placeholder{
    color:rgba(255,255,255,0.55) !important;
}

.stDateInput svg{
    fill:white !important;
}

.stButton>button{
    background: linear-gradient(135deg, #ff4da6 0%, #ff7ab9 100%) !important;
    color:white !important;
    border:none !important;
    border-radius:18px;
    height:56px;
    width:100%;
    font-size:20px;
    font-weight:800;
    box-shadow:0 16px 35px rgba(255,77,166,0.22);
    transition: transform .25s ease, box-shadow .25s ease, opacity .25s ease;
}

.stButton>button:hover{
    transform: translateY(-1px) scale(1.02);
    box-shadow:0 20px 45px rgba(255,77,166,0.32);
    opacity:0.98;
}

/* Hilangkan menu streamlit */
#MainMenu{visibility:hidden;}
footer{visibility:hidden;}
header{visibility:hidden;}

.login-box{
    width:min(100%, 560px);
    max-width:560px;
    min-width:280px;
    margin:auto;
    margin-top:44px;
    position:relative;
    overflow:hidden;
    background:rgba(12, 12, 12, 0.95);
    border:1px solid rgba(255, 77, 166, 0.18);
    backdrop-filter: blur(14px);
    border-radius:28px;
    padding:36px 26px 38px;
}

.login-box::before{
    content: "";
    position:absolute;
    top:-50px;
    right:-50px;
    width:220px;
    height:220px;
    background: radial-gradient(circle, rgba(255,77,166,0.15) 0%, transparent 58%);
    border-radius:50%;
    pointer-events:none;
}

.login-box::after{
    content: "";
    position:absolute;
    bottom:-40px;
    left:-30px;
    width:160px;
    height:160px;
    background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 58%);
    border-radius:50%;
    pointer-events:none;
}

.login-badge{
    text-align:center;
    font-size:13px;
    color:#ff92cd;
    text-transform:uppercase;
    letter-spacing:1.2px;
    margin-bottom:18px;
}

.title{
    text-align:center;
    font-size:34px;
    color:white;
    font-weight:800;
    letter-spacing:0.6px;
    margin-bottom:10px;
}

.sub{
    text-align:center;
    color:#cccccc;
    margin-bottom:30px;
    line-height:1.8;
    font-size:16px;
}

.hint{
    text-align:center;
    color:#bbbbbb;
    font-size:14px;
    margin-bottom:28px;
    line-height:1.7;
    color:#66ff99;
}

@media(max-width:640px){
    .login-box{
        margin-top:28px;
        padding:24px 18px 28px;
    }
    .title{
        font-size:28px;
    }
    .sub{
        font-size:15px;
    }
}

</style>
""", unsafe_allow_html=True)

def image_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# ==========================
# LOGIN PAGE
# ==========================

if st.session_state.login is False:

    st.markdown(
        """
<div class="login-box">
    <div class="login-badge">✨ Kejutan Ulang Tahun Asya ✨</div>
    <div class="title">🎂 Happy Birthday</div>
    <div class="sub">Silakan login terlebih dahulu untuk masuk ke kejutan ulang tahun.</div>
    <div class="hint">Masukkan nama lengkap dan tanggal lahir dengan benar agar kamu bisa membuka kejutan spesial ini.</div>
    <div class="created-by" style="text-align:center; color:#ffb4d9; font-size:14px; margin-top:18px;">Created by THX</div>
</div>
        """,
        unsafe_allow_html=True,
    )

    nama = st.text_input(
        "Nama",
        placeholder="Masukkan Nama"
    )

    tanggal = st.date_input(
        "Tanggal Lahir",
        value=datetime(2026,1,1),
        min_value=datetime(1990,1,1),
        max_value=datetime(2030,12,31)
    )

    login = st.button(
        "Masuk",
        use_container_width=True
    )

    if login:

        nama_benar = "Artasya Salsabila Anggrahini"

        tanggal_benar = datetime(
            2007,
            7,
            13
        ).date()

        if nama.strip().lower() == nama_benar.lower() and tanggal == tanggal_benar:

            st.session_state.login = True
            st.rerun()

        else:

            st.error("Nama atau tanggal lahir salah.")

# ==========================
# BERHASIL LOGIN
# ==========================

else:

    folder = "images"
    gambar = []

    if os.path.exists(folder):
        for file in sorted(os.listdir(folder)):
            if file.lower().endswith(("jpg", "jpeg", "png", "webp")):
                gambar.append(
                    "data:image/jpeg;base64," +
                    image_to_base64(os.path.join(folder, file))
                )

    st.markdown("""
    <style>
    .count-title{
        text-align:center;
        font-size:55px;
        color:white;
        font-weight:bold;
        margin-top:30px;
    }
    .count-sub{
        text-align:center;
        color:#aaaaaa;
        font-size:22px;
        margin-bottom:40px;
    }
    </style>
    """, unsafe_allow_html=True)

    image_js = json.dumps(gambar)
    audio = ""

    if os.path.exists("assets/happybirthday.mp3"):
        with open("assets/happybirthday.mp3", "rb") as f:
            audio = base64.b64encode(f.read()).decode()

    components.html(
        """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
body {
    background: #000;
    color: white;
    margin: 0;
    font-family: Arial, sans-serif;
    overflow-x: hidden;
}
.wrapper {
    max-width: 1150px;
    margin: 0 auto;
    padding: 24px 16px 48px;
}
.section-title {
    text-align: center;
    font-size: 50px;
    font-weight: 800;
    margin-top: 20px;
    color: white;
    text-shadow: 0 0 25px rgba(255, 77, 166, 0.35);
}
.section-sub {
    text-align: center;
    color: #cccccc;
    font-size: 20px;
    margin: 12px auto 36px;
}
.timer {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 22px;
}
.box {
    width: 150px;
    height: 150px;
    background: #111;
    border-radius: 24px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    box-shadow: 0 0 30px rgba(255, 77, 166, 0.22);
}
.number {
    font-size: 50px;
    font-weight: 800;
    color: white;
}
.label {
    font-size: 18px;
    color: #ff77aa;
    margin-top: 8px;
}
.message {
    text-align: center;
    font-size: 22px;
    color: white;
    margin-top: 28px;
    animation: blink 2.5s infinite;
}
.slider {
    position: relative;
    z-index: 1;
    width: 90%;
    max-width: 900px;
    height: 520px;
    margin: 40px auto 0;
    border-radius: 24px;
    overflow: hidden;
    box-shadow: 0 0 44px rgba(255, 77, 166, 0.3);
}
.slider img {
    position: absolute;
    width: 100%;
    height: 100%;
    object-fit: cover;
    opacity: 0;
    transition: opacity 1s ease;
}
.slider img.active {
    opacity: 1;
}
.typing {
    margin-top: 36px;
    text-align: center;
    font-size: 24px;
    line-height: 1.7;
    color: #fff;
    text-shadow: 0 0 20px rgba(255,255,255,0.45);
    background: rgba(0, 0, 0, 0.35);
    padding: 18px 22px;
    border-radius: 20px;
    max-width: 900px;
    margin-left: auto;
    margin-right: auto;
    position: relative;
    z-index: 2;
    white-space: pre-wrap;
}
.floating {
    position: fixed;
    font-size: 28px;
    pointer-events: none;
    animation: floatUp linear infinite;
    opacity: 0.85;
    z-index: 2;
}
.star {
    position: fixed;
    color: white;
    font-size: 18px;
    animation: twinkle 2s infinite;
    pointer-events: none;
    z-index: 1;
}
.confetti {
    position: fixed;
    top: -20px;
    font-size: 22px;
    pointer-events: none;
    animation: confettiFall linear infinite;
    z-index: 3;
}
#letter {
    width: 90%;
    max-width: 900px;
    margin: 40px auto 0;
    padding: 28px;
    border-radius: 20px;
    background: rgba(255, 255, 255, 0.08);
    color: white;
    line-height: 1.9;
    font-size: 20px;
    display: none;
    backdrop-filter: blur(10px);
}
button {
    margin: 30px auto 0;
    display: block;
    padding: 15px 34px;
    font-size: 22px;
    background: #ff4da6;
    color: white;
    border: none;
    border-radius: 15px;
    cursor: pointer;
    box-shadow: 0 0 20px hotpink;
}
@keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}
@keyframes floatUp {
    0% { transform: translateY(100vh); opacity: 0; }
    20% { opacity: 1; }
    100% { transform: translateY(-20vh); opacity: 0; }
}
@keyframes twinkle {
    0% { opacity: 0.2; }
    50% { opacity: 1; }
    100% { opacity: 0.2; }
}
@keyframes confettiFall {
    0% { transform: translateY(-10vh) rotate(0deg); opacity: 1; }
    100% { transform: translateY(120vh) rotate(720deg); opacity: 0; }
}
canvas {
    position: fixed;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 0;
}
</style>
</head>
<body>
<audio autoplay loop controls style="display:none;">
<source src="data:audio/mp3;base64,{audio}" type="audio/mp3">
</audio>
<div class="wrapper">
    <div class="section-title">🎂 Happy Birthday Asya ❤️</div>
    <div class="section-sub">Countdown menuju 13 Juli 2026 WIB</div>
    <div class="timer">
        <div class="box"><div id="day" class="number">00</div><div class="label">Hari</div></div>
        <div class="box"><div id="hour" class="number">00</div><div class="label">Jam</div></div>
        <div class="box"><div id="minute" class="number">00</div><div class="label">Menit</div></div>
        <div class="box"><div id="second" class="number">00</div><div class="label">Detik</div></div>
    </div>
    <div class="message" id="count-message">💖 Waktu terus berjalan menuju hari spesialmu 💖</div>
    <div id="end-button-container" style="text-align:center; margin-top: 24px; display:none;">
        <button id="end-button">Buka Kejutan</button>
    </div>
</div>
<script>
const IMAGE_LIST = {image_js};
const target = new Date("2026-07-13T00:00:00+07:00").getTime();
const dayEl = document.getElementById("day");
const hourEl = document.getElementById("hour");
const minuteEl = document.getElementById("minute");
const secondEl = document.getElementById("second");
const countMessage = document.getElementById("count-message");
const endButtonContainer = document.getElementById("end-button-container");
const endButton = document.getElementById("end-button");

if (endButton) {
    endButton.addEventListener("click", showSurprise);
}

function pad(value) {
    return value.toString().padStart(2, "0");
}

function updateCountdown() {
    const now = Date.now();
    const distance = target - now;

    if (distance <= 0) {
        dayEl.innerText = "00";
        hourEl.innerText = "00";
        minuteEl.innerText = "00";
        secondEl.innerText = "00";
        countMessage.innerText = "🎉 Countdown selesai! Klik tombol untuk membuka kejutanmu.";
        endButtonContainer.style.display = "block";
        return;
    }

    const days = Math.floor(distance / (1000 * 60 * 60 * 24));
    const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((distance % (1000 * 60)) / 1000);

    dayEl.innerText = pad(days);
    hourEl.innerText = pad(hours);
    minuteEl.innerText = pad(minutes);
    secondEl.innerText = pad(seconds);
}

function showSurprise() {
    document.body.innerHTML = `
    <div class="wrapper">
        <div class="section-title">🎉 Selamat Ulang Tahun Asya 🎉</div>
        <div class="section-sub">Selamat ulang tahun! Klik tombol di bawah untuk membuka kejutanmu.</div>
        <div style="text-align:center; margin-top:32px;">
            <button id="prank-button" style="padding:18px 34px; font-size:22px; border-radius:16px; background:#ff4da6; color:#fff; border:none; box-shadow:0 0 30px rgba(255,77,166,0.4); cursor:pointer;">Klik di sini</button>
        </div>
        <div id="puzzle-box" style="display:none; text-align:center; margin-top:32px;">
            <div style="font-size:20px; color:#fff; margin-bottom:18px;">Selesaikan puzzle ini dulu:</div>
            <div style="font-size:34px; color:#ff88c4; margin-bottom:20px;">2 + 2 = ?</div>
            <input id="puzzle-answer" type="text" placeholder="Masukkan jawaban" style="width:80%; max-width:280px; padding:14px 16px; border-radius:14px; border:1px solid rgba(255,255,255,0.18); background:#111; color:#fff; font-size:18px; text-align:center;" />
            <br />
            <button id="puzzle-submit" style="margin-top:24px; padding:14px 32px; font-size:20px; border-radius:16px; background:#ff4da6; color:#fff; border:none; cursor:pointer;">Kirim Jawaban</button>
            <div id="puzzle-feedback" style="margin-top:18px; color:#ffb4d9; min-height:24px; font-size:16px;"></div>
        </div>
        <div id="final-content" style="display:none; margin-top:40px; position: relative; z-index: 2;">
            <div class="slider"></div>
            <div style="text-align:center; margin-top:22px;">
                <button id="surprise-button" style="padding:18px 34px; font-size:22px; border-radius:18px; background:#ff4da6; color:#fff; border:none; box-shadow:0 0 30px rgba(255,77,166,0.4); cursor:pointer;">Selamat ulang tahun! Klik tombol untuk membuka kejutanmu</button>
            </div>
            <div class="typing" id="typing"></div>
            <div id="letter" style="display:none; margin-top:30px;">
                <h2 align="center">❤️ Untuk Asya ❤️</h2>
                <p>
Happy Birthday Asya 🎉

Semoga di umur yang baru ini selalu diberikan kesehatan,

kebahagiaan, rezeki yang melimpah,

dimudahkan dalam setiap langkah,

semua impian tercapai,

dan selalu dikelilingi orang-orang yang menyayangimu.

Terima kasih sudah menjadi pribadi yang kuat,

baik, dan selalu membawa kebahagiaan bagi orang lain.

Semoga setiap doa yang dipanjatkan
dikabulkan oleh Allah SWT.

Enjoy your special day ❤️
                </p>
            </div>
        </div>
        <canvas id="firework"></canvas>
    </div>`;
    initSurprise();
}

function initSurprise() {
    const prankButton = document.getElementById("prank-button");
    const puzzleBox = document.getElementById("puzzle-box");
    const finalContent = document.getElementById("final-content");
    const puzzleAnswer = document.getElementById("puzzle-answer");
    const puzzleSubmit = document.getElementById("puzzle-submit");
    const puzzleFeedback = document.getElementById("puzzle-feedback");
    const slider = document.querySelector(".slider");

    let prankClicks = 0;
    const prankLabels = [
        "Klik di sini",
        "Beneran klik di sini",
        "Jangan lupa klik di sini",
        "Satu lagi dong klik di sini",
        "Terakhir klik di sini"
    ];

    prankButton.addEventListener("click", () => {
        prankClicks += 1;
        if (prankClicks < 5) {
            prankButton.innerText = prankLabels[prankClicks];
        } else {
            prankButton.style.display = "none";
            puzzleBox.style.display = "block";
        }
    });

    puzzleSubmit.addEventListener("click", () => {
        const answer = puzzleAnswer.value.trim();
        if (answer === "4" || answer.toLowerCase() === "empat") {
            puzzleFeedback.innerText = "Jawaban benar! Siap membuka kejutan...";
            setTimeout(() => {
                puzzleBox.style.display = "none";
                finalContent.style.display = "block";
                startSlideshow();
                startTyping();
                const surpriseButton = document.getElementById("surprise-button");
                surpriseButton.addEventListener("click", () => {
                    const letter = document.getElementById("letter");
                    const isOpen = letter.style.display === "block";
                    letter.style.display = isOpen ? "none" : "block";
                    surpriseButton.innerText = isOpen ? "Selamat ulang tahun! Klik tombol untuk membuka kejutanmu" : "Tutup Kejutan";
                    if (!isOpen) {
                        letter.scrollIntoView({ behavior: "smooth", block: "center" });
                    }
                });
                createFloatingItems();
                startFireworks();
            }, 700);
        } else {
            puzzleFeedback.innerText = "Hampir benar, coba lagi ya.";
        }
    });

    IMAGE_LIST.forEach((src, index) => {
        const img = document.createElement("img");
        img.src = src;
        if (index === 0) img.classList.add("active");
        slider.appendChild(img);
    });

    function startSlideshow() {
        const slides = slider.querySelectorAll("img");
        let current = 0;
        if (slides.length > 0) {
            setInterval(() => {
                slides[current].classList.remove("active");
                current = (current + 1) % slides.length;
                slides[current].classList.add("active");
            }, 3000);
        }
    }

    function startTyping() {
        const text = "Happy Birthday Asya ❤️ Semoga panjang umur, sehat selalu, dimudahkan segala urusannya, dan semua impiannya tercapai.";
        const typingTarget = document.getElementById("typing");
        let index = 0;
        typingTarget.textContent = "";
        typingTarget.style.whiteSpace = "pre-wrap";
        typingTarget.style.wordSpacing = "normal";

        const typingInterval = setInterval(() => {
            if (index >= text.length) {
                clearInterval(typingInterval);
                return;
            }
            typingTarget.textContent += text.charAt(index);
            index++;
        }, 45);
    }
}

function createFloatingItems() {
    setInterval(() => {
        const item = document.createElement("div");
        item.className = "floating";
        item.innerText = ["🎈", "💖", "🎀"][Math.floor(Math.random() * 3)];
        item.style.left = Math.random() * 100 + "vw";
        item.style.animationDuration = (7 + Math.random() * 5) + "s";
        document.body.appendChild(item);
        setTimeout(() => item.remove(), 10000);
    }, 700);

    for (let i = 0; i < 60; i++) {
        const star = document.createElement("div");
        star.className = "star";
        star.innerText = "✦";
        star.style.left = Math.random() * 100 + "vw";
        star.style.top = Math.random() * 100 + "vh";
        star.style.animationDelay = Math.random() * 2 + "s";
        document.body.appendChild(star);
    }

    setInterval(() => {
        const confetti = document.createElement("div");
        confetti.className = "confetti";
        confetti.innerText = ["🎊", "🎉", "✨", "💖", "🌸", "⭐"][Math.floor(Math.random() * 6)];
        confetti.style.left = Math.random() * 100 + "vw";
        confetti.style.animationDuration = (4 + Math.random() * 4) + "s";
        document.body.appendChild(confetti);
        setTimeout(() => confetti.remove(), 9000);
    }, 150);
}

function startFireworks() {
    const canvas = document.getElementById("firework");
    const ctx = canvas.getContext("2d");
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    const particles = [];

    function Particle(x, y) {
        this.x = x;
        this.y = y;
        this.dx = (Math.random() - 0.5) * 10;
        this.dy = (Math.random() - 0.5) * 10;
        this.life = 100;
        this.size = Math.random() * 4 + 2;
        this.color = `hsl(${Math.random() * 360}, 100%, 70%)`;
    }

    function explode() {
        const x = Math.random() * canvas.width;
        const y = Math.random() * canvas.height * 0.6;
        for (let i = 0; i < 100; i++) {
            particles.push(new Particle(x, y));
        }
    }

    setInterval(explode, 900);

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        particles.forEach((p, index) => {
            ctx.beginPath();
            ctx.fillStyle = p.color;
            ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
            ctx.fill();
            p.x += p.dx;
            p.y += p.dy;
            p.dy += 0.08;
            p.life -= 1;
            if (p.life <= 0) {
                particles.splice(index, 1);
            }
        });
        requestAnimationFrame(draw);
    }

    draw();
}

updateCountdown();
setInterval(updateCountdown, 1000);
</script>
</body>
</html>
        """.replace("{image_js}", image_js).replace("{audio}", audio),
        height=820,
    )