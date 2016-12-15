from django.core.exceptions import PermissionDenied


def check_account_owner(account_queryset, request):
    account = account_queryset[0]
    user = request.user
    if not user.is_superuser and account.user != user:
        raise PermissionDenied()
    return account