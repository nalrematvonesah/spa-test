from io import BytesIO
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side
from app.models.part import Part
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(
    TTFont("DejaVu", "app/fonts/DejaVuSans.ttf")
)

def calculate_total(part: Part):
    if part.children:
        return sum(calculate_total(child) for child in part.children)
    return (part.price or 0) * (part.quantity or 1)

def build_tree(part: Part, level=0, index=""):
    rows = []

    current_index = index or "1"

    rows.append({
        "index": current_index,
        "name": "    " * level + part.name,
        "price": part.price or 0,
        "quantity": part.quantity or 1,
        "total": calculate_total(part)
    })

    for i, child in enumerate(part.children, 1):
        child_index = f"{current_index}.{i}"
        rows.extend(build_tree(child, level + 1, child_index))

    return rows

def generate_excel(part: Part) -> BytesIO:
    wb = Workbook()
    ws = wb.active
    ws.title = "Parts"

    headers = ["№", "Деталь", "Цена", "Кол-во", "Стоимость"]
    ws.append(headers)

    bold = Font(bold=True)
    border = Border(
        left=Side(style="thin"),
        right=Side(style="thin"),
        top=Side(style="thin"),
        bottom=Side(style="thin")
    )

    for col in range(1, 6):
        cell = ws.cell(row=1, column=col)
        cell.font = bold
        cell.alignment = Alignment(horizontal="center")
        cell.border = border

    rows = build_tree(part)

    for row in rows:
        ws.append([
            row["index"],
            row["name"],
            row["price"],
            row["quantity"],
            row["total"]
        ])

    ws.column_dimensions["B"].width = 30

    stream = BytesIO()
    wb.save(stream)
    stream.seek(0)
    return stream

def generate_pdf(part: Part) -> BytesIO:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)

    rows = build_tree(part)

    table_data = [["№", "Деталь", "Цена", "Кол-во", "Стоимость"]]

    for row in rows:
        table_data.append([
            row["index"],
            row["name"],
            row["price"],
            row["quantity"],
            row["total"]
        ])

    table = Table(table_data)

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("FONTNAME", (0, 0), (-1, -1), "DejaVu"),
    ]))

    doc.build([table])

    buffer.seek(0)
    return buffer