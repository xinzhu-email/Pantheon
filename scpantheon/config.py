import os
import sys
from PyQt5.QtGui import QSurfaceFormat, QOpenGLContext

def set_software_rendering():
    if sys.platform.startswith('linux'):
        os.environ['LIBGL_ALWAYS_SOFTWARE'] = '1'
        print("Software rendering is enabled (LIBGL_ALWAYS_SOFTWARE=1)")

def configure_opengl():
    # 获取系统支持的 OpenGL 版本
    fmt = QSurfaceFormat()
    context = QOpenGLContext()
    context.create()
    version = context.format().version()  # 返回 (major, minor)

    # 根据支持版本动态调整
    if version >= (4, 1):
        fmt.setVersion(4, 1)
        fmt.setProfile(QSurfaceFormat.OpenGLContextProfile.CoreProfile)
    elif version >= (3, 3):
        fmt.setVersion(3, 3)
        fmt.setProfile(QSurfaceFormat.OpenGLContextProfile.CompatibilityProfile)
    else:
        fmt.setVersion(2, 1)
        fmt.setProfile(QSurfaceFormat.OpenGLContextProfile.CompatibilityProfile)

    fmt.setDepthBufferSize(24)
    fmt.setSamples(4)
    QSurfaceFormat.setDefaultFormat(fmt)
    print("Final format:", QSurfaceFormat.defaultFormat().version())