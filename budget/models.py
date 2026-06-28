from django.db import models


class Projet(models.Model):
    nom = models.CharField(max_length=255)
    budget_avance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    taux_imprevu = models.DecimalField(max_digits=5, decimal_places=2, default=10)
    date_creation = models.DateTimeField(auto_now_add=True)

    def budget_estimatif(self):
        return sum(p.total_devis_revu() for p in self.postes.all())

    def imprevu(self):
        return float(self.budget_estimatif()) * (float(self.taux_imprevu) / 100)

    def total_avances(self):
        return sum(
        float(l.avance or 0)
        for p in self.postes.all()
        for l in p.lignes.all()
        )

    def en_caisse(self):
        return float(self.budget_avance or 0) - self.total_avances()

    def total_reliquat(self):
        return sum(
        l.reliquat()
        for p in self.postes.all()
        for l in p.lignes.all()
        )

    def reliquat_def(self):
        return self.en_caisse() - self.total_reliquat()

    def surplus(self):
        return float(self.budget_avance or 0) - float(self.budget_estimatif())

    def __str__(self):
        return self.nom


class Poste(models.Model):
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE, related_name='postes')
    nom = models.CharField(max_length=255)
    ordre = models.PositiveIntegerField(default=0)

    def total_devis_revu(self):
        return sum(l.devis_revu or 0 for l in self.lignes.all())

    def total_avance(self):
        return sum(l.avance or 0 for l in self.lignes.all())

    def total_reliquat(self):
        return sum(l.reliquat() for l in self.lignes.all())

    class Meta:
        ordering = ['ordre']

    def __str__(self):
        return f"{self.projet.nom} — {self.nom}"


class LigneDesignation(models.Model):
    poste = models.ForeignKey(Poste, on_delete=models.CASCADE, related_name='lignes')
    designation = models.CharField(max_length=255)
    devis = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    devis_revu = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    avance = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def reliquat(self):
        return (float(self.devis_revu) if self.devis_revu else 0) - (float(self.avance) if self.avance else 0)

    def __str__(self):
        return f"{self.poste.nom} — {self.designation}"