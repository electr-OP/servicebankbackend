import random as r


def otpgen():
    """
        Function for otp generation
    """
    otp=""
    for i in range(6):
        otp+=str(r.randint(1,9))
    return otp

def unique_otp_generator(instance):
    otp= otpgen()

    User= instance.__class__

    qs_exists= User.objects.filter(activation_code=otp).exists()
    if qs_exists:
        return unique_otp_generator(instance)
    return otp


def generate_referral_id():
    return str(r.randint(100000, 999999))