import os
from fpdf import FPDF

class PersonalizedLaunchPass(FPDF):
    def __init__(self, name):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.name = name

    def header(self):
        self.image("final_invite_template.jpg", x=0, y=0, w=210, h=297)  # ✅ Final branded background

    def generate(self, output_path="APIT-Digital-Pass.pdf"):
        self.add_page()
        self.set_font("Helvetica", "", 16)
        self.set_text_color(255, 255, 255)

        # ✅ Position between logo and main paragraph
        self.set_xy(0, 63)
        self.cell(w=210, h=10, txt=f"Dear {self.name},", ln=True, align='C')

        self.output(output_path)
        return output_path


def create_pass_pdf(name, company):
    print("Looking for:", os.path.exists("final_invite_template.jpg"))
    pdf = PersonalizedLaunchPass(name)
    return pdf.generate("APIT-Digital-Pass.pdf")

# Example usage
if __name__ == "__main__":
    pdf = PersonalizedLaunchPass("Deependra Singh")
    pdf.generate("Refined-Centered-Launch-Pass.pdf")
