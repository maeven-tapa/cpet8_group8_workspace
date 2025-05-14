import os
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import matplotlib.pyplot as plt
import tempfile
import pandas as pd
import io

class ReportGeneration:
    def __init__(self, db):
        self.db = db
        self.styles = getSampleStyleSheet()
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=1
        )
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            textColor=colors.HexColor('#2c3e50')
        )

    def generate_report(self, output_path):
        doc = SimpleDocTemplate(
            output_path,
            pagesize=landscape(letter),
            rightMargin=50,
            leftMargin=50,
            topMargin=50,
            bottomMargin=50
        )
        
        story = []
        
        # Title
        title = Paragraph(f"Employee Performance Report - {datetime.now().strftime('%B %Y')}", self.title_style)
        story.append(title)
        
        # Employee Table
        story.append(Paragraph("Employee Overview", self.heading_style))
        employee_table = self.create_employee_table()
        story.append(employee_table)
        story.append(Spacer(1, 20))
        
        # Statistics Section
        story.append(Paragraph("Statistics & Analytics", self.heading_style))
        
        # Department Distribution Chart
        dept_chart = self.create_department_chart()
        story.append(Image(dept_chart, width=400, height=200))
        story.append(Spacer(1, 20))
        
        # Work Hours Chart
        hours_chart = self.create_work_hours_chart()
        story.append(Image(hours_chart, width=400, height=200))
        story.append(Spacer(1, 20))
        
        # Performance Tables
        story.append(Paragraph("Top Performers", self.heading_style))
        top_performers = self.create_top_performers_table()
        story.append(top_performers)
        story.append(Spacer(1, 20))
        
        story.append(Paragraph("Areas for Improvement", self.heading_style))
        improvement_needed = self.create_improvement_table()
        story.append(improvement_needed)
        
        # Build the PDF
        doc.build(story)
        
        # Cleanup temporary files
        if os.path.exists(dept_chart):
            os.remove(dept_chart)
        if os.path.exists(hours_chart):
            os.remove(hours_chart)

    def create_employee_table(self):
        cursor = self.db.execute_query("""
            SELECT 
                e.employee_id,
                e.first_name || ' ' || e.last_name as name,
                e.department,
                e.position,
                e.status,
                COUNT(DISTINCT a.date) as attendance_days,
                SUM(CASE WHEN a.is_late = 1 THEN 1 ELSE 0 END) as late_count
            FROM Employee e
            LEFT JOIN attendance_logs a ON e.employee_id = a.employee_id
            WHERE e.is_hr = 0
            GROUP BY e.employee_id
        """)
        
        data = [["ID", "Name", "Department", "Position", "Status", "Days Present", "Late Count"]]
        data.extend([list(row) for row in cursor.fetchall()])
        
        table = Table(data, repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BOX', (0, 0), (-1, -1), 2, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.Color(0.9, 0.9, 0.9)]),
        ]))
        
        return table

    def create_department_chart(self):
        cursor = self.db.execute_query("""
            SELECT department, COUNT(*) as count
            FROM Employee
            WHERE is_hr = 0
            GROUP BY department
        """)
        
        departments, counts = zip(*cursor.fetchall())
        
        plt.figure(figsize=(10, 5))
        plt.pie(counts, labels=departments, autopct='%1.1f%%')
        plt.title('Employee Distribution by Department')
        
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
        plt.savefig(temp_file.name)
        plt.close()
        
        return temp_file.name

    def create_work_hours_chart(self):
        cursor = self.db.execute_query("""
            SELECT DATE(created_at) as date, average_work_hours
            FROM system_logs
            WHERE strftime('%Y-%m', created_at) = strftime('%Y-%m', 'now')
            ORDER BY date
        """)
        
        dates, hours = zip(*cursor.fetchall())
        
        plt.figure(figsize=(10, 5))
        plt.plot(dates, hours, marker='o')
        plt.title('Average Work Hours Trend')
        plt.xticks(rotation=45)
        plt.ylabel('Hours')
        plt.grid(True)
        
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
        plt.savefig(temp_file.name, bbox_inches='tight')
        plt.close()
        
        return temp_file.name

    def create_top_performers_table(self):
        cursor = self.db.execute_query("""
            SELECT 
                e.first_name || ' ' || e.last_name as name,
                e.department,
                COUNT(DISTINCT a.date) as attendance_days,
                SUM(CASE WHEN a.is_late = 0 THEN 1 ELSE 0 END) as on_time_days
            FROM Employee e
            LEFT JOIN attendance_logs a ON e.employee_id = a.employee_id
            WHERE e.is_hr = 0
            GROUP BY e.employee_id
            ORDER BY attendance_days DESC, on_time_days DESC
            LIMIT 10
        """)
        
        data = [["Name", "Department", "Days Present", "On-Time Days"]]
        data.extend([list(row) for row in cursor.fetchall()])
        
        table = Table(data, repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#27ae60')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        
        return table

    def create_improvement_table(self):
        cursor = self.db.execute_query("""
            SELECT 
                e.first_name || ' ' || e.last_name as name,
                e.department,
                COUNT(DISTINCT a.date) as attendance_days,
                SUM(CASE WHEN a.is_late = 1 THEN 1 ELSE 0 END) as late_days
            FROM Employee e
            LEFT JOIN attendance_logs a ON e.employee_id = a.employee_id
            WHERE e.is_hr = 0
            GROUP BY e.employee_id
            HAVING late_days > 0
            ORDER BY late_days DESC
            LIMIT 10
        """)
        
        data = [["Name", "Department", "Days Present", "Late Days"]]
        data.extend([list(row) for row in cursor.fetchall()])
        
        table = Table(data, repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e74c3c')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        
        return table
