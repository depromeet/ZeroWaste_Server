from apps.user.models.bazzi import Bazzi


def initialize_bazzi():
    Bazzi(name="", icon_url="", description="첫 로그인 축하 뱃지").save()
    Bazzi(name="", icon_url="", description="첫 미션 좋아요 뱃지").save()
    Bazzi(name="", icon_url="", description="첫 미션 수락 뱃지").save()
    Bazzi(name="", icon_url="", description="첫 미션 인증완료 뱃지").save()
    Bazzi(name="", icon_url="", description="첫 미션 제안 뱃지").save()
    Bazzi(name="", icon_url="", description="첫 미션 자랑 뱃지").save() # client에서 주라고 요청해야함
    Bazzi(name="", icon_url="", description="첫 인증 좋아요 뱃지").save()
    Bazzi(name="", icon_url="", description="미션 2회 이상 수행").save()
    Bazzi(name="", icon_url="", description="미션 재도전 신청").save()

    # 공감 순위 뱃지는 랭킹 api 제작되면 구현방식 정하기
    Bazzi(name="", icon_url="", description="공감 순위 5위 진출").save()
    Bazzi(name="", icon_url="", description="공감 순위 3위 진출").save()
    Bazzi(name="", icon_url="", description="공감 순위 1위 진출").save()

    # 누적 이벤트
    Bazzi(name="", icon_url="", description="미션 수행 누적 이벤트").save()