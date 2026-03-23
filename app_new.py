import streamlit as st
from memory_operations import *
from datetime import date

st.set_page_config(
    page_title="Personal Mesh",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@300;400;500&display=swap');

:root {
    --bg:        #090d12;
    --surface:   #0f1520;
    --border:    #1a2535;
    --accent:    #00d4aa;
    --accent2:   #0088ff;
    --text:      #e0eaf5;
    --muted:     #4a6080;
    --danger:    #ff4466;
}

/* Base */
html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'JetBrains Mono', monospace !important;
}

/* Hide default Streamlit elements */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}

[data-testid="stSidebar"] * {
    font-family: 'Syne', sans-serif !important;
}

/* Logo area */
.mesh-logo {
    padding: 2rem 1rem 1rem;
    text-align: center;
}

.mesh-logo h1 {
    font-family: 'Syne', sans-serif !important;
    font-weight: 800;
    font-size: 1.6rem;
    letter-spacing: -0.02em;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
}

.mesh-logo p {
    font-size: 0.65rem;
    color: var(--muted);
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin: 0.3rem 0 0;
}

/* Nav buttons */
.stRadio > div {
    gap: 0.3rem !important;
}

.stRadio label {
    background: transparent !important;
    border: 1px solid transparent !important;
    border-radius: 8px !important;
    padding: 0.6rem 1rem !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
    font-size: 0.85rem !important;
}

.stRadio label:hover {
    background: var(--border) !important;
    border-color: var(--border) !important;
}

/* Page title */
.page-title {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1.8rem;
    color: var(--text);
    margin-bottom: 0.2rem;
    letter-spacing: -0.02em;
}

.page-subtitle {
    font-size: 0.75rem;
    color: var(--muted);
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 2rem;
}

/* Chat messages */
.chat-user {
    display: flex;
    justify-content: flex-end;
    margin: 0.8rem 0;
}

.chat-user .bubble {
    background: linear-gradient(135deg, #003d80, #0055aa);
    border: 1px solid var(--accent2);
    border-radius: 16px 16px 4px 16px;
    padding: 0.8rem 1.2rem;
    max-width: 70%;
    font-size: 0.9rem;
    line-height: 1.5;
}

.chat-ai {
    display: flex;
    justify-content: flex-start;
    margin: 0.8rem 0;
}

.chat-ai .bubble {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px 16px 16px 4px;
    padding: 0.8rem 1.2rem;
    max-width: 75%;
    font-size: 0.9rem;
    line-height: 1.6;
}

.chat-ai .avatar {
    width: 32px;
    height: 32px;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.9rem;
    margin-right: 0.6rem;
    flex-shrink: 0;
    margin-top: 0.2rem;
}

/* Memory cards */
.memory-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.8rem;
    transition: border-color 0.2s;
}

.memory-card:hover {
    border-color: var(--accent);
}

.memory-card .meta {
    font-size: 0.7rem;
    color: var(--muted);
    margin-bottom: 0.4rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

.memory-card .content {
    font-size: 0.88rem;
    color: var(--text);
    line-height: 1.5;
}

.tag {
    display: inline-block;
    background: rgba(0, 212, 170, 0.1);
    border: 1px solid rgba(0, 212, 170, 0.3);
    color: var(--accent);
    border-radius: 20px;
    padding: 0.15rem 0.6rem;
    font-size: 0.65rem;
    margin-right: 0.3rem;
    letter-spacing: 0.05em;
}

.badge {
    display: inline-block;
    border-radius: 4px;
    padding: 0.1rem 0.5rem;
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

.badge-high   { background: rgba(255,68,102,0.15); color: #ff4466; border: 1px solid rgba(255,68,102,0.3); }
.badge-medium { background: rgba(255,165,0,0.15);  color: #ffaa00; border: 1px solid rgba(255,165,0,0.3); }
.badge-low    { background: rgba(0,212,170,0.15);  color: #00d4aa; border: 1px solid rgba(0,212,170,0.3); }

/* Stat cards */
.stat-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.2rem;
    text-align: center;
}

.stat-card .number {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.stat-card .label {
    font-size: 0.7rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 0.2rem;
}

/* Input styling */
.stTextInput input, .stTextArea textarea, .stSelectbox select {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.88rem !important;
}

.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(0,212,170,0.15) !important;
}

/* Buttons */
.stButton button {
    background: linear-gradient(135deg, var(--accent), var(--accent2)) !important;
    color: #000 !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.05em !important;
    padding: 0.5rem 1.5rem !important;
    transition: opacity 0.2s !important;
}

.stButton button:hover {
    opacity: 0.85 !important;
}

/* Chat input */
.stChatInput textarea {
    background: var(--surface) !important;
    border: 1px solid var(--accent) !important;
    border-radius: 12px !important;
    color: var(--text) !important;
    font-family: 'JetBrains Mono', monospace !important;
}

/* Divider */
hr { border-color: var(--border) !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: var(--muted); }

</style>
""", unsafe_allow_html=True)


# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="mesh-logo">
        <h1>⬡ PERSONAL MESH</h1>
        <p>Your AI Memory Layer</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    page = st.radio(
        "",
        ["💬  Chat", "🧠  Memory"],
        label_visibility="collapsed"
    )

    st.markdown("---")

    # Quick stats in sidebar
    try:
        stats = get_stats()
        total = stats['total']
        st.markdown(f"""
        <div style="padding: 0.5rem 0; font-size: 0.75rem; color: var(--muted);">
            <div style="display:flex; justify-content:space-between; margin-bottom:0.4rem;">
                <span>MEMORIES</span>
                <span style="color: var(--accent); font-weight:600;">{total}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    except:
        pass


# ── CHAT PAGE ─────────────────────────────────────────────────────────────────
if "Chat" in page:

    st.markdown('<div class="page-title">Ask Personal Mesh</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Your AI — powered by your memories</div>', unsafe_allow_html=True)

    # Init chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display chat history
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="chat-user">
                <div class="bubble">{msg["content"]}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-ai">
                <div class="avatar">⬡</div>
                <div class="bubble">{msg["content"]}</div>
            </div>
            """, unsafe_allow_html=True)

    # Empty state
    if not st.session_state.chat_history:
        st.markdown("""
        <div style="text-align:center; padding: 4rem 2rem; color: var(--muted);">
            <div style="font-size: 3rem; margin-bottom: 1rem;">⬡</div>
            <div style="font-family: 'Syne', sans-serif; font-size: 1.1rem; color: var(--text); margin-bottom: 0.5rem;">
                Ask me anything about your life
            </div>
            <div style="font-size: 0.8rem; line-height: 1.8;">
                "What projects have I built?"<br>
                "Tell me about my hackathon performance"<br>
                "What are my skills?"
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Voice in chat
    col_chat, col_voice = st.columns([6, 1])

    with col_voice:
        voice_chat_btn = st.button("🎙️")

    with col_chat:
        question = st.chat_input("Ask something about your memories...")

    if voice_chat_btn:
        with st.spinner("Recording 5s... speak now!"):
            from voice_input import voice_to_text
            question = voice_to_text(duration=5)
        if question:
            st.session_state.chat_history.append({"role": "user", "content": question})
            with st.spinner(""):
                try:
                    from rag import ask_personal_mesh
                    answer = ask_personal_mesh(question)
                except Exception as e:
                    answer = f"Error: {str(e)}"
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
            st.rerun()

    if question:
        st.session_state.chat_history.append({"role": "user", "content": question})

        with st.spinner(""):
            try:
                from rag import ask_personal_mesh
                answer = ask_personal_mesh(question)
            except Exception as e:
                answer = f"Error connecting to AI: {str(e)}"

        st.session_state.chat_history.append({"role": "assistant", "content": answer})
        st.rerun()


# ── MEMORY PAGE ───────────────────────────────────────────────────────────────
elif "Memory" in page:

    tab1, tab2, tab3 = st.tabs(["＋  Add", "  Browse", "  Stats"])

    # ── ADD TAB
    with tab1:
        st.markdown('<div style="height:1rem"></div>', unsafe_allow_html=True)
        st.markdown('<div class="page-title" style="font-size:1.3rem">New Memory</div>', unsafe_allow_html=True)
        st.markdown('<div style="height:1rem"></div>', unsafe_allow_html=True)

        # Voice input at top
        col_mic, col_dur = st.columns([2, 1])
        with col_mic:
            record_btn = st.button("🎙️ Record Voice Memory")
        with col_dur:
            duration = st.selectbox("Duration", [5, 10, 15, 30], index=1, label_visibility="collapsed")

        if record_btn:
            with st.spinner(f"Recording {duration}s... speak now!"):
                from voice_input import voice_to_text
                transcript = voice_to_text(duration=duration)
            if transcript:
                st.session_state.voice_transcript = transcript
            else:
                st.warning("Could not hear anything. Check your mic.")

        # Pre-fill content from voice if available
        default_content = st.session_state.get("voice_transcript", "")

        content = st.text_area("What happened?", value=default_content, height=120, placeholder="Describe your memory or record voice above...")

        col1, col2 = st.columns(2)
        with col1:
            mem_type = st.selectbox("Type", ["project", "personal", "health", "work"])
            priority = st.selectbox("Priority", ["medium", "high", "low"])
        with col2:
            user_id = st.text_input("User", value="ayush")
            mem_date = st.date_input("Date", value=date.today())

        tags = st.text_input("Tags", placeholder="ai, project, health ...")

        if st.button("Save Memory"):
            if content.strip():
                result = add_memory(content, user_id, mem_type, priority, str(mem_date), tags)
                st.success(result)
                st.session_state.voice_transcript = ""
            else:
                st.error("Please enter some content.")


    # ── BROWSE TAB
    with tab2:
        st.markdown('<div style="height:1rem"></div>', unsafe_allow_html=True)

        col1, col2 = st.columns([3, 1])
        with col1:
            search_q = st.text_input("", placeholder="Search memories...", label_visibility="collapsed")
        with col2:
            type_filter = st.selectbox("", ["all", "project", "personal", "health", "work"], label_visibility="collapsed")

        memories = get_all_memories()

        if search_q:
            memories = [m for m in memories if search_q.lower() in m[1].lower()]
        if type_filter != "all":
            memories = [m for m in memories if m[4] == type_filter]

        st.markdown(f'<div style="font-size:0.75rem; color:var(--muted); margin-bottom:1rem;">{len(memories)} memories</div>', unsafe_allow_html=True)

        for mem in memories:
            tags_html = ""
            if len(mem) > 6 and mem[6]:
                for tag in mem[6].split(","):
                    if tag.strip():
                        tags_html += f'<span class="tag">#{tag.strip()}</span>'

            priority_badge = f'<span class="badge badge-{mem[5]}">{mem[5]}</span>' if mem[5] else ""
            type_badge = f'<span class="badge" style="background:rgba(0,136,255,0.1);color:#0088ff;border:1px solid rgba(0,136,255,0.3)">{mem[4]}</span>'

            st.markdown(f"""
            <div class="memory-card">
                <div class="meta">#{mem[0]} · {mem[2][:10]} · {type_badge} {priority_badge}</div>
                <div class="content">{mem[1]}</div>
                {'<div style="margin-top:0.6rem">' + tags_html + '</div>' if tags_html else ''}
            </div>
            """, unsafe_allow_html=True)

    # ── STATS TAB
    with tab3:
        st.markdown('<div style="height:1rem"></div>', unsafe_allow_html=True)
        try:
            stats = get_stats()

            total = stats['total']
            project_count = sum([c for t, c in stats['by_type'] if t == 'project'])
            high_count = sum([c for p, c in stats['by_priority'] if p == 'high'])
            personal_count = sum([c for t, c in stats['by_type'] if t == 'personal'])

            c1, c2, c3, c4 = st.columns(4)
            for col, num, label in [
                (c1, total, "Total"),
                (c2, project_count, "Projects"),
                (c3, personal_count, "Personal"),
                (c4, high_count, "High Priority")
            ]:
                with col:
                    st.markdown(f"""
                    <div class="stat-card">
                        <div class="number">{num}</div>
                        <div class="label">{label}</div>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown('<div style="height:1.5rem"></div>', unsafe_allow_html=True)

            if stats['by_type']:
                import plotly.graph_objects as go
                col1, col2 = st.columns(2)

                with col1:
                    labels = [i[0] for i in stats['by_type']]
                    values = [i[1] for i in stats['by_type']]
                    fig = go.Figure(data=[go.Pie(
                        labels=labels, values=values, hole=0.6,
                        marker=dict(colors=['#00d4aa','#0088ff','#ff4466','#ffaa00'])
                    )])
                    fig.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='#e0eaf5', family='JetBrains Mono'),
                        showlegend=True,
                        height=280,
                        margin=dict(t=20, b=20, l=20, r=20)
                    )
                    st.plotly_chart(fig, use_container_width=True)

                with col2:
                    if stats['by_priority']:
                        priorities = [i[0] for i in stats['by_priority']]
                        counts = [i[1] for i in stats['by_priority']]
                        colors = {'high': '#ff4466', 'medium': '#ffaa00', 'low': '#00d4aa'}
                        fig2 = go.Figure(data=[go.Bar(
                            x=priorities, y=counts,
                            marker_color=[colors.get(p, '#4a6080') for p in priorities],
                            marker_line_width=0
                        )])
                        fig2.update_layout(
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)',
                            font=dict(color='#e0eaf5', family='JetBrains Mono'),
                            height=280,
                            showlegend=False,
                            margin=dict(t=20, b=20, l=20, r=20),
                            xaxis=dict(gridcolor='#1a2535'),
                            yaxis=dict(gridcolor='#1a2535')
                        )
                        st.plotly_chart(fig2, use_container_width=True)
        except Exception as e:
            st.error(f"Stats error: {e}")