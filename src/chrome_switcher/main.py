"""Docstring"""
import get_user_info
import make_persistent
import make_temporary


profile_path = get_user_info.main()
if profile_path is None:
