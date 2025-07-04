import io
from datetime import datetime
from django.core.files.base import ContentFile
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas


def generate_driver_pay_pdf(driver_pay_data, driver, company_info=None):
    """
    Driver uchun PDF hisobot yaratish
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    styles = getSampleStyleSheet()
    story = []

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        alignment=TA_CENTER,
        spaceAfter=20,
        textColor=colors.black
    )
    
    header_style = ParagraphStyle(
        'HeaderStyle',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_LEFT,
        spaceAfter=6
    )

    # Company header
    if company_info:
        company_header_data = [
            [company_info.get('company_name', 'Company Name'), 'Driver: Orol Berdiyev'],
            [f"Phone: {company_info.get('phone', 'N/A')}", f"Report Date: {driver_pay_data['driver']['report_date']}"],
            [f"Fax: {company_info.get('fax', 'N/A')}", f"Search From: {driver_pay_data['driver']['search_from']}"],
            ['', f"Search To: {driver_pay_data['driver']['search_to']}"],
            ['', f"Status: {driver_pay_data['driver']['contact_number']}"]
        ]
    else:
        company_header_data = [
            ['Company Name', 'Driver: Orol Berdiyev'],
            ['Phone: N/A', f"Report Date: {driver_pay_data['driver']['report_date']}"],
            ['Fax: N/A', f"Search From: {driver_pay_data['driver']['search_from']}"],
            ['', f"Search To: {driver_pay_data['driver']['search_to']}"],
            ['', f"Status: {driver_pay_data['driver']['contact_number']}"]
        ]

    company_table = Table(company_header_data, colWidths=[3*inch, 3*inch])
    company_table.setStyle(TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(company_table)
    story.append(Spacer(1, 20))

    # Title
    title = Paragraph("Driver Pay Report", title_style)
    story.append(title)

    # Loads table header
    load_headers = ['Load #', 'Pickup', 'Delivery', 'Rate', 'Notes', 'Total Pay']
    load_data = [load_headers]

    for load in driver_pay_data['loads']:
        row = [
            load['Load #'],
            load['Pickup'],
            load['Delivery'],
            load['Formula'],
            load['Notes'][:20] + '...' if len(load['Notes']) > 20 else load['Notes'],
            load['Result']
        ]
        load_data.append(row)

    # Add total row
    load_data.append(['', '', '', '', 'Total:', driver_pay_data['total_pay']['Result']])

    load_table = Table(load_data, colWidths=[0.8*inch, 1.8*inch, 1.8*inch, 1*inch, 1*inch, 0.8*inch])
    load_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
        ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    story.append(load_table)
    story.append(Spacer(1, 20))

    # Recurring Deductions
    deduction_data = [
        ['Recurring Deductions', ''],
        ['Escrow Deposit:', driver_pay_data['escrow_deduction']['Result']],
        ['Fuel:', '$0.00'],
        ['Insurance:', '$0.00'],
        ['ETA:', '$0.00'],
        ['Other:', '$0.00'],
        ['', ''],
        ['Total:', driver_pay_data['total_pay']['Result']]
    ]

    deduction_table = Table(deduction_data, colWidths=[4*inch, 1.5*inch])
    deduction_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    story.append(deduction_table)
    story.append(Spacer(1, 20))

    # Page number
    story.append(Paragraph("Page 1 of 1", ParagraphStyle('PageNumber', parent=styles['Normal'], alignment=TA_CENTER)))

    doc.build(story)
    buffer.seek(0)
    return buffer


def generate_company_driver_pdf(driver_pay_data, driver, loads_data, company_info=None):
    """
    Company Driver uchun CD fayl PDF hisobot yaratish
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    styles = getSampleStyleSheet()
    story = []

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        alignment=TA_CENTER,
        spaceAfter=20,
        textColor=colors.black
    )

    # Company header
    if company_info:
        company_header_data = [
            [company_info.get('company_name', 'Company Name'), 'Driver: Orol Berdiyev'],
            [f"Phone: {company_info.get('phone', 'N/A')}", f"Report Date: {driver_pay_data['driver']['report_date']}"],
            [f"Fax: {company_info.get('fax', 'N/A')}", f"Search From: {driver_pay_data['driver']['search_from']}"],
            ['', f"Search To: {driver_pay_data['driver']['search_to']}"],
            ['', f"Status: {driver_pay_data['driver']['contact_number']}"]
        ]
    else:
        company_header_data = [
            ['Shuntransport Express Inc.', 'Driver: Orol Berdiyev'],
            ['Phone: (815) 636-3917', f"Report Date: {driver_pay_data['driver']['report_date']}"],
            ['Fax: (815) 636-3560', f"Search From: {driver_pay_data['driver']['search_from']}"],
            ['', f"Search To: {driver_pay_data['driver']['search_to']}"],
            ['', f"Status: {driver_pay_data['driver']['contact_number']}"]
        ]

    company_table = Table(company_header_data, colWidths=[3*inch, 3*inch])
    company_table.setStyle(TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(company_table)
    story.append(Spacer(1, 20))

    # Driver name
    driver_name = f"{driver_pay_data['driver']['first_name']} {driver_pay_data['driver']['last_name']}"
    story.append(Paragraph(f"In total, {driver_name} drove in the week from {driver_pay_data['driver']['search_from']} to {driver_pay_data['driver']['search_to']}:", styles['Normal']))
    story.append(Spacer(1, 10))

    # Calculate total miles and total pay
    total_miles = sum([load.get('loaded_miles', 0) for load in loads_data])
    total_pay = total_miles * 0.65

    # Summary table
    summary_data = [
        ['Miles', 'Rate', 'To pay'],
        [str(total_miles), '$0.65', f'${total_pay:.2f}']
    ]

    summary_table = Table(summary_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ]))

    story.append(summary_table)
    story.append(Spacer(1, 20))

    # Loads detail table
    load_headers = ['Load #', 'Trip', 'Loaded Miles', 'Load ID']
    load_data = [load_headers]

    for load in loads_data:
        trip_info = f"{load.get('pickup_location', 'N/A')} - {load.get('delivery_location', 'N/A')}"
        row = [
            load.get('load_number', 'N/A'),
            trip_info[:50] + '...' if len(trip_info) > 50 else trip_info,
            str(load.get('loaded_miles', 0)),
            load.get('load_id', 'N/A')
        ]
        load_data.append(row)

    load_table = Table(load_data, colWidths=[1*inch, 3*inch, 1*inch, 1.5*inch])
    load_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    story.append(load_table)
    story.append(Spacer(1, 20))

    # Summary at bottom
    final_summary_data = [
        ['Total Load Pages:', f'${total_pay:.2f}'],
        ['Net Other Pays:', '$0.00'],
        ['Net Driver Pays:', '$0.00'],
        ['', ''],
        ['Grand Total:', f'${total_pay:.2f}']
    ]

    final_summary_table = Table(final_summary_data, colWidths=[4*inch, 1.5*inch])
    final_summary_table.setStyle(TableStyle([
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    story.append(final_summary_table)
    story.append(Spacer(1, 20))

    # Page number
    story.append(Paragraph("Page 2 of 2", ParagraphStyle('PageNumber', parent=styles['Normal'], alignment=TA_CENTER)))

    doc.build(story)
    buffer.seek(0)
    return buffer
