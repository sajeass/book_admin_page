import platform

def remove_duplicate(some_list):
    result = []
    for row in some_list:
        if row not in result:
            result.append(row)
    return result

def is_ubuntu():
    # platform.linux_distribution() 함수는 Python 3.8 이상에서는 사용할 수 없습니다.
    # 대신 distro 모듈을 사용할 수 있습니다. (distro 모듈을 사용하기 위해서는 먼저 설치해야 할 수 있습니다.)
    try:
        # Python 3.7 이하 버전에서 사용 가능
        distribution = platform.linux_distribution()
        return distribution[0].lower() == "ubuntu"
    except AttributeError:
        # Python 3.8 이상에서는 distro 모듈을 사용
        try:
            import distro
            return distro.id().lower() == "ubuntu"
        except ImportError:
            print("distro 모듈이 설치되어 있지 않습니다. 'pip install distro'를 실행하세요.")
            return False