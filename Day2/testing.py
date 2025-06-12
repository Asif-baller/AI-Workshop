import streamlit as st
import pandas as pd
import datetime

# Initialize session state
if "bugs" not in st.session_state:
    st.session_state.bugs = []

st.set_page_config(page_title="Bug Tracker", layout="wide")
st.title("🐞 Software Testing Team – Bug Tracker")

# Add a new bug form
st.subheader("➕ Report a New Bug")
with st.form("bug_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        tester = st.text_input("Tester Name")
        bug_date = st.date_input("Date Found", datetime.date.today())
        module = st.text_input("Module Name")
        priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
    with col2:
        description = st.text_area("Bug Description")
        status = st.selectbox("Bug Status", ["Open", "Forwarded to Dev", "Fixed"])
        developer = st.text_input("Forward to Developer (optional)")

    submit = st.form_submit_button("Submit Bug Report")

    if submit and tester and module and description:
        bug = {
            "Tester": tester,
            "Date": bug_date,
            "Module": module,
            "Priority": priority,
            "Description": description,
            "Status": status,
            "Developer": developer,
        }
        st.session_state.bugs.append(bug)
        st.success("Bug report submitted!")

# View/filter existing bug reports
st.subheader("📊 Bug Reports Dashboard")

status_filter = st.selectbox("Filter by Status", ["All", "Open", "Forwarded to Dev", "Fixed"])
if st.session_state.bugs:
    df = pd.DataFrame(st.session_state.bugs)
    if status_filter != "All":
        df = df[df["Status"] == status_filter]

    st.dataframe(df, use_container_width=True)

    # Optionally export to CSV
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download Bug Report as CSV",
        data=csv,
        file_name="bug_report.csv",
        mime="text/csv"
    )
else:
    st.info("No bugs reported yet.")

# Footer
st.markdown("---")
st.caption("Built for QA Teams | Streamlit + Python")