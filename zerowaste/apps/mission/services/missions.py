from apps.core.utils import s3


def separate_url_to_signed_public(signed_url_num, user):
    signed_url_list = []
    public_url_list = []
    if signed_url_num:
        url_list = s3.generate_upload_signed_url(signed_url_num, user.id)
        for url in url_list:
            signed_url_list.append(url['signed_url'])
            public_url_list.append(url['public_url'])
    return signed_url_list, public_url_list