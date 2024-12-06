from .upload import upload

__all__ = ['upload']


def __getattr__(name):
    if name == "upload":
        return upload
    raise AttributeError(f"Module '{__name__}' has no attribute '{name}'")


def __dir__():
    return ['upload']  # 노출할 항목만 반환
