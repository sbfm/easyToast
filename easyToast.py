# coding: utf-8
#
# Licence : MIT Licence 
# owner   : Fumiya Shibamata
# web     : https://github.com/sbfm/easyToast
#
# 
# official Documents
# https://docs.microsoft.com/en-us/windows/win32/winmsg/window-classes
# https://docs.microsoft.com/en-us/windows/win32/api/shellapi/ns-shellapi-notifyicondataw
# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-loadimagew
#
#
import os
import ctypes
from ctypes import Structure, windll, sizeof, POINTER, WINFUNCTYPE
from ctypes.wintypes import ( 
    DWORD, HICON, HWND, UINT, WCHAR, WORD, 
    BYTE, LPCWSTR, INT, HINSTANCE, BOOL, HANDLE
    ) 


def toast (title, message, tips = "tips", icon="") :
    """
    toast 
    
    icon : set .ico file
    """
    class GUID(Structure):
        _fields_ = [
            ("Data1", DWORD),
            ("Data2", WORD),
            ("Data3", WORD),
            ("Data4", BYTE * 8)
        ]
    
    class NOTIFYICONDATAW(Structure):
        _fields_ = [
            ("cbSize", DWORD),
            ("hWnd", HWND),
            ("uID", UINT),
            ("uFlags", UINT),
            ("uCallbackMessage", UINT),
            ("hIcon", HICON),
            ("szTip", WCHAR * 128),
            ("dwState", DWORD),
            ("dwStateMask", DWORD),
            ("szInfo", WCHAR * 256),
            ("uVersion", UINT),
            ("szInfoTitle", WCHAR * 64),
            ("dwInfoFlags", DWORD),
            ("guidItem", GUID),
            ("hBalloonIcon", HICON),
        ]
    
    # Load WindowsAPI
    LoadImageW = windll.User32.LoadImageW
    LoadImageW.argtypes = [HINSTANCE, LPCWSTR, UINT, INT, INT, UINT]
    LoadImageW.restype = HANDLE
    
    Shell_NotifyIconW = windll.Shell32.Shell_NotifyIconW
    Shell_NotifyIconW.argtypes = [DWORD, POINTER(NOTIFYICONDATAW)]
    Shell_NotifyIconW.restype = BOOL
    
    # set icon
    if icon:
        hicon = LoadImageW( None, icon, 1, 0, 0, 0x00000050)
        flags = 0x00000016 # NIF_ICON,NIF_TIP,NIF_INFO
        infoflag = 0x00000034 # NIIF_USER,NIIF_NOSOUND,NIIF_LARGE_ICON
        if hicon is None:
            raise Exception('load icon error.')
    else:
        hicon = None
        flags = 0x00000014 # NIF_TIP,NIF_INFO
        infoflag = 0x00000000 # NO PARAMETER
    
    
    mem_size = sizeof(NOTIFYICONDATAW)
    notify_data = NOTIFYICONDATAW(
            mem_size, 0, os.getpid(), flags, 0, hicon, tips, 
            0, 0, message, 4, title, infoflag, GUID(), hicon
    )
    
    Shell_NotifyIconW(0x00000000, notify_data)
    Shell_NotifyIconW(0x00000002, notify_data)
    

#toast(title="hogehoge",message="hogehoge")
