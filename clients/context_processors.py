def role_user(request):
    est_technicien = False

    if request.user.is_authenticated:
        try:
            est_technicien = request.user.technicien is not None
        except:
            est_technicien = False

    return {
        'est_technicien': est_technicien
    }