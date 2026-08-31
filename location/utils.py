from __future__ import annotations

from decimal import Decimal
from io import BytesIO


def generate_quittance_pdf(bail, output=None):
    """Génère un PDF de quittance de loyer pour un bail.

    La fonction est volontairement légère et compatible avec le projet :
    elle n'a pas besoin d'une implémentation complète pour que le système
    charge correctement. Le vrai PDF est généré uniquement si reportlab est
    disponible dans l'environnement d'exécution.
    """
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
    except ModuleNotFoundError as exc:  # pragma: no cover - dépendance optionnelle
        raise ModuleNotFoundError(
            "Le package 'reportlab' est requis pour générer une quittance PDF."
        ) from exc

    buffer = BytesIO() if output is None else output
    pdf = canvas.Canvas(buffer, pagesize=A4)
    pdf.setTitle("Quittance de loyer")
    pdf.drawString(80, 780, "Quittance de loyer")

    if bail is not None:
        locataire = getattr(bail, "locataire", None)
        montant = getattr(bail, "loyer_mensuel", Decimal("0.00"))
        pdf.drawString(80, 760, f"Locataire: {locataire or 'Non renseigné'}")
        pdf.drawString(80, 745, f"Montant: {montant} FCFA")

    pdf.showPage()
    pdf.save()
    if output is None:
        return buffer.getvalue()
    return output