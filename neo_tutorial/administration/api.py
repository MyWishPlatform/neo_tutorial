from neo_tutorial.profile.models import TutorialCommonUser


def get_all_users():
    users = TutorialCommonUser.objects.all()
    return users
