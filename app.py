
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import uuid
from datetime import datetime
from supabase import create_client

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="ChristNotes",
    page_icon="📚",
    layout="wide"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>
.stApp {
    background-color: #F3EBDD;
    color: #2E1F1B;
}

section[data-testid="stSidebar"] {
    background-color: #6B2D3A;
}

section[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
}

h1, h2, h3 {
    color: #6B2D3A;
}

div[data-testid="stMetric"] {
    background-color: #EADBCB;
    padding: 18px;
    border-radius: 10px;
}

.stTabs [data-baseweb="tab-list"] {
    justify-content: center;
    gap: 35px;
}

.stTextInput input {
    background-color: #F3EBDD;
    border: 1px solid #C8A27E;
    border-radius: 8px;
}

/* Global Button Styling */
.stButton > button {
    background-color: #6B2D3A;
    color: white;
    border-radius: 8px;
    border: none;
    height: 45px;
    font-weight: 600;
    letter-spacing: 0.3px;
}

.stButton > button:hover {
    background-color: #8A4654;
    color: white;
}

.block-container {
    padding-top: 3rem;
}

/* -------------------------------------------------- */
/* THE DUSTY ROSE PROFILE BOX FIX                     */
/* -------------------------------------------------- */

/* 1. Color the outer wrapper of the sidebar container */
section[data-testid="stSidebar"] div[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #B98A84 !important;
    border: 2px solid #B98A84 !important;
    border-radius: 10px !important;
}

/* 2. Strip the background from the immediate inner block so the color shows through */
section[data-testid="stSidebar"] div[data-testid="stVerticalBlockBorderWrapper"] > div[data-testid="stVerticalBlock"] {
    background-color: transparent !important;
}

/* 3. Ensure the Logout button stays burgundy against the rose background */
section[data-testid="stSidebar"] div[data-testid="stVerticalBlockBorderWrapper"] button {
    background-color: #6B2D3A !important;
    border: 1px solid rgba(255,255,255,0.3) !important;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# SUPABASE CONNECTION
# --------------------------------------------------

def get_supabase():
    return create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"]
    )

if "supabase" not in st.session_state:
    st.session_state.supabase = get_supabase()

sb = st.session_state.supabase

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "user" not in st.session_state:
    st.session_state.user = None

# --------------------------------------------------
# HELPER FUNCTION: GET RESOURCES
# --------------------------------------------------

def get_resources():
    response = (
        sb.table("resources")
        .select("*")
        .order("created_at", desc=True)
        .execute()
    )
    return response.data or []

# --------------------------------------------------
# LOGIN / REGISTRATION
# --------------------------------------------------


def authentication_page():

    # Center the entire authentication section
    left, center, right = st.columns([1, 1.15, 1])

    with center:

        # Add vertical spacing
        st.write("")
        st.write("")
        st.write("")
        
        # Application heading
        st.markdown(
            """
            <div style="text-align:center;">
                <h1 style="
                    color:#6B2D3A;
                    font-size:45px;
                    margin-bottom:0px;
                ">
                    ChristNotes
                </h1>
                <p style="
                    color:#88766B;
                    font-size:15px;
                    margin-top:5px;
                ">
                    YOUR ACADEMIC RESOURCE HUB
                </p>
                <p style="
                    color:#2E1F1B;
                    font-size:14px;
                    margin-top:25px;
                    margin-bottom:25px;
                ">
                    Discover. Share. Learn Together.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        login_tab, register_tab = st.tabs(
            ["Login", "Register"]
        )

        # ---------------- LOGIN ----------------

        with login_tab:

            st.markdown(
                "<h3 style='text-align:center;'>Welcome back!</h3>",
                unsafe_allow_html=True
            )

            email = st.text_input(
                "University Email",
                key="login_email",
                placeholder="Enter your email"
            )

            password = st.text_input(
                "Password",
                type="password",
                key="login_password",
                placeholder="Enter your password"
            )

            if st.button("Sign In", use_container_width=True):

                if not email or not password:
                    st.error("Please enter your email and password.")

                else:
                    try:
                        result = sb.auth.sign_in_with_password({
                            "email": email,
                            "password": password
                        })

                        st.session_state.user = result.user
                        st.rerun()

                    except Exception:
                        st.error("Login failed. Check your credentials.")

        # ---------------- REGISTER ----------------

        with register_tab:

            st.markdown(
                "<h3 style='text-align:center;'>Create your account</h3>",
                unsafe_allow_html=True
            )

            name = st.text_input(
                "Full Name",
                key="register_name",
                placeholder="Enter your full name"
            )

            email = st.text_input(
                "University Email",
                key="register_email",
                placeholder="Enter your university email"
            )

            password = st.text_input(
                "Create Password",
                type="password",
                key="register_password",
                placeholder="Minimum 6 characters"
            )

            if st.button("Create Account", use_container_width=True):

                if not name.strip() or not email.strip() or not password:
                    st.error("Please fill in all fields.")

                elif len(password) < 6:
                    st.error("Password must contain at least 6 characters.")

                else:
                    try:
                        result = sb.auth.sign_up({
                            "email": email.strip(),
                            "password": password,
                            "options": {
                                "data": {
                                    "full_name": name.strip()
                                }
                            }
                        })

                        if result.session:
                            st.session_state.user = result.user
                            st.success("Account created!")
                            st.rerun()

                        else:
                            st.success(
                                "Account created! Please verify your email."
                            )

                    except Exception as e:
                        st.error(f"Registration failed: {e}")

        st.markdown(
            """
            <p style="
                text-align:center;
                color:#88766B;
                font-size:12px;
                margin-top:35px;
            ">
                CHRISTNOTES · A COMMUNITY OF SHARED KNOWLEDGE
            </p>
            """,
            unsafe_allow_html=True
        )



# --------------------------------------------------
# HOME PAGE
# --------------------------------------------------

def home_page():

    st.title("Welcome to ChristNotes")
    st.caption("Discover, share and learn together.")

    resources = get_resources()
    df = pd.DataFrame(resources)

    # Calculate metrics safely
    if not df.empty:
        if "course" not in df.columns:
            df["course"] = "Unknown"
            
        total_resources = len(df)
        total_courses = df["course"].nunique()
        total_subjects = df["subject"].nunique()
        total_contributors = df["uploaded_by"].nunique()
    else:
        total_resources = total_courses = total_subjects = total_contributors = 0

    # Expanded to 4 columns for the new Course metric
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Resources", total_resources)
    col2.metric("Courses", total_courses)
    col3.metric("Subjects", total_subjects)
    col4.metric("Contributors", total_contributors)

    st.divider()

    st.subheader("Recently Uploaded")

    if resources:
        for resource in resources[:5]:
            with st.container(border=True):
                st.markdown(f"**{resource['title']}**")
                st.write(resource["description"])
                st.caption(
                    f"Course: {resource.get('course', 'N/A')} | "
                    f"Subject: {resource.get('subject', 'N/A')} | "
                    f"{resource.get('semester', 'N/A')}"
                )
    else:
        st.info("No resources uploaded yet. Be the first!")


# --------------------------------------------------
# UPLOAD PAGE
# --------------------------------------------------
import uuid # Make sure this is imported at the top of app.py

# --------------------------------------------------
# UPLOAD PAGE
# --------------------------------------------------
import uuid # Make sure this is imported somewhere at the top of app.py

def upload_page():
    st.title("Upload Notes")
    st.caption("Share your academic resources with the community.")

    with st.form("upload_form", clear_on_submit=True):
        title = st.text_input("Document Title *")
        description = st.text_area("Description")
        
        col1, col2, col3 = st.columns(3)
        
        # HERE IT IS: Course is now a free text field!
        course = col1.text_input("Course *") 
        subject = col2.text_input("Subject *")
        semester = col3.selectbox("Semester *", [f"Semester {i}" for i in range(1, 9)])
        
        # File Validation
        st.caption("Allowed types: PDF, DOCX, PPTX (Max size: 10MB)")
        uploaded_file = st.file_uploader("Choose a file *", type=["pdf", "docx", "pptx"], label_visibility="collapsed")
        
        submit_button = st.form_submit_button("Upload Resource", use_container_width=True)

    if submit_button:
        # Check all mandatory fields including the new course text field
        if not title or not course or not subject or not uploaded_file:
            st.error("Please fill out all mandatory fields marked with *")
            
        # Check file size (10MB)
        elif uploaded_file.size > 10 * 1024 * 1024:
            st.error("File is too large! Please upload a file smaller than 10MB.")
            
        else:
            # UX Polish: The loading spinner
            with st.spinner("Uploading to cloud storage... please wait ☁️"):
                try:
                    user_id = st.session_state.user.id
                    user_email = st.session_state.user.email
                    
                    file_ext = uploaded_file.name.split('.')[-1]
                    unique_filename = f"{uuid.uuid4()}.{file_ext}"
                    storage_path = f"{user_id}/{unique_filename}"
                    
                    file_bytes = uploaded_file.read()
                    
                    # Fixed to point to your exact "christ notes" bucket!
                    sb.storage.from_("christnotes").upload(storage_path, file_bytes)
                    
                    record = {
                        "title": title,
                        "description": description,
                        "course": course.upper(), # Capitalizes "mca" to "MCA" automatically!
                        "subject": subject,
                        "semester": semester,
                        "file_name": uploaded_file.name,
                        "storage_path": storage_path,
                        "uploaded_by": user_id,
                        "uploader_name": user_email.split('@')[0], 
                    }
                    
                    sb.table("resources").insert(record).execute()
                    
                    # UX Polish: The success toast!
                    st.toast("Resource uploaded successfully! 🎉", icon="✅")
                    st.success(f"**{title}** has been added to ChristNotes!")
                    
                except Exception as e:
                    st.error(f"An error occurred during upload: {e}")
# --------------------------------------------------
# EXPLORE NOTES PAGE
# --------------------------------------------------

def explore_page():

    st.title("Explore Notes")
    st.caption("Search and discover shared academic resources.")

    resources = get_resources()

    if not resources:
        st.info("No documents available yet.")
        return

    df = pd.DataFrame(resources)
    
    # Safety check for older test uploads that might not have a course
    if "course" not in df.columns:
        df["course"] = "Unknown"

    search = st.text_input(
        "Search by document name or description"
    )

    # Expanded to 3 columns for the new Course filter
    col1, col2, col3 = st.columns(3)

    # Get unique lists for dropdowns, removing empty values
    courses = ["All Courses"] + sorted(
        df["course"].dropna().astype(str).unique().tolist()
    )
    subjects = ["All Subjects"] + sorted(
        df["subject"].dropna().astype(str).unique().tolist()
    )
    semesters = ["All Semesters"] + sorted(
        df["semester"].dropna().astype(str).unique().tolist()
    )

    selected_course = col1.selectbox("Course", courses)
    selected_subject = col2.selectbox("Subject", subjects)
    selected_semester = col3.selectbox("Semester", semesters)

    # Apply Search Filter
    if search:
        df = df[
            df["title"].str.contains(search, case=False, na=False)
            | df["description"].str.contains(search, case=False, na=False)
        ]

    # Apply Dropdown Filters
    if selected_course != "All Courses":
        df = df[df["course"] == selected_course]
        
    if selected_subject != "All Subjects":
        df = df[df["subject"] == selected_subject]

    if selected_semester != "All Semesters":
        df = df[df["semester"] == selected_semester]

    st.divider()

    if df.empty:
        st.warning("No matching documents found.")
        return

    for _, resource in df.iterrows():

        with st.container(border=True):

            st.subheader(resource["title"])
            st.write(resource["description"])

            # Updated to show Course alongside Subject and Semester
            st.caption(
                f"Course: {resource.get('course', 'N/A')} | "
                f"Subject: {resource.get('subject', 'N/A')} | "
                f"{resource.get('semester', 'N/A')} | "
                f"File: {resource.get('file_name', 'N/A')}"
            )

            try:
                file_data = sb.storage.from_(
                    "christnotes"
                ).download(resource["storage_path"])

                st.download_button(
                    label="Download Document",
                    data=file_data,
                    file_name=resource["file_name"],
                    key=f"download_{resource['id']}"
                )

            except Exception as e:
                st.error("Unable to download this document.")


# --------------------------------------------------
# ANALYTICS PAGE
# --------------------------------------------------

def analytics_page():

    st.title("Analytics Dashboard")
    st.caption("Insights into academic resource sharing.")

    resources = get_resources()

    if not resources:
        st.info("Upload some resources to view analytics.")
        return

    df = pd.DataFrame(resources)
    
    if "course" not in df.columns:
        df["course"] = "Unknown"

    # --- DELTA METRICS LOGIC ---
    df["created_at"] = pd.to_datetime(df["created_at"])
    
    now = pd.Timestamp.now(tz='UTC')
    last_30 = now - pd.Timedelta(days=30)
    last_60 = now - pd.Timedelta(days=60)
    
    current_uploads = df[df["created_at"] > last_30]
    prev_uploads = df[(df["created_at"] <= last_30) & (df["created_at"] > last_60)]
    
    curr_total = len(current_uploads)
    prev_total = len(prev_uploads)
    
    unique_contributors = current_uploads["uploaded_by"].nunique()
    prev_contributors = prev_uploads["uploaded_by"].nunique()
    
    user_counts = df['uploaded_by'].value_counts()
    mean_uploads = user_counts.mean() if not user_counts.empty else 0

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Uploads (30d)", curr_total, delta=(curr_total - prev_total))
    col2.metric("Active Contributors (30d)", unique_contributors, delta=(unique_contributors - prev_contributors))
    col3.metric("Mean Docs / Student", f"{mean_uploads:.2f}")

    st.divider()

    # --- ROW 1: ORIGINAL GRAPHS (Bar Charts) ---
    col_chart1, col_chart2 = st.columns(2)

    # Chart 1: Popular Subjects
    with col_chart1:
        st.subheader("Popular Subjects")
        subject_counts = df["subject"].value_counts().head(5)
        
        fig1, ax1 = plt.subplots(figsize=(5, 4))
        subject_counts.plot(kind="bar", ax=ax1, color="#B98A84") 
        ax1.set_ylabel("Number of Documents")
        plt.xticks(rotation=45, ha='right')
        
        fig1.patch.set_alpha(0.0)
        ax1.patch.set_alpha(0.0)
        st.pyplot(fig1)
        plt.close(fig1)

    # Chart 2: Uploads by Semester
    with col_chart2:
        st.subheader("Uploads by Semester")
        sem_counts = df["semester"].value_counts()
        
        fig2, ax2 = plt.subplots(figsize=(5, 4))
        sem_counts.plot(kind="bar", ax=ax2, color="#C8A27E")
        ax2.set_ylabel("Number of Documents")
        plt.xticks(rotation=45, ha='right')
        
        fig2.patch.set_alpha(0.0)
        ax2.patch.set_alpha(0.0)
        st.pyplot(fig2)
        plt.close(fig2)

    st.divider()

    # --- ROW 2: NEW GRAPHS (Donut & Line Charts) ---
    col_chart3, col_chart4 = st.columns(2)

    # Chart 3: Course Distribution (Donut Chart)
    with col_chart3:
        st.subheader("Course Distribution")
        course_counts = df["course"].value_counts()
        
        fig3, ax3 = plt.subplots(figsize=(5, 4))
        # Warm academia colors for the pie slices
        theme_colors = ['#6B2D3A', '#B98A84', '#C8A27E', '#2E1F1B']
        
        # Create pie chart
        wedges, texts, autotexts = ax3.pie(
            course_counts, 
            labels=course_counts.index, 
            autopct='%1.1f%%', 
            startangle=90, 
            colors=theme_colors
        )
        
        # Draw a circle in the center to turn the pie chart into a Donut chart
        centre_circle = plt.Circle((0,0), 0.70, fc='#F3EBDD') # Matches your background color
        fig3.gca().add_artist(centre_circle)
        
        # Make the text inside the donut readable
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_weight('bold')

        ax3.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        fig3.patch.set_alpha(0.0)
        st.pyplot(fig3)
        plt.close(fig3)

    # Chart 4: Cumulative Uploads (Time-Series Line Chart)
    with col_chart4:
        st.subheader("Growth Over Time")
        
        # Sort data by date and calculate cumulative sum
        df_time = df.sort_values("created_at")
        df_time['cumulative'] = range(1, len(df_time) + 1)
        
        fig4, ax4 = plt.subplots(figsize=(5, 4))
        
        # Plot line chart with markers
        ax4.plot(
            df_time['created_at'].dt.date, 
            df_time['cumulative'], 
            color="#6B2D3A", 
            marker='o', 
            linestyle='-', 
            linewidth=2
        )
        
        ax4.set_ylabel("Total Resources Shared")
        plt.xticks(rotation=45, ha='right')
        
        # Add a subtle grid for better readability
        ax4.grid(True, axis='y', linestyle='--', alpha=0.5)
        
        fig4.patch.set_alpha(0.0)
        ax4.patch.set_alpha(0.0)
        st.pyplot(fig4)
        plt.close(fig4)

    st.divider()

    # --- TOP CONTRIBUTORS TABLE ---
    st.subheader("Top Contributors")
    contributors = df["uploader_name"].value_counts().head(5)
    
    st.dataframe(
        contributors.rename("Documents Uploaded"),
        use_container_width=True
    )


# --------------------------------------------------
# MAIN APPLICATION
# --------------------------------------------------

def main():

    if st.session_state.user is None:
        authentication_page()
        return

    # Set up session state to remember the current page
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Home"

    st.sidebar.title("ChristNotes")
    st.sidebar.caption("Academic Resource Hub")
    
    st.sidebar.write("") # Little bit of spacing
    
    # Navigation Buttons
    if st.sidebar.button("Home", use_container_width=True):
        st.session_state.current_page = "Home"
        
    if st.sidebar.button("Explore Notes", use_container_width=True):
        st.session_state.current_page = "Explore Notes"
        
    if st.sidebar.button("Upload Notes", use_container_width=True):
        st.session_state.current_page = "Upload Notes"
        
    if st.sidebar.button("Analytics", use_container_width=True):
        st.session_state.current_page = "Analytics"

    st.sidebar.divider()

    # Injecting the CSS right above the box
    st.sidebar.markdown(
        """
        <style>
        /* Force Dusty Rose on the sidebar container */
        [data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"] {
            background-color: #B98A84 !important;
            border-color: #B98A84 !important;
        }
        /* Strip Streamlit's invisible background layers */
        [data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stVerticalBlock"] {
            background-color: transparent !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # The Container
    with st.sidebar.container(border=True):
        st.write("Logged in as:")
        st.write(f"**{st.session_state.user.email}**")
        
        empty_space, button_col = st.columns([1.2, 1]) 
        
        with button_col:
            if st.button("Logout", use_container_width=True):
                sb.auth.sign_out()
                st.session_state.user = None
                st.rerun()

    # Page Routing 
    if st.session_state.current_page == "Home":
        home_page()
    elif st.session_state.current_page == "Explore Notes":
        explore_page()
    elif st.session_state.current_page == "Upload Notes":
        upload_page()
    elif st.session_state.current_page == "Analytics":
        analytics_page()

if __name__ == "__main__":
    main()
