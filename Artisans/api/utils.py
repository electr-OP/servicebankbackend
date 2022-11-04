import random as r


def otpgen():
    """
        Function for otp generation
    """
    otp=""
    for i in range(4):
        otp+=str(r.randint(1,9))
    return otp

def unique_otp_generator(instance):
    otp= otpgen()

    Merchant= instance.__class__

    qs_exists= Merchant.objects.filter(email_activation_token=otp).exists()
    if qs_exists:
        return unique_otp_generator(instance)
    return otp