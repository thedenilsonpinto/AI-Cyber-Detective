import streamlit as st
import matplotlib.pyplot as plt
from detective_engine import investigate_message
from report_generator import create_report
from PIL import Image

st.set_page_config(
    page_title="AI Cyber Detective",
    page_icon="🕵️",
    layout="wide"
)
logo = Image.open("assets/logo.png")

st.image(
    logo,
    width=180
)

# ----------------------------------
# PAGE CONFIG
# ----------------------------------

st.set_page_config(
    page_title="AI Cyber Detective",
    page_icon="🕵️",
    layout="wide"
)

# ----------------------------------
# GLASSMORPHISM THEME
# ----------------------------------

st.markdown("""
<style>

.stApp{
    background: linear-gradient(
        135deg,
        #0f172a,
        #111827,
        #1e293b
    );
}

.hero{
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(15px);
    border-radius:25px;
    padding:30px;
    text-align:center;
    border:1px solid rgba(255,255,255,0.15);
    box-shadow:0 8px 32px rgba(0,0,0,0.3);
    margin-bottom:20px;
}

.hero h1{
    color:#00ff88;
}

.hero p{
    color:white;
}

.metric-box{
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(10px);
    border-radius:20px;
    padding:20px;
    text-align:center;
    border:1px solid rgba(255,255,255,0.15);
    margin-bottom:15px;
}

.metric-title{
    color:#cccccc;
    font-size:16px;
}

.metric-value{
    color:#00ff88;
    font-size:24px;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------------
# HERO SECTION
# ----------------------------------

st.markdown("""
<div class="hero">

<h1>🕵️ AI Cyber Detective</h1>

<p>
AI-Powered Cyber Threat Investigation Platform
</p>

<p>
Developed by <b>Denilson Pinto B</b>
</p>

</div>
""", unsafe_allow_html=True)
st.caption(
    "Powered by AI • Developed by DENILSON PINTO B"
)

# ----------------------------------
# RECOMMENDATIONS
# ----------------------------------

recommendations = {

    "Phishing Scam":
    "Do not click unknown links. Verify the sender before responding.",

    "Fake Job Scam":
    "Never pay registration or interview fees.",

    "OTP Theft":
    "Never share OTPs with anyone.",

    "Investment Scam":
    "Verify investment platforms before sending money.",

    "Lottery Scam":
    "Ignore messages claiming you won money unexpectedly.",

    "Tech Support Scam":
    "Do not call unknown support numbers."
}

# ----------------------------------
# INPUT
# ----------------------------------

st.subheader("📩 Paste Suspicious Message")

message = st.text_area(
    "",
    height=250,
    placeholder="Paste suspicious email, SMS, WhatsApp message, job offer, scam text..."
)

# ----------------------------------
# BUTTON
# ----------------------------------

if st.button("🔍 Investigate"):

    if message.strip():

        results = investigate_message(message)
        # ----------------------------------
        # METRIC CARDS
        # ----------------------------------

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"""
            <div class="metric-box">
            <div class="metric-title">🎯 Attack Type</div>
            <div class="metric-value">{results['attack']}</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="metric-box">
            <div class="metric-title">⚠ Risk Level</div>
            <div class="metric-value">{results['risk']}</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="metric-box">
            <div class="metric-title">📊 Confidence</div>
            <div class="metric-value">{results['confidence']}%</div>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
            <div class="metric-box">
            <div class="metric-title">🏆 Grade</div>
            <div class="metric-value">{results['grade']}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # ----------------------------------
        # SUMMARY
        # ----------------------------------

        summary = f"""
Attack Type: {results['attack']}

Risk Level: {results['risk']}

Confidence Score: {results['confidence']}%

Security Grade: {results['grade']}
"""

        st.subheader("📋 Investigation Summary")
        st.info(summary)
        # ----------------------------------
# AI THREAT EXPLANATION
# ----------------------------------

        st.subheader("🤖 AI Threat Explanation")

        st.info(
    results["explanation"]
)

        # ----------------------------------
        # EVIDENCE
        # ----------------------------------

        st.subheader("🔍 Evidence Found")

        evidence_list = results.get("evidence", [])

        if evidence_list:
            for item in evidence_list:
                st.warning(f"⚠ Detected Pattern: {item}")
        else:
            st.success("No suspicious evidence detected.")

        # ----------------------------------
        # RECOMMENDATION
        # ----------------------------------

        st.subheader("🛡 Cyber Recommendation")

        if results["attack"] in recommendations:
            st.success(
                recommendations[results["attack"]]
            )
        else:

            st.success(
        "Avoid clicking suspicious links, sharing OTPs, passwords, bank details, or sending money to unknown sources."
    )
            confidence = max(
    0,
    min(
        int(results["confidence"]),
        100
    )
)
        # ----------------------------------
        # THREAT METER
        # ----------------------------------

        st.subheader("🚨 Threat Meter")

        st.progress(
            int(results["confidence"])
        )

        # ----------------------------------
        # THREAT STATISTICS
        # ----------------------------------

        st.subheader("📈 Threat Statistics")

        colA, colB, colC = st.columns(3)

        with colA:
            st.metric(
                "Threat %",
                f"{results['confidence']}%"
            )

        with colB:
            st.metric(
                "Safety %",
                f"{100-results['confidence']}%"
            )

        with colC:
            st.metric(
                "Grade",
                results["grade"]
            )

        # ----------------------------------
        # PIE CHART
        # ----------------------------------

        st.subheader("📊 Threat Analysis")

        fig, ax = plt.subplots()

        ax.pie(
            [
                results["confidence"],
                100-results["confidence"]
            ],
            labels=["Threat", "Safe"],
            autopct="%1.1f%%"
        )

        st.pyplot(fig)
        st.progress(confidence)
        100 - confidence

        # ----------------------------------
        # TIMELINE
        # ----------------------------------

        st.subheader("📜 Investigation Timeline")

        st.write("1️⃣ Message Submitted")
        st.write("2️⃣ AI Analysis Started")
        st.write("3️⃣ Threat Patterns Detected")
        st.write("4️⃣ Risk Level Calculated")
        st.write("5️⃣ Investigation Report Generated")

        # ----------------------------------
        # DOWNLOAD REPORT
        # ----------------------------------

        st.subheader(
            "📥 Download Report"
        )

        pdf_file = create_report(results)

        with open(pdf_file, "rb") as file:
            st.download_button(
                label="📄 Download PDF Report",
                data=file,
                file_name="Cyber_Detective_Report.pdf",
                mime="application/pdf"
                )

    else:

        st.warning(
            "Paste a suspicious message first."
        )

# ----------------------------------
# FOOTER
# ----------------------------------

st.markdown("---")

st.markdown("""
### 🛡️ AI Cyber Detective

Developed by **DENILSON PINTO B**

Artificial Intelligence Engineer

© 2026 All Rights Reserved
""")