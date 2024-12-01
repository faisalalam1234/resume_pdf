import streamlit as st
from fpdf import FPDF
import os

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

# Streamlit App
st.title("📝 Stylish Resume Builder")
st.write("Fill out the details below to generate your professional resume!")

# Add "About Us" Section with Expandable
with st.expander("👨‍💻 About Us"):
    st.write("""
    Hi! I'm Faisal Alam, a passionate and creative individual specializing in video editing, 3D animation, and visual effects. With a keen eye for detail and a love for storytelling, I aim to bring out the best in every project I work on.

With experience in using powerful tools like Blender, Premiere Pro, and After Effects, I am dedicated to crafting engaging visual content that leaves a lasting impact. Whether you're looking to enhance your online presence or create something truly unique, I’m here to help bring your ideas to life.

Join me in the exciting journey of turning your visions into reality!   
             
             We help you create a stylish resume quickly.
    Our tool allows you to customize your resume with ease.
    Create a standout resume today!
    """)

# Add "Contact Us" Section with Expandable
with st.expander("📬 Contact Us"):
    st.write("""
    Email: [ka9190430@gmail.com](mailto:ka9190430@gmail.com)
    Phone: 9219711509
    Reach out for any queries!
    """)

# Input Form for Resume Details
st.header("👤 Personal Information")
name = st.text_input("Full Name").strip()  # Remove extra spaces
email = st.text_input("Email").strip()  # Remove extra spaces
phone = st.text_input("Phone Number").strip()  # Remove extra spaces

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
