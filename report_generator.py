from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet


def create_report(results):

    pdf_file = "Cyber_Detective_Report.pdf"

    doc = SimpleDocTemplate(pdf_file)

    styles = getSampleStyleSheet()

    content = []

    title = Paragraph(
        "AI CYBER DETECTIVE REPORT",
        styles["Title"]
    )

    content.append(title)

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            f"<b>Attack Type:</b> {results['attack']}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"<b>Risk Level:</b> {results['risk']}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"<b>Confidence Score:</b> {results['confidence']}%",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"<b>Security Grade:</b> {results['grade']}",
            styles["BodyText"]
        )
    )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            "<b>Evidence Found:</b>",
            styles["Heading2"]
        )
    )

    if results["evidence"]:

        for item in results["evidence"]:

            content.append(
                Paragraph(
                    f"• {item}",
                    styles["BodyText"]
                )
            )

    else:

        content.append(
            Paragraph(
                "No suspicious evidence found.",
                styles["BodyText"]
            )
        )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            "<b>AI Threat Explanation:</b>",
            styles["Heading2"]
        )
    )

    content.append(
        Paragraph(
            results["explanation"],
            styles["BodyText"]
        )
    )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            "Developed By: DENILSON PINTO B",
            styles["BodyText"]
        )
    )

    doc.build(content)

    return pdf_file