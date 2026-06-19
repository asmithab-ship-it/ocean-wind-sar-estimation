import os
from reportlab.lib.pagesizes import a4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def create_report():
    pdf_path = "../output/Ocean_Wind_SAR_Interim_Report.pdf"
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
    
    # Setup document structure
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=a4,
        rightMargin=40, leftMargin=40,
        topMargin=40, bottomMargin=40
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Technical Layout Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#1a365d'),
        spaceAfter=15
    )
    
    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#2b6cb0'),
        spaceBefore=18,
        spaceAfter=8,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        spaceAfter=10,
        alignment=4 # Justified
    )
    
    caption_style = ParagraphStyle(
        'CaptionCustom',
        parent=styles['Italic'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#4a5568'),
        alignment=1, # Centered
        spaceBefore=4,
        spaceAfter=12
    )
    
    img_placeholder_style = ParagraphStyle(
        'ImgText',
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#4a5568'),
        alignment=1
    )

    story = []
    
    # Header Banner
    story.append(Paragraph("TECHNICAL RESEARCH MILESTONE REPORT", ParagraphStyle('Sub', fontName='Helvetica-Bold', fontSize=9, textColor=colors.HexColor('#4a5568'), spaceAfter=4)))
    story.append(Paragraph("Ocean Wind Field Estimation Using SAR Imagery Over Tamil Nadu Coastal Region for Wind Farm Planning", title_style))
    story.append(Paragraph("Date: June 2026 | Status: Interim Submission", ParagraphStyle('Meta', fontName='Helvetica', fontSize=9, textColor=colors.HexColor('#718096'))))
    story.append(Spacer(1, 15))
    
    # 1. Introduction
    story.append(Paragraph("1. Introduction", h2_style))
    story.append(Paragraph("Offshore wind energy is one of the most promising renewable energy resources for meeting future energy demands. Accurate estimation of ocean wind fields is important for identifying suitable locations for offshore wind farms. Synthetic Aperture Radar (SAR) imagery provides high-resolution information about ocean surface conditions and can be used to estimate wind speed and direction over coastal waters.", body_style))
    story.append(Paragraph("This project focuses on estimating ocean wind fields along the Tamil Nadu coast using Sentinel-1 SAR imagery. The final objective is to develop an API-based system that allows users to provide a date and area of interest and obtain corresponding wind field vectors for the selected coastal region.", body_style))
    
    # 2. Problem Statement
    story.append(Paragraph("2. Problem Statement", h2_style))
    story.append(Paragraph("To develop a system for estimating ocean wind fields using Sentinel-1 SAR imagery over Indian coastal regions and provide wind vector information through an API for offshore wind farm planning applications.", body_style))
    
    # 3. Objectives
    story.append(Paragraph("3. Objectives", h2_style))
    story.append(Paragraph("• To collect and process Sentinel-1 SAR wind data.<br/>• To estimate offshore wind speed and direction.<br/>• To visualize wind vectors over coastal regions.<br/>• To validate generated wind data using reference datasets.<br/>• To develop an API that provides wind field vectors based on user-selected date and area of interest.", body_style))
    
    # 4. Study Area
    story.append(Paragraph("4. Study Area", h2_style))
    story.append(Paragraph("The study area selected for this work is the Tamil Nadu coastal region. Two different seasonal datasets were analyzed:", body_style))
    story.append(Paragraph("<b>December 2025 Dataset:</b> Northern Tamil Nadu Coast (Chennai–Pondicherry Shelf Region) covering Latitude 11.2° N to 12.8° N and Longitude 79.8° E to 81.6° E.", body_style))
    story.append(Paragraph("<b>August 2025 Dataset:</b> Southern Tamil Nadu Coast (Palk Strait and Rameswaram Region) covering Latitude 8.4° N to 9.9° N and Longitude 78.2° E to 80.0° E.", body_style))
    
    # 5. Methodology
    story.append(Paragraph("5. Methodology", h2_style))
    story.append(Paragraph("The workflow followed in this project includes collection of Sentinel-1 SAR wind datasets, data cleaning and preprocessing, wind speed and direction extraction, API development using FastAPI, wind vector visualization in QGIS, and validation using ERA5 reference data.", body_style))
    
    # 6. Work Completed
    story.append(Paragraph("6. Work Completed", h2_style))
    story.append(Paragraph("<b>6.1 Data Preparation and Cleaning:</b> A data preprocessing workflow was developed to handle raw wind datasets efficiently. The implemented scripts perform removal of unnecessary spaces in filenames, cleaning of special symbols, automatic standardization of column names, and removal of invalid records.", body_style))
    story.append(Paragraph("<b>6.2 API Backend Development:</b> A backend application was developed using FastAPI and Uvicorn to accept user query inputs and serve clean JSON format streams.", body_style))
    story.append(Paragraph("<b>6.3 Wind Field Visualization Using QGIS:</b> Wind field vectors generated from the processed datasets were visualized in QGIS with custom attribute-driven direction arrows and graded colors overlaying Bing Aerial maps.", body_style))
    
    # 7. Seasonal Analysis Results
    story.append(Paragraph("7.0 Seasonal Analysis Results", h2_style))
    story.append(Paragraph("<b>7.1 August 2025 Analysis:</b> The August dataset represents peak monsoon conditions over the southern Tamil Nadu coast. Wind speeds ranged from 6.5 m/s to 20.0 m/s with heavy monsoon-driven channels around the Palk Strait.", body_style))
    
    # Figure 1 Box
    f1_text = Paragraph("<br/><br/><b>[Image Attached: Screenshot 2026-06-08 220516.jpg]</b><br/>August 2025 Peak Monsoon Wind Vector Layout (QGIS)", img_placeholder_style)
    t1 = Table([[f1_text]], colWidths=[510], rowHeights=[90])
    t1.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#edf2f7')), ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e0')), ('ALIGN', (0,0), (-1,-1), 'CENTER'), ('VALIGN', (0,0), (-1,-1), 'MIDDLE')]))
    story.append(t1)
    story.append(Paragraph("Figure 1: Spatial representation of August monsoon vector fields and velocity grading patterns.", caption_style))
    
    story.append(Paragraph("<b>7.2 December 2025 Analysis:</b> The December dataset represents winter monsoon conditions over the northern Tamil Nadu coast. Wind speeds ranged from 1.2 m/s to 7.2 m/s, reflecting calm and stable wind vectors.", body_style))
    
    # Figure 2 Box
    f2_text = Paragraph("<br/><br/><b>[Image Attached: output image from qgis.jpg]</b><br/>December 2025 Winter Monsoonal Baseline Canvas (QGIS)", img_placeholder_style)
    t2 = Table([[f2_text]], colWidths=[510], rowHeights=[90])
    t2.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#edf2f7')), ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e0'))]))
    story.append(t2)
    story.append(Paragraph("Figure 2: QGIS layout tracking uniform flow headings across the northern shelf during December.", caption_style))
    
    # 8. Validation and Analysis
    story.append(Paragraph("8.0 Validation and Analysis", h2_style))
    story.append(Paragraph("<b>8.1 Wind Rose Analysis:</b> A Wind Rose diagram was generated using the December dataset to study wind direction patterns, showing dominant winds from the North-East matching the winter monsoon circulation.", body_style))
    
    # Figure 3 Box
    f3_text = Paragraph("<br/><br/><b>[Image Attached: site_windrose_corrected.jpg]</b><br/>December Offshore Polar Wind Rose Frequency Diagram", img_placeholder_style)
    t3 = Table([[f3_text]], colWidths=[510], rowHeights=[90])
    t3.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#edf2f7')), ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e0'))]))
    story.append(t3)
    story.append(Paragraph("Figure 3: Polar distribution diagram validating dominant northeasterly vector counts.", caption_style))
    
    story.append(Paragraph("<b>8.2 Scatter Plot Validation:</b> The estimated SAR-derived wind speeds were compared against ERA5 reference data. Points clustered tightly alongside the ideal diagonal line, indicating high reliability and accuracy.", body_style))
    
    # Figure 4 Box
    f4_text = Paragraph("<br/><br/><b>[Image Attached: validation scatter plot.png]</b><br/>SAR-Derived Velocity vs. ERA5 Reference Validation Scatter Plot", img_placeholder_style)
    t4 = Table([[f4_text]], colWidths=[510], rowHeights=[90])
    t4.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#edf2f7')), ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e0'))]))
    story.append(t4)
    story.append(Paragraph("Figure 4: Scatter validation plot displaying reliable linear fit consistency.", caption_style))
    
    # 9. Current Progress Status Table
    story.append(Paragraph("9.0 Current Progress Status", h2_style))
    table_data = [
        [Paragraph("<b>Task Description</b>", body_style), Paragraph("<b>Status</b>", body_style)],
        [Paragraph("Data Collection & Ingestion", body_style), Paragraph("<font color='#2f855a'><b>Completed</b></font>", body_style)],
        [Paragraph("Data Cleaning and Preprocessing Pipeline", body_style), Paragraph("<font color='#2f855a'><b>Completed</b></font>", body_style)],
        [Paragraph("FastAPI Backend Server Architecture", body_style), Paragraph("<font color='#2f855a'><b>Completed</b></font>", body_style)],
        [Paragraph("Wind Vector Generation", body_style), Paragraph("<font color='#2f855a'><b>Completed</b></font>", body_style)],
        [Paragraph("QGIS Visualization Layouts", body_style), Paragraph("<font color='#2f855a'><b>Completed</b></font>", body_style)],
        [Paragraph("December & August Dataset Analyses", body_style), Paragraph("<font color='#2f855a'><b>Completed</b></font>", body_style)],
        [Paragraph("Wind Rose & Scatter Plot Validation Charts", body_style), Paragraph("<font color='#2f855a'><b>Completed</b></font>", body_style)],
        [Paragraph("API Integration Refinement & Documentation", body_style), Paragraph("<font color='#c05621'><i>In Progress</i></font>", body_style)]
    ]
    stat_table = Table(table_data, colWidths=[330, 180])
    stat_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (1,0), colors.HexColor('#1a365d')),
        ('TEXTCOLOR', (0,0), (1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
    ]))
    # Quick color fix for table text headers
    table_data[0][0].style.textColor = colors.white
    table_data[0][1].style.textColor = colors.white
    
    story.append(stat_table)
    story.append(Spacer(1, 10))
    
    # 10. Conclusion
    story.append(Paragraph("10. Conclusion", h2_style))
    story.append(Paragraph("The project has successfully established a complete workflow for processing Sentinel-1 SAR wind data, generating wind field vectors, visualizing results in QGIS, and validating outputs using ERA5 data. Validation results indicate good agreement, confirming the high reliability of the proposed system architecture.", body_style))
    
    # Build Document
    doc.build(story)
    print(f"Success! Report generated and saved locally to: {pdf_path}")

if __name__ == '__main__':
    create_report()