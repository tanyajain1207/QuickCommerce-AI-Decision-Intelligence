#!/usr/bin/env python3
"""
Master Report Builder conforming strictly to JIIT Capstone Project Guidelines:
- Template: final capstone project report template (1).pdf
- Cover Page: Sample front page MajorProject-Jaypee Institute of Information Technology.docx.pdf
- Font: Times New Roman, 12pt body, 1.5 line spacing, 2cm margins
- Team: Tanya Jain (23104034), Tanmay Tiwari (23104032), Tanishq Jain (23104060)
- Supervisor: Dr. Diksha Chawla
"""

import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

DOCS_DIR = r"D:\Desktop\Major Project Updated\Major Project\docs"
FIG_DIR = os.path.join(DOCS_DIR, "figures")
OUT_DOCX = os.path.join(DOCS_DIR, "MAJOR_PROJECT_REPORT.docx")

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>'))

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def format_row(row, bg_hex=None, bold=False, font_size=10.5, align=WD_ALIGN_PARAGRAPH.LEFT):
    for cell in row.cells:
        if bg_hex:
            set_cell_background(cell, bg_hex)
        set_cell_margins(cell, top=120, bottom=120, left=150, right=150)
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        for p in cell.paragraphs:
            p.alignment = align
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.space_before = Pt(2)
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(font_size)
                r.bold = bold

def add_header(doc, text, level):
    p = doc.add_paragraph()
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.bold = True
    
    if level == 1:
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(8)
        run.font.size = Pt(16)
        run.font.color.rgb = RGBColor(15, 23, 42) # Dark navy
    elif level == 2:
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        run.font.size = Pt(14)
        run.font.color.rgb = RGBColor(30, 41, 59)
    else:
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        run.font.size = Pt(12)
        run.font.color.rgb = RGBColor(51, 65, 85)
    return p

def add_p(doc, text="", space_after=6, bold=False, italic=False, align=WD_ALIGN_PARAGRAPH.LEFT):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.space_before = Pt(0)
    if text:
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        r.bold = bold
        r.italic = italic
    return p

def add_bullet(doc, text, bold_prefix="", space_after=4):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.line_spacing = 1.3
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.space_before = Pt(0)
    if bold_prefix:
        r_b = p.add_run(bold_prefix)
        r_b.font.name = 'Times New Roman'
        r_b.font.size = Pt(12)
        r_b.bold = True
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    return p

def add_table_data(doc, headers, rows_data, col_widths=None):
    t = doc.add_table(rows=len(rows_data)+1, cols=len(headers))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    
    # Headers
    hdr_row = t.rows[0]
    for i, h in enumerate(headers):
        hdr_row.cells[i].text = h
    format_row(hdr_row, bg_hex="1E293B", bold=True, font_size=10, align=WD_ALIGN_PARAGRAPH.LEFT)
    for cell in hdr_row.cells:
        for p in cell.paragraphs:
            for r in p.runs:
                r.font.color.rgb = RGBColor(255, 255, 255)
                
    # Rows
    for r_idx, r_data in enumerate(rows_data):
        row = t.rows[r_idx+1]
        bg = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(r_data):
            row.cells[c_idx].text = str(val)
        format_row(row, bg_hex=bg, bold=False, font_size=10, align=WD_ALIGN_PARAGRAPH.LEFT)
        
    if col_widths:
        for row in t.rows:
            for idx, w in enumerate(col_widths):
                row.cells[idx].width = Cm(w)
                
    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    return t

def add_figure_image(doc, img_path, caption, width_in=6.0):
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(4)
        run_img = p_img.add_run()
        run_img.add_picture(img_path, width=Inches(width_in))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(12)
        r_cap = p_cap.add_run(caption)
        r_cap.font.name = 'Times New Roman'
        r_cap.font.size = Pt(10.5)
        r_cap.italic = True
        r_cap.bold = True

print("Helper functions initialized. Generating full report...")

def generate_full_capstone_report():
    doc = docx.Document()
    
    # ── Page Setup (A4, 2 cm margins on all sides) ──
    for sec in doc.sections:
        sec.page_width = Cm(21.0)
        sec.page_height = Cm(29.7)
        sec.top_margin = Cm(2.0)
        sec.bottom_margin = Cm(2.0)
        sec.left_margin = Cm(2.0)
        sec.right_margin = Cm(2.0)
        sec.header_distance = Cm(1.2)
        sec.footer_distance = Cm(1.2)
        
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Times New Roman'
    style_normal.font.size = Pt(12)
    style_normal.paragraph_format.line_spacing = 1.5
    
    # =========================================================================
    # PRELIMINARY PAGES
    # =========================================================================
    
    # 1. COVER PAGE (Standardized Institutional Format from Sample Front Page)
    p_inst = add_p(doc, "Jaypee Institute of Information Technology, Noida", space_after=2, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    p_inst.runs[0].font.size = Pt(16)
    
    p_dept = add_p(doc, "Department of Computer Science & Engineering and IT", space_after=36, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    p_dept.runs[0].font.size = Pt(14)
    
    p_ttl_label = add_p(doc, "MAJOR PROJECT REPORT ON", space_after=12, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    p_ttl_label.runs[0].font.size = Pt(12)
    p_ttl_label.runs[0].font.color.rgb = RGBColor(100, 116, 139)
    
    p_proj = add_p(doc, "AI-Powered Business Decision Intelligence System\nfor Quick-Commerce Operations", space_after=36, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    p_proj.runs[0].font.size = Pt(18)
    p_proj.runs[0].font.color.rgb = RGBColor(15, 23, 42)
    
    p_sub = add_p(doc, "Submitted in partial fulfillment of the requirements for the award of the degree of\nBachelor of Technology in Computer Science & Engineering / Information Technology", space_after=40, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    p_sub.runs[0].font.size = Pt(11)
    
    # Team Table
    add_p(doc, "Submitted by:", space_after=6, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT)
    team_table_data = [
        ["23104034", "Tanya Jain", "B.Tech IT (8th Sem)"],
        ["23104032", "Tanmay Tiwari", "B.Tech IT (8th Sem)"],
        ["23104060", "Tanishq Jain", "B.Tech CS&E (8th Sem)"]
    ]
    add_table_data(doc, ["Enrolment No.", "Name of Student", "Program & Semester"], team_table_data, [4.5, 6.5, 6.0])
    
    add_p(doc, "", space_after=12)
    add_p(doc, "Under the Supervision of:", space_after=2, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT)
    p_sup = add_p(doc, "Dr. Diksha Chawla", space_after=2, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT)
    p_sup.runs[0].font.size = Pt(13)
    add_p(doc, "Assistant Professor, Department of CSE & IT\nJaypee Institute of Information Technology, Noida", space_after=36, align=WD_ALIGN_PARAGRAPH.LEFT)
    
    p_foot = add_p(doc, "Course Name: Major Project (15B29CI692)  |  Academic Year: 2025 – 2026", space_after=0, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    p_foot.runs[0].font.size = Pt(11)
    
    doc.add_page_break()
    
    # 2. CERTIFICATE OF APPROVAL
    add_header(doc, "CERTIFICATE OF APPROVAL", level=1)
    add_p(doc, "This is to certify that the project report entitled \"AI-Powered Business Decision Intelligence System for Quick-Commerce Operations\", submitted by Tanya Jain (Enrolment No. 23104034), Tanmay Tiwari (Enrolment No. 23104032), and Tanishq Jain (Enrolment No. 23104060) in partial fulfillment of the requirements for the award of the degree of Bachelor of Technology in Computer Science & Engineering / Information Technology at Jaypee Institute of Information Technology, Noida, is an authentic record of the work carried out by them under my supervision and guidance.", space_after=18)
    
    add_p(doc, "To the best of my knowledge, the matter embodied in this project report has not been submitted to any other University / Institute for the award of any Degree or Diploma.", space_after=48)
    
    # Signature rows
    sig_table = doc.add_table(rows=2, cols=2)
    sig_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    sig_table.rows[0].cells[0].text = "______________________________\nDr. Diksha Chawla\n(Project Supervisor)\nDepartment of CSE & IT\nJIIT Noida"
    sig_table.rows[0].cells[1].text = "______________________________\nHead of the Department\nDepartment of CSE & IT\nJaypee Institute of Information Technology\nNoida, Uttar Pradesh"
    sig_table.rows[1].cells[0].text = "Date: ________________________"
    sig_table.rows[1].cells[1].text = "Date: ________________________"
    for r in sig_table.rows:
        for c in r.cells:
            for p in c.paragraphs:
                p.paragraph_format.line_spacing = 1.3
                for run in p.runs:
                    run.font.name = 'Times New Roman'
                    run.font.size = Pt(11)
                    
    doc.add_page_break()
    
    # 3. DECLARATION OF ORIGINALITY
    add_header(doc, "DECLARATION OF ORIGINALITY", level=1)
    add_p(doc, "We hereby declare that the work presented in this Major Project Report entitled \"AI-Powered Business Decision Intelligence System for Quick-Commerce Operations\" is an authentic record of our own original work carried out under the supervision of Dr. Diksha Chawla, Department of Computer Science & Engineering and Information Technology, Jaypee Institute of Information Technology, Noida.", space_after=16)
    
    add_p(doc, "We have adequately acknowledged and cited all sources of ideas, text, empirical data, and mathematical models that were consulted or adapted from existing literature. This work does not infringe upon any intellectual property rights or copyright laws. Neither this report nor any significant part of it has been previously submitted to this or any other academic institution for any degree, diploma, or certificate.", space_after=36)
    
    decl_table = doc.add_table(rows=4, cols=3)
    decl_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    decl_table.rows[0].cells[0].text = "Signature: __________________"
    decl_table.rows[0].cells[1].text = "Signature: __________________"
    decl_table.rows[0].cells[2].text = "Signature: __________________"
    decl_table.rows[1].cells[0].text = "Tanya Jain"
    decl_table.rows[1].cells[1].text = "Tanmay Tiwari"
    decl_table.rows[1].cells[2].text = "Tanishq Jain"
    decl_table.rows[2].cells[0].text = "Enrolment No: 23104034"
    decl_table.rows[2].cells[1].text = "Enrolment No: 23104032"
    decl_table.rows[2].cells[2].text = "Enrolment No: 23104060"
    decl_table.rows[3].cells[0].text = "Date: _______________"
    decl_table.rows[3].cells[1].text = "Date: _______________"
    decl_table.rows[3].cells[2].text = "Date: _______________"
    for r in decl_table.rows:
        for c in r.cells:
            for p in c.paragraphs:
                p.paragraph_format.line_spacing = 1.2
                for run in p.runs:
                    run.font.name = 'Times New Roman'
                    run.font.size = Pt(11)

    doc.add_page_break()
    
    # 4. ACKNOWLEDGEMENTS
    add_header(doc, "ACKNOWLEDGEMENTS", level=1)
    add_p(doc, "We express our profound gratitude and heartfelt respect to our supervisor, Dr. Diksha Chawla, Assistant Professor, Department of Computer Science & Engineering and Information Technology, Jaypee Institute of Information Technology, Noida, for her exemplary guidance, sustained encouragement, and insightful technical critiques throughout the ideation, system design, and implementation stages of this Major Project.", space_after=14)
    add_p(doc, "We extend our sincere thanks to the Head of the Department, Department of CSE & IT, for providing the necessary infrastructural facilities, laboratory resources, and computing environment that enabled the execution and evaluation of the machine learning pipelines and decision intelligence frameworks presented in this report.", space_after=14)
    add_p(doc, "We also express our indebtedness to all faculty members of the Department of Computer Science & Engineering and Information Technology for imparting the foundational principles of database engineering, statistical machine learning, algorithms, and software development that underpinned this work.", space_after=14)
    add_p(doc, "Finally, we place on record our deepest appreciation to our parents and peers for their unyielding moral support, patience, and understanding during the intensive development and experimental phases of this project.", space_after=24)
    
    add_p(doc, "Tanya Jain (23104034)\nTanmay Tiwari (23104032)\nTanishq Jain (23104060)", bold=True, align=WD_ALIGN_PARAGRAPH.RIGHT)

    doc.add_page_break()
    
    # 5. ABSTRACT
    add_header(doc, "ABSTRACT", level=1)
    add_p(doc, "The hyper-competitive quick-commerce industry in India—pioneered by platforms such as Blinkit, Zepto, and Swiggy Instamart—operates under stringent 10-to-15 minute delivery Service Level Agreements (SLAs). While dark stores generate millions of transactional records across orders, inventory logs, rider dispatches, and customer sentiment, store managers face an acute \"Information-Rich, Action-Poor\" dilemma. Traditional Business Intelligence (BI) dashboards passively visualize historical KPIs but fail to diagnose underlying root causes or prescribe timely operational interventions. Conversely, raw generative Large Language Models (LLMs) suffer from stochastic hallucinations and cannot be entrusted with ungrounded financial or inventory computations.", space_after=14)
    add_p(doc, "This project presents an enterprise-grade, end-to-end AI-Powered Business Decision Intelligence System specifically engineered for quick-commerce dark-store operations. The system adopts an anti-hallucination hybrid architecture consisting of five decoupled layers: (1) an 11-table relational MySQL 8.0 schema storing 54,900+ sales and delivery records across 10 metropolitan dark stores; (2) a deterministic SQL analytics engine executing 15 parameterized business intelligence queries with window functions, Common Table Expressions (CTEs), and month-over-month lag aggregations; (3) a predictive machine learning layer integrating an XGBoost 7-day SKU demand forecasting model with recursive lag features, an XGBoost customer churn classifier achieving 94.40% accuracy and 0.8357 ROC-AUC across 500 behavioral profiles, and a dynamic delivery fulfillment regressor with Mean Absolute Error of ±2.74 minutes; (4) a grounded generative AI interpretation engine powered by Google Gemini 2.5 Flash with a sub-second deterministic rule-based fail-safe; and (5) a glassmorphic Streamlit web operations console paired with an automated multi-channel operational alert dispatcher.", space_after=14)
    add_p(doc, "Experimental validation conducted across healthy, crisis, and margin-eroded dark stores demonstrates that the system reduces root-cause diagnostic latency from 4–6 hours to under 65 seconds. By proactively predicting stockout trajectories 7 days in advance and identifying at-risk high-value customers, the platform establishes a closed-loop prescriptive decision intelligence paradigm with demonstrated economic viability and societal sustainability.", space_after=14)
    add_p(doc, "Keywords: Quick-Commerce, Dark Stores, Decision Intelligence, Anti-Hallucination AI, XGBoost, Predictive Demand Forecasting, Customer Churn, Service Level Agreement (SLA), Streamlit.", italic=True, bold=True)

    doc.add_page_break()
    
    # 6. TABLE OF CONTENTS
    add_header(doc, "TABLE OF CONTENTS", level=1)
    toc_data = [
        ["Certificate of Approval", "ii"],
        ["Declaration of Originality", "iii"],
        ["Acknowledgements", "iv"],
        ["Abstract", "v"],
        ["List of Figures", "viii"],
        ["List of Tables", "ix"],
        ["List of Abbreviations", "x"],
        ["CHAPTER 1: INTRODUCTION", "1"],
        ["  1.1 Background & Industry Motivation", "1"],
        ["  1.2 Problem Definition and Technical Objectives", "3"],
        ["  1.3 Social, Economic & Environmental Relevance", "5"],
        ["  1.4 Project Plan, WBS, Timeline & Roles", "6"],
        ["  1.5 Scope and Delimitations", "9"],
        ["CHAPTER 2: LITERATURE SURVEY", "11"],
        ["  2.1 Critical Review of Business Intelligence & Analytics", "11"],
        ["  2.2 Summary Comparison of State-of-the-Art Approaches", "14"],
        ["  2.3 Identification of Research & Operational Gaps", "16"],
        ["CHAPTER 3: SYSTEM DESIGN & METHODOLOGY", "18"],
        ["  3.1 Design Considerations & Multi-Disciplinary Constraints", "18"],
        ["  3.2 Five-Layer Decision Intelligence Architecture", "20"],
        ["  3.3 Mathematical Modelling & Algorithm Formulation", "24"],
        ["  3.4 Tool and Technology Selection Justification", "28"],
        ["CHAPTER 4: IMPLEMENTATION & TESTING", "31"],
        ["  4.1 Development Details & Subsystem Execution", "31"],
        ["  4.2 Experimental & Computational Setup", "36"],
        ["  4.3 Verification Test Cases & Functional Validation", "38"],
        ["  4.4 Safety Protocols, Anti-Hallucination & Cybersecurity", "41"],
        ["CHAPTER 5: RESULTS & DISCUSSION", "44"],
        ["  5.1 Empirical Performance Analysis of ML Models", "44"],
        ["  5.2 Validation Against Defined Project Objectives", "49"],
        ["  5.3 Economic Analysis, Bill of Materials & ROI", "51"],
        ["  5.4 Comparative Evaluation with Existing BI Standards", "54"],
        ["CHAPTER 6: CONCLUSION & FUTURE SCOPE", "56"],
        ["  6.1 Summary of Technical Achievements", "56"],
        ["  6.2 Societal & Environmental Impact Statement", "57"],
        ["  6.3 System Limitations", "58"],
        ["  6.4 Future Research & Roadmap", "59"],
        ["REFERENCES (IEEE Standards)", "61"],
        ["ANNEXURES", "64"],
        ["  Annexure I: Plagiarism Statement & Academic Integrity", "64"],
        ["  Annexure II: Program Outcomes (PO/PSO) Mapping Matrix", "65"],
        ["  Annexure III: Project Outcomes & Technical Deliverables", "67"],
        ["  Annexure IV: Sustainability & Environmental Assessment", "68"],
        ["  Annexure V: Team Member Contributions Breakdown", "69"],
    ]
    add_table_data(doc, ["Section / Chapter Title", "Page No."], toc_data, [14.0, 3.0])

    doc.add_page_break()
    
    # 7. LIST OF FIGURES & LIST OF TABLES
    add_header(doc, "LIST OF FIGURES", level=1)
    fig_list = [
        ["Figure 3.1", "5-Layer AI-Powered Business Decision Intelligence Architecture", "21"],
        ["Figure 3.2", "Normalized Relational Database Schema & ML Entity Relationships", "23"],
        ["Figure 3.3", "Anti-Hallucination Grounded Prompt Generation Workflow", "27"],
        ["Figure 4.1", "Interactive Streamlit Operations Console (Real-Time Store Health View)", "35"],
        ["Figure 5.1", "Predictive Machine Learning Model Validation Curves (ROC & ETA Scatter)", "46"],
        ["Figure 5.2", "SKU-Level 7-Day Demand Trajectory & Restock Warning Curves (Store 3)", "48"],
        ["Figure 5.3", "Delivery Delay Risk Distribution across 10 Metropolitan Dark Stores", "50"]
    ]
    add_table_data(doc, ["Figure No.", "Figure Caption / Description", "Page No."], fig_list, [3.0, 11.5, 2.5])
    
    add_p(doc, "", space_after=12)
    add_header(doc, "LIST OF TABLES", level=1)
    tbl_list = [
        ["Table 1.1", "Measurable Project Objectives & Success Criteria", "4"],
        ["Table 1.2", "Work Breakdown Structure (WBS) & Task Ownership", "7"],
        ["Table 1.3", "Project Execution Timeline & Milestone Schedule", "8"],
        ["Table 2.1", "Comparison of Existing BI Platforms vs Proposed System", "15"],
        ["Table 3.1", "Relational Database Schema Table Inventory (MySQL 8.0)", "22"],
        ["Table 3.2", "15 Business Intelligence SQL Analytics Query Directory", "24"],
        ["Table 4.1", "Experimental Hardware and Software Specifications", "37"],
        ["Table 4.2", "System Verification & Acceptance Test Cases", "39"],
        ["Table 5.1", "Customer Churn Classifier Performance Metrics (XGBoost)", "45"],
        ["Table 5.2", "Delivery Fulfillment Regressor Performance Metrics", "47"],
        ["Table 5.3", "Bill of Materials (BOM) & Cloud Deployment Cost Structure", "52"],
        ["Table 5.4", "Cost-Benefit & Economic Value Quantification Analysis", "53"],
        ["Table A.1", "Program Outcomes (PO1-PO12) & PSO Mapping Matrix", "66"]
    ]
    add_table_data(doc, ["Table No.", "Table Title / Description", "Page No."], tbl_list, [3.0, 11.5, 2.5])

    doc.add_page_break()
    
    # 8. LIST OF ABBREVIATIONS
    add_header(doc, "LIST OF ABBREVIATIONS", level=1)
    abbr_data = [
        ["AI", "Artificial Intelligence"],
        ["AOV", "Average Order Value"],
        ["API", "Application Programming Interface"],
        ["AUC", "Area Under the Curve (Receiver Operating Characteristic)"],
        ["BI", "Business Intelligence"],
        ["BOM", "Bill of Materials"],
        ["CAGR", "Compound Annual Growth Rate"],
        ["CRM", "Customer Relationship Management"],
        ["CTE", "Common Table Expression (SQL)"],
        ["ETA", "Estimated Time of Arrival"],
        ["GBR", "Gradient Boosting Regressor"],
        ["JSON", "JavaScript Object Notation"],
        ["KPI", "Key Performance Indicator"],
        ["LLM", "Large Language Model"],
        ["MAE", "Mean Absolute Error"],
        ["ML", "Machine Learning"],
        ["MoM", "Month-over-Month"],
        ["ODBC", "Open Database Connectivity"],
        ["PO", "Purchase Order / Program Outcome"],
        ["PSO", "Program Specific Outcome"],
        ["RDBMS", "Relational Database Management System"],
        ["RF", "Random Forest"],
        ["RMSE", "Root Mean Squared Error"],
        ["ROC", "Receiver Operating Characteristic"],
        ["SKU", "Stock Keeping Unit"],
        ["SLA", "Service Level Agreement"],
        ["SQL", "Structured Query Language"],
        ["UI", "User Interface"],
        ["WBS", "Work Breakdown Structure"],
        ["XGBoost", "eXtreme Gradient Boosting"]
    ]
    add_table_data(doc, ["Abbreviation", "Full Expanded Form"], abbr_data, [4.5, 12.5])

    doc.add_page_break()

    print("Preliminary pages completed. Building Chapters 1 through 6...")
    return doc

print("Preliminary builder defined.")

if __name__ == "__main__":
    import report_chapters
    print("Initializing document...")
    doc = generate_full_capstone_report()
    
    print("Building Chapter 1...")
    report_chapters.build_chapter_1(doc)
    
    print("Building Chapters 2 and 3...")
    report_chapters.build_chapter_2_and_3(doc)
    
    print("Building Chapters 4, 5, 6, References, and Annexures...")
    report_chapters.build_chapter_4_5_6_and_annexures(doc)
    
    out_path = r"D:\Desktop\Major Project Updated\Major Project\docs\MAJOR_PROJECT_REPORT.docx"
    doc.save(out_path)
    print(f"\n==========================================================================")
    print(f"  SUCCESS: Formal College Capstone Report successfully compiled!")
    print(f"  Output Path: {out_path}")
    print(f"==========================================================================\n")
