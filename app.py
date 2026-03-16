import streamlit as st
from memory_operations import *
from datetime import date

st.set_page_config(page_title="Personal Mesh", page_icon="🧠", layout="wide")

# Header
st.title("🧠 Personal Mesh")
st.markdown("*Your AI-powered memory system*")
st.divider()

# Sidebar for actions
with st.sidebar:
    st.header("📋 Actions")
    action = st.radio(
    "Choose an action:",
    ["📊 Dashboard", "📝 Add Memory", "👁️ View All", "🔍 Search", "🗂️ Filter by Type", "📅 Filter by Date", "🏷️ Browse by Tags", "✏️ Edit", "🗑️ Delete"]
)

# Main content area
if action == "📊 Dashboard":
    st.subheader("📊 Memory Dashboard")
    
    stats = get_stats()
    
    # Top metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Memories", stats['total'])
    
    with col2:
        project_count = sum([count for typ, count in stats['by_type'] if typ == 'project'])
        st.metric("Projects", project_count)
    
    with col3:
        personal_count = sum([count for typ, count in stats['by_type'] if typ == 'personal'])
        st.metric("Personal", personal_count)
    
    with col4:
        high_priority = sum([count for pri, count in stats['by_priority'] if pri == 'high'])
        st.metric("High Priority", high_priority)
    
    st.divider()
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Memories by Type")
        if stats['by_type']:
            import plotly.graph_objects as go
            
            labels = [item[0] for item in stats['by_type']]
            values = [item[1] for item in stats['by_type']]
            
            fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data yet")
    
    with col2:
        st.subheader("⚡ Priority Distribution")
        if stats['by_priority']:
            import plotly.graph_objects as go
            
            priorities = [item[0] for item in stats['by_priority']]
            counts = [item[1] for item in stats['by_priority']]
            
            colors = {'high': '#ff4b4b', 'medium': '#ffa500', 'low': '#00cc00'}
            bar_colors = [colors.get(p, '#cccccc') for p in priorities]
            
            fig = go.Figure(data=[go.Bar(x=priorities, y=counts, marker_color=bar_colors)])
            fig.update_layout(height=300, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data yet")
    
    # Recent activity
    st.subheader("📅 Recent Activity (Last 7 Days)")
    if stats['recent']:
        import plotly.graph_objects as go
        
        dates = [item[0] for item in stats['recent']]
        counts = [item[1] for item in stats['recent']]
        
        fig = go.Figure(data=[go.Scatter(x=dates, y=counts, mode='lines+markers', fill='tozeroy')])
        fig.update_layout(height=250, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No recent activity")

elif action == "📝 Add Memory":
    st.subheader("Add New Memory")
    
    content = st.text_area("What happened?", height=100)
    
    col1, col2 = st.columns(2)
    with col1:
        mem_type = st.selectbox("Type", ["project", "personal", "health", "work"])
        priority = st.selectbox("Priority", ["low", "medium", "high"])
    
    with col2:
        user_id = st.text_input("User ID", value="ayush")
        mem_date = st.date_input("Date", value=date.today())
    
    tags = st.text_input("Tags (comma-separated)", placeholder="e.g. hackathon, AI, coding")
    
    if st.button("💾 Save Memory", type="primary"):
        if content.strip():
            result = add_memory(content, user_id, mem_type, priority, str(mem_date), tags)
            st.success(result)
        else:
            st.error("❌ Please enter some content!")

elif action == "👁️ View All":
    st.subheader("All Memories")
    
    memories = get_all_memories()
    
    if memories:
        for mem in memories:
            with st.expander(f"**[{mem[0]}]** {mem[1][:50]}..." if len(mem[1]) > 50 else f"**[{mem[0]}]** {mem[1]}"):
                st.write(f"**Content:** {mem[1]}")
                st.write(f"**Type:** {mem[4]} | **Priority:** {mem[5]}")
                if mem[6]:  # if tags exist
                    st.write(f"**Tags:** {mem[6]}")
                st.write(f"**Date:** {mem[2]}")
                st.write(f"**User:** {mem[3]}")
    else:
        st.info("No memories found. Add your first memory!")

elif action == "🔍 Search":
    st.subheader("Search Memories")
    
    keyword = st.text_input("Enter keyword to search:")
    
    if keyword:
        results = search_memory(keyword)
        
        if results:
            st.success(f"Found {len(results)} result(s)")
            for mem in results:
                with st.expander(f"**[{mem[0]}]** {mem[1][:50]}..."):
                    st.write(f"**Content:** {mem[1]}")
                    st.write(f"**Type:** {mem[4]} | **Priority:** {mem[5]}")
                    st.write(f"**Date:** {mem[2]}")
        else:
            st.warning("No matching memories found.")

elif action == "🗂️ Filter by Type":
    st.subheader("Filter by Type")
    
    filter_type = st.selectbox("Select type:", ["project", "personal", "health", "work"])
    
    if st.button("🔎 Filter"):
        results = filter_by_type(filter_type)
        
        if results:
            st.success(f"Found {len(results)} {filter_type} memory/memories")
            for mem in results:
                with st.expander(f"**[{mem[0]}]** {mem[1][:50]}..."):
                    st.write(f"**Content:** {mem[1]}")
                    st.write(f"**Priority:** {mem[5]}")
                    st.write(f"**Date:** {mem[2]}")
        else:
            st.warning(f"No {filter_type} memories found.")

elif action == "📅 Filter by Date":
    st.subheader("Filter by Date")
    
    filter_date = st.date_input("Select date:")
    
    if st.button("🔎 Filter"):
        results = filter_by_date(str(filter_date))
        
        if results:
            st.success(f"Found {len(results)} memory/memories on {filter_date}")
            for mem in results:
                with st.expander(f"**[{mem[0]}]** {mem[1][:50]}..."):
                    st.write(f"**Content:** {mem[1]}")
                    st.write(f"**Type:** {mem[4]} | **Priority:** {mem[5]}")
        else:
            st.warning(f"No memories found on {filter_date}.")

elif action == "🏷️ Browse by Tags":
    st.subheader("Browse by Tags")
    
    all_tags = get_all_tags()
    
    if all_tags:
        st.write("**Available tags:**")
        
        # Display tags as clickable buttons
        cols = st.columns(4)
        for idx, tag in enumerate(all_tags):
            with cols[idx % 4]:
                if st.button(f"#{tag}", key=f"tag_{tag}"):
                    st.session_state.selected_tag = tag
        
        # Show memories for selected tag
        if 'selected_tag' in st.session_state:
            st.divider()
            st.subheader(f"Memories tagged with #{st.session_state.selected_tag}")
            
            results = search_by_tag(st.session_state.selected_tag)
            
            if results:
                for mem in results:
                    with st.expander(f"**[{mem[0]}]** {mem[1][:50]}..."):
                        st.write(f"**Content:** {mem[1]}")
                        st.write(f"**Type:** {mem[4]} | **Priority:** {mem[5]}")
                        st.write(f"**Tags:** {mem[6]}")
                        st.write(f"**Date:** {mem[2]}")
    else:
        st.info("No tags yet. Add tags when creating memories!")

elif action == "✏️ Edit":
    st.subheader("Edit Memory")
    
    memories = get_all_memories()
    
    if memories:
        mem_options = {f"[{m[0]}] {m[1][:40]}...": m[0] for m in memories}
        selected = st.selectbox("Select memory to edit:", mem_options.keys())
        
        new_content = st.text_area("New content:", height=100)
        
        if st.button("💾 Update", type="primary"):
            if new_content.strip():
                result = edit_memory(mem_options[selected], new_content)
                st.success(result)
            else:
                st.error("❌ Content cannot be empty!")
    else:
        st.info("No memories to edit.")

elif action == "🗑️ Delete":
    st.subheader("Delete Memory")
    
    memories = get_all_memories()
    
    if memories:
        mem_options = {f"[{m[0]}] {m[1][:40]}...": m[0] for m in memories}
        selected = st.selectbox("Select memory to delete:", mem_options.keys())
        
        st.warning("⚠️ This action cannot be undone!")
        
        if st.button("🗑️ Delete Permanently", type="primary"):
            result = delete_memory(mem_options[selected])
            st.success(result)
            st.rerun()
    else:
        st.info("No memories to delete.")