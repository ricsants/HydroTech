from rest_framework import permissions


class IsOwnerOrSelf(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return getattr(request.user, 'is_authenticated', False) and obj.id == request.user.id


class IsDefesaCivilOrAdmin(permissions.BasePermission):
    """
    Permite acesso apenas para usuários Defesa Civil ou Admin (staff)
    """
    def has_permission(self, request, view):
        if not getattr(request.user, 'is_authenticated', False):
            return False
        return getattr(request.user, 'is_staff', False) or getattr(request.user, 'is_defesa_civil', False)


class IsDefesaCivilAdminOrOwner(permissions.BasePermission):
    """
    Permite visualizar PontoRisco por qualquer um autenticado,
    mas criar/editar/deletar apenas para Defesa Civil + Admin e o criador
    """
    def has_permission(self, request, view):
        if not getattr(request.user, 'is_authenticated', False):
            return False
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return getattr(request.user, 'is_staff', False) or getattr(request.user, 'is_defesa_civil', False)
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return obj.criado_por.id == request.user.id or getattr(request.user, 'is_staff', False)
        return True


class IsAdminOnly(permissions.BasePermission):
    """
    Permite apenas usuários Admin/Staff.
    (Usa getattr pra não depender de campos que podem não existir no modelo Usuario.)
    """
    def has_permission(self, request, view):
        return bool(
            getattr(request.user, 'is_authenticated', False)
            and getattr(request.user, 'is_staff', False)
        )
