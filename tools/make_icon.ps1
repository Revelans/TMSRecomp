# make_icon.ps1 <image> [out.ico]: any image (e.g. the game's own icon from your NSP's control NCA,
# icon_AmericanEnglish.dat, a 256x256 JPEG) -> a 256x256 PNG-in-ICO; default out private\tms\icon.ico.
# build.cmd embeds private\tms\icon.ico in tms.exe when it exists (re-run cmake: delete private\tms\build\build.ninja).
param([Parameter(Mandatory = $true)][string]$image, [string]$out = "$PSScriptRoot\..\private\tms\icon.ico")
Add-Type -AssemblyName System.Drawing
$src = [System.Drawing.Image]::FromFile((Resolve-Path $image))
$bmp = New-Object System.Drawing.Bitmap 256, 256
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
$g.DrawImage($src, 0, 0, 256, 256)
$ms = New-Object System.IO.MemoryStream
$bmp.Save($ms, [System.Drawing.Imaging.ImageFormat]::Png)
$png = $ms.ToArray()
$f = New-Object System.IO.BinaryWriter([System.IO.File]::Create([System.IO.Path]::GetFullPath($out)))
$f.Write([uint16]0); $f.Write([uint16]1); $f.Write([uint16]1)                # ICONDIR: reserved, type icon, 1 image
$f.Write([byte]0); $f.Write([byte]0); $f.Write([byte]0); $f.Write([byte]0)  # 256x256 (0 = 256), no palette
$f.Write([uint16]1); $f.Write([uint16]32); $f.Write([uint32]$png.Length); $f.Write([uint32]22)
$f.Write($png)
$f.Close(); $g.Dispose(); $bmp.Dispose(); $src.Dispose()
"wrote $out ($($png.Length + 22) bytes)"
