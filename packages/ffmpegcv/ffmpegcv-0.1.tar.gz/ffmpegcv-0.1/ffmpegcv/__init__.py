from .ffmpeg_reader import FFmpegReader
from .ffmpeg_writer import FFmpegWriter

def VideoCapture(file, 
                 codec=None, 
                 pix_fmt='bgr24',
                 resize=None,
                 resize_keepratio=True):
    """
    Alternative to cv2.VideoCapture

    Parameters
    ----------
    file : str
        Path to video file.
    codec : str
        Codec to use. Optional. Default is `None`.
    pix_fmt : str
        Pixel format. ['bgr24' | 'rgb24']. Optional. Default is 'bgr24'.
    resize  : tuple
        Resize the video to the given size. Optional. Default is `None`.
    resize_keepratio : bool
        Keep the aspect ratio and the border is black. Optional. Default is `True`.

    Examples
    --------
    opencv
    ```
    cap = cv2.VideoCapture(file)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        pass
    ```

    ffmpegcv
    ```
    cap = ffmpegcv.VideoCapture(file)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        pass
    ```

    Or use iterator
    ```
    cap = ffmpegcv.VideoCapture(file)
    for frame in cap:
        pass
    counts = len(cap)
    ```

    Use GPU to accelerate decoding
    ```
    cap_cpu = ffmpegcv.VideoCapture(file, codec='h264')
    cap_gpu = ffmpegcv.VideoCapture(file, codec='h264_cuvid')
    ```

    Use rgb24 instead of bgr24
    ```
    cap = ffmpegcv.VideoCapture(file, pix_fmt='rgb24')
    ```

    Resize the video to the given size
    ```
    cap = ffmpegcv.VideoCapture(file, resize=(640, 480))
    ```

    Resize and keep the aspect ratio with black border
    ```
    cap = ffmpegcv.VideoCapture(file, resize=(640, 480), resize_keepratio=True)
    ```

    Author: Chenxinfeng 2022-04-16, cxf529125853@163.com
    """
    print(file, codec, pix_fmt, resize, resize_keepratio)
    return FFmpegReader.VideoReader(file, codec, pix_fmt, resize, resize_keepratio)


def VideoReader(*args, **kwargs):
    """
     `ffmpegcv.VideoReader` is an alias to `ffmpegcv.VideoCapture`
    """
    return VideoCapture(*args, **kwargs)                                                                       


def VideoWriter(file, 
                codec=None, 
                fps=30, 
                frameSize=None, 
                pix_fmt='bgr24'):
    """
    Alternative to cv2.VideoWriter

    Parameters
    ----------
    file : str
        Path to video file.
    codec : str
        Codec to use. Optional. Default is `None` (x264).
    fps : number
        Frames per second. Optional. Default is 30.
    frameSize : tuple
        Frame size. (width, height). Requisite. 
    pix_fmt : str
        Pixel format. ['bgr24' | 'rgb24']. Optional. Default is 'bgr24'.

    Examples
    --------
    opencv
    ```
    out = cv2.VideoWriter('outpy.avi',
                          cv2.VideoWriter_fourcc('M','J','P','G'), 
                          10, 
                          (w, h))
    out.write(frame1)
    out.write(frame2)
    out.release()
    ```

    ffmpegcv
    ```
    out = ffmpegcv.VideoWriter('outpy.avi', None, 10, (w, h))
    out.write(frame1)
    out.write(frame2)
    out.release()
    ```

    Use GPU to accelerate encoding
    ```
    out_cpu = ffmpegcv.VideoWriter('outpy.avi', None, 10, (w, h))
    out_gpu = ffmpegcv.VideoWriter('outpy.avi', 'h264_nvenc', 10, (w, h))
    ```

    Use rgb24 instead of bgr24
    ```
    out = ffmpegcv.VideoWriter('outpy.avi', None, 10, (w, h), pix_fmt='rgb24')
    out.write(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    ```

    Author: Chenxinfeng 2022-04-16, cxf529125853@163.com
    """
    return FFmpegWriter.VideoWriter(file, codec, fps, frameSize, pix_fmt)

