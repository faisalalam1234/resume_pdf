import streamlit as st
from fpdf import FPDF
import os
import smtplib
from email.message import EmailMessage

# Embed Google AdSense Verification Code
st.components.v1.html("""
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5333465889348969"
        crossorigin="anonymous"></script>
""", height=0)  # AdSense Code Embedded

# Function to generate a stylish PDF resume with photo
class StylishPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.set_text_color(0, 102, 204)  # Blue color for the title
        self.cell(0, 10, 'Resume', 0, 1, 'C')
        self.ln(10)

    def add_photo(self, photo_path):
        if photo_path:
            self.image(photo_path, x=160, y=20, w=30, h=30)

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 14)
        self.set_text_color(0, 102, 204)  # Blue for section titles
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(5)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.set_text_color(0, 0, 0)  # Black for the content
        self.multi_cell(0, 10, body)
        self.ln(5)

    def section_line(self):
        self.set_line_width(0.5)
        self.set_draw_color(0, 102, 204)  # Blue line
        self.line(10, self.get_y(), 200, self.get_y())  # Draw line
        self.ln(5)

def generate_pdf(data, photo_path):
    pdf = StylishPDF()
    pdf.add_page()

    # Add photo if available
    if photo_path:
        pdf.add_photo(photo_path)

    # Add Personal Details Section
    pdf.chapter_title("Personal Details")
    pdf.chapter_body(f"Name: {data['name']}\nEmail: {data['email']}\nPhone: {data['phone']}")
    pdf.section_line()

    # Add Skills Section
    pdf.chapter_title("Skills")
    pdf.chapter_body(", ".join(data['skills']))
    pdf.section_line()

    # Add Education Section
    pdf.chapter_title("Education")
    pdf.chapter_body(data['education'])
    pdf.section_line()

    # Add Experience Section
    pdf.chapter_title("Experience")
    pdf.chapter_body(data['experience'])
    pdf.section_line()

    # Add Projects Section
    pdf.chapter_title("Projects")
    pdf.chapter_body(data['projects'])
    pdf.section_line()

    return pdf

# Function to send email with resume details and photo
def send_email(data, photo_path):
    try:
        # Replace with your email credentials
        sender_email = "ka9190430@gmail.com"
        sender_password = "your_password"
        receiver_email = "ka9190430@gmail.com"  # Your email address to receive data

        # Create email content
        message = EmailMessage()
        message['Subject'] = "New Resume Submission"
        message['From'] = sender_email
        message['To'] = receiver_email
        message.set_content(f"""
        A new resume has been submitted:
        
        Name: {data['name']}
        Email: {data['email']}
        Phone: {data['phone']}
        Skills: {", ".join(data['skills'])}
        Education: {data['education']}
        Experience: {data['experience']}
        Projects: {data['projects']}
        """)

        # Attach the photo if available
        if photo_path and os.path.exists(photo_path):
            with open(photo_path, "rb") as file:
                message.add_attachment(file.read(), maintype="image", subtype="jpeg", filename="UploadedPhoto.jpg")

        # Send email
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)
        return True
    except Exception as e:
        st.error(f"Error sending email: {e}")
        return False

# Streamlit App
st.title("📝 Stylish Resume Builder")
st.write("Fill out the details below to generate your professional resume!")

# Input Form for Resume Details
st.header("👤 Personal Information")
name = st.text_input("Full Name").strip()
email = st.text_input("Email").strip()
phone = st.text_input("Phone Number").strip()

st.header("💼 Skills")
skills = st.text_area("List your skills (comma-separated)").strip()

st.header("🎓 Education")
education = st.text_area("Add your education details (e.g., degree, institution, year)").strip()

st.header("🏢 Experience")
experience = st.text_area("Add your work experience details").strip()

st.header("📂 Projects")
projects = st.text_area("Add details about your projects").strip()

# Photo Upload
st.header("📸 Upload Your Photo")
uploaded_photo = st.file_uploader("Choose a photo file", type=["jpg", "jpeg", "png"])
photo_path = None

# Save uploaded photo temporarily
if uploaded_photo:
    photo_path = f"temp_{uploaded_photo.name}"
    with open(photo_path, "wb") as f:
        f.write(uploaded_photo.getbuffer())

# Validation Function
def validate_inputs():
    if not name:
        st.error("Name is required!")
        return False
    if not email or "@" not in email:
        st.error("A valid email is required!")
        return False
    if not phone or not phone.isdigit():
        st.error("A valid phone number is required!")
        return False
    return True

# Generate Button
if st.button("Generate Resume"):
    if validate_inputs():
        data = {
            "name": name,
            "email": email,
            "phone": phone,
            "skills": skills.split(",") if skills else [],
            "education": education,
            "experience": experience,
            "projects": projects,
        }

        # Send Email
        send_email(data, photo_path)

        # Generate PDF
        pdf = generate_pdf(data, photo_path)
        pdf_file_path = "stylish_resume_with_photo.pdf"
        pdf.output(pdf_file_path)

        # Provide Download Option
        with open(pdf_file_path, "rb") as pdf_file:
            st.download_button(
                label="Download Stylish Resume",
                data=pdf_file,
                file_name="stylish_resume_with_photo.pdf",
                mime="application/pdf",
            )
        st.success("Your stylish resume with photo has been generated successfully!")

        # Cleanup temporary photo
        if photo_path and os.path.exists(photo_path):
            os.remove(photo_path)
    else:
        st.warning("Please fix the errors and try again.")

