"""
pdf_generator.py
Generates professional PDF reports for SecureSphere AI simulations.
Takes computed simulation data and formats it into a board-ready document.
"""

from typing import Dict, Any
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


class PDFGenerator:
    """
    Handles the creation of PDF reports summarizing the cyber risk simulation.
    Uses ReportLab to build a styled, structured document.
    """

    def __init__(self):
        """
        Initializes the PDFGenerator and loads standard stylesheets.
        """
        self.styles = getSampleStyleSheet()
        # Add custom styles for the report
        self.styles.add(ParagraphStyle(
            name='ReportSubtitle',
            parent=self.styles['Heading2'],
            textColor=colors.HexColor("#06B6D4"),
            spaceAfter=12
        ))
        self.styles.add(ParagraphStyle(
            name='TimelineDay',
            parent=self.styles['Heading3'],
            textColor=colors.HexColor("#1E293B"),
            spaceBottom=4
        ))
        self.styles.add(ParagraphStyle(
            name='FooterText',
            parent=self.styles['Normal'],
            textColor=colors.gray,
            fontSize=8,
            alignment=1  # Center alignment
        ))

    def generate_report(self, output_path: str, simulation_data: Dict[str, Any]) -> None:
        """
        Generates a PDF report and saves it to the specified output path.

        Args:
            output_path (str): The file path where the PDF will be saved.
            simulation_data (Dict[str, Any]): The data dictionary containing
                                              metrics, configuration, and timeline.
        """
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=50,
            leftMargin=50,
            topMargin=50,
            bottomMargin=50
        )

        story = []

        # ==========================================
        # TITLE & HEADER
        # ==========================================
        story.append(Paragraph("SecureSphere AI", self.styles['Title']))
        story.append(Paragraph("Enterprise Cyber Risk Simulation Report", self.styles['ReportSubtitle']))
        story.append(Spacer(1, 20))

        # ==========================================
        # SIMULATION SUMMARY
        # ==========================================
        story.append(Paragraph("Simulation Profile", self.styles['Heading2']))

        # Formatting financial numbers safely
        rev = simulation_data.get('annual_revenue', 0)
        formatted_rev = f"${rev:,.2f}" if isinstance(rev, (int, float)) else str(rev)

        summary_data = [
            ["Company Name:", str(simulation_data.get("company_name", "N/A"))],
            ["Industry:", str(simulation_data.get("industry", "N/A"))],
            ["Annual Revenue:", formatted_rev],
            ["Employee Count:", str(simulation_data.get("employee_count", "N/A"))],
            ["Critical Asset:", str(simulation_data.get("critical_asset", "N/A"))],
            ["Targeted Attack:", str(simulation_data.get("attack_type", "N/A"))],
            ["Prepared For:", str(simulation_data.get("business_persona", "N/A"))]
        ]

        summary_table = Table(summary_data, colWidths=[150, 300])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor("#F8FAFC")),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor("#1E293B")),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 20))

        # ==========================================
        # RISK SUMMARY & FINANCIAL IMPACT
        # ==========================================
        story.append(Paragraph("Risk & Financial Impact", self.styles['Heading2']))

        risk_score = simulation_data.get("risk_score", 0)
        stars = simulation_data.get("readiness_stars", "")

        # Format financial loss safely
        loss_range = simulation_data.get("financial_loss_range", (0, 0))
        if isinstance(loss_range, (list, tuple)) and len(loss_range) == 2:
            min_loss, max_loss = loss_range
            loss_str = f"${min_loss:,.2f} - ${max_loss:,.2f}"
        else:
            loss_str = str(loss_range)

        impact_data = [
            ["Cyber Readiness:", str(stars)],
            ["Risk Score (0-100):", f"{risk_score} (Lower is better)"],
            ["Estimated Financial Loss:", loss_str]
        ]

        impact_table = Table(impact_data, colWidths=[150, 300])
        impact_table.setStyle(TableStyle([
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor("#1E293B")),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ]))
        story.append(impact_table)
        story.append(Spacer(1, 20))

        # ==========================================
        # ATTACK STORY TIMELINE
        # ==========================================
        story.append(Paragraph("Attack Story Timeline", self.styles['Heading2']))

        timeline_events = simulation_data.get("timeline", [])
        if not timeline_events:
            story.append(Paragraph("No timeline data available for this simulation.", self.styles['Normal']))
        else:
            for event in timeline_events:
                day = event.get("day", "Day X")
                title = event.get("title", "Event")
                description = event.get("description", "")

                story.append(Paragraph(f"{day}: {title}", self.styles['TimelineDay']))
                story.append(Paragraph(description, self.styles['Normal']))
                story.append(Spacer(1, 10))

        # ==========================================
        # FOOTER
        # ==========================================
        story.append(Spacer(1, 30))
        story.append(Paragraph("Generated by SecureSphere AI", self.styles['FooterText']))

        # Build and save the PDF
        doc.build(story)