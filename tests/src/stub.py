# Jormungandr - Onboarding
from func.src.domain.user.model import UserModel
from func.src.domain.validator import UserParams

stub_user_params = UserParams(**{
    'email': 'teste@teste.com',
    'nickname': 'vnnstar',
}).dict()

stub_user_model = UserModel(email=stub_user_params['email'], nickname=stub_user_params['nickname']).get_user_template()
