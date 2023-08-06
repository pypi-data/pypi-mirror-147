from django.contrib.auth.models import Group, Permission, _user_get_permissions, _user_has_perm, _user_has_module_perms
from django.db.models.manager import EmptyManager


class ShareTokenUser:
    id = None
    pk = None
    username = ''
    is_staff = False
    is_active = False
    is_superuser = False
    _groups = EmptyManager(Group)
    _user_permissions = EmptyManager(Permission)

    def __init__(self, model_name, model_pk, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model_name = model_name
        self.model_pk = model_pk

    def __str__(self):
        return 'ShareTokenUser'

    def __eq__(self, other):
        return isinstance(other, self.__class__)

    def __hash__(self):
        return 1

    def __int__(self):
        raise TypeError('Cannot cast ShareTokenUser to int. Are you trying to use it in place of User?')

    def save(self):
        raise NotImplementedError("A ShareTokenUser doesn't have DB representation")

    def delete(self):
        raise NotImplementedError("A ShareTokenUser doesn't have DB representation")

    def set_password(self, raw_password):
        raise NotImplementedError("A ShareTokenUser has no password")

    def check_password(self, raw_password):
        raise NotImplementedError("A ShareTokenUser has no password")

    @property
    def groups(self):
        return self._groups

    @property
    def user_permissions(self):
        return self._user_permissions

    def get_user_permissions(self, obj=None):
        return set()

    def get_group_permissions(self, obj=None):
        return set()

    def get_all_permissions(self, obj=None):
        return set()

    def has_perm(self, perm, obj=None):
        return False

    def has_perms(self, perm_list, obj=None):
        return all(self.has_perm(perm, obj) for perm in perm_list)

    def has_module_perms(self, module):
        return False

    @property
    def is_anonymous(self):
        return True

    @property
    def is_authenticated(self):
        return True

    def get_username(self):
        return self.username