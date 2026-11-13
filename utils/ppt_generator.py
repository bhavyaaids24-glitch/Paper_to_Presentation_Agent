import io
import re
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

def create_ppt(content: str, paper_name: str = "Research Paper") -> bytes:
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Split generated text into slide sections by Markdown level-2 headings.
    sections = re.split(r"(?m)^##\s+", content.strip())
    sections = [s.strip() for s in sections if s.strip()]

    if not sections:
        sections = [content.strip()]

    for section in sections[:15]:
        lines = [line.strip() for line in section.splitlines() if line.strip()]
        title = lines[0].lstrip("#").strip()[:100] if lines else "Research Paper"
        bullets = []
        for line in lines[1:]:
            cleaned = re.sub(r"^[-*•]\s*", "", line).strip()
            if cleaned:
                bullets.append(cleaned)

        slide = prs.slides.add_slide(prs.slide_layouts[6])
        title_box = slide.shapes.add_textbox(Inches(0.65), Inches(0.45), Inches(12), Inches(0.8))
        title_tf = title_box.text_frame
        title_tf.text = title
        title_run = title_tf.paragraphs[0].runs[0]
        title_run.font.size = Pt(28)
        title_run.font.bold = True
        title_run.font.color.rgb = RGBColor(31, 78, 121)

        body_box = slide.shapes.add_textbox(Inches(0.9), Inches(1.55), Inches(11.5), Inches(5.3))
        body_tf = body_box.text_frame
        body_tf.word_wrap = True

        if not bullets:
            bullets = ["Refer to the research paper for details."]
        for index, bullet in enumerate(bullets[:7]):
            paragraph = body_tf.paragraphs[0] if index == 0 else body_tf.add_paragraph()
            paragraph.text = bullet
            paragraph.level = 0
            paragraph.font.size = Pt(20)
            paragraph.space_after = Pt(14)

    output = io.BytesIO()
    prs.save(output)
    output.seek(0)
    return output.getvalue()
