# clients/cups.py
# Ce fichier contient les fonctions de tri personnalisées

def modelSort(queryset, sort_by=None):
    """
    Fonction de tri personnalisée
    """
    if sort_by:
        return queryset.order_by(sort_by)
    return queryset

