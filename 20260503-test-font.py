import sys
import win32gui
import win32con
import win32api

def draw_text_with_font(hdc, font, text, x_pos, y_pos):
    logfont = win32gui.LOGFONT()
    logfont.lfFaceName = font
    logfont.lfHeight = 20
    logfont.lfQuality = win32con.CLEARTYPE_QUALITY
    hf = win32gui.CreateFontIndirect(logfont)
    win32gui.SelectObject(hdc, hf)
    win32gui.DrawText(
        hdc, text, -1, (x_pos, y_pos, x_pos + 200, y_pos + 20),
        win32con.DT_LEFT | win32con.DT_TOP | win32con.DT_SINGLELINE
    )

def wnd_proc(hwnd, message, wparam, lparam):
    if message == win32con.WM_CREATE:
        hdc = win32gui.GetDC(hwnd)
        win32gui.ReleaseDC(hwnd, hdc)
        return 0
    elif message == win32con.WM_PAINT:
        hdc, paintStruct = win32gui.BeginPaint(hwnd)
        win32gui.SetTextColor(hdc, win32api.RGB(0, 0, 0))
        win32gui.SetBkMode(hdc, win32con.TRANSPARENT)
        draw_text_with_font(hdc, "SimSun", "文字", 10, 10)
        draw_text_with_font(hdc, "@SimSun", "文字", 10, 30)
        draw_text_with_font(hdc, "SimSun-ExtB", "𠀀𠀁𪜀𪜁𫝀𫝁𫠠𫠡𬺰𬺱", 10, 50)
        draw_text_with_font(hdc, "@SimSun-ExtB", "𠀀𠀁𪜀𪜁𫝀𫝁𫠠𫠡𬺰𬺱", 10, 70)
        draw_text_with_font(hdc, "SimSun-ExtG", "𰀀𰀁", 10, 90)
        draw_text_with_font(hdc, "@SimSun-ExtG", "𰀀𰀁", 10, 110)
        win32gui.EndPaint(hwnd, paintStruct)
        return 0
    elif message == win32con.WM_DESTROY:
        win32gui.PostQuitMessage(0)
        return 0

    return win32gui.DefWindowProc(hwnd, message, wparam, lparam)

def main():
    instance = win32api.GetModuleHandle(None)
    app_name = "FontDemo"

    wnd = win32gui.WNDCLASS()
    wnd.style = win32con.CS_HREDRAW | win32con.CS_VREDRAW
    wnd.hInstance = instance
    wnd.lpszClassName = app_name
    wnd.lpfnWndProc = wnd_proc
    wnd.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
    wnd.hIcon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)
    wnd.hbrBackground = win32con.COLOR_WINDOW + 1
    wnd_id = win32gui.RegisterClass(wnd)

    if not wnd_id:
        win32gui.MessageBox(
            None, "This program requirs Windows NT!",
            app_name, win32con.MB_ICONERROR
        )
        return 0

    window = win32gui.CreateWindow(
        wnd_id, app_name,
        win32con.WS_OVERLAPPEDWINDOW,
        win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT,
        400, 200, 0, 0, instance, None
    )

    win32gui.ShowWindow(window, win32con.SW_SHOWNORMAL)
    win32gui.UpdateWindow(window)

    while True:
        hwnd, msg = win32gui.GetMessage(None, 0, 0)
        if hwnd <= 0:
            break
        else:
            win32gui.TranslateMessage(msg)
            win32gui.DispatchMessage(msg)

    sys.exit(msg[1])

if __name__ == "__main__":
    main()
