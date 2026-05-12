from pathlib import Path
from PIL import Image, ImageCms

_PROJECT = Path(__file__).parent
_ICC_DIR = _PROJECT / "icc"
_RENDERS = _PROJECT / "renders"


def export(create_fn, name, display_bg):
    """Render and export a piece in both print and display formats, padded to A2.

    create_fn: callable matching create_artwork(bg=...) signature
    name:       output filename stem, e.g. "harmonic-tension"
    display_bg: RGB tuple for the display version background
    """
    _export_print(create_fn, name)
    _export_display(create_fn, name, display_bg)


def _export_print(create_fn, name):
    print("Rendering print version...")
    artwork = create_fn(bg=(255, 255, 255))
    width, height = artwork.size

    a2_height, pad_top, resolution = _a2_layout(width, height)
    canvas = Image.new("RGB", (width, a2_height), (255, 255, 255))
    canvas.paste(artwork, (0, pad_top))

    print("Converting to CMYK...")
    try:
        srgb = ImageCms.getOpenProfile(str(_ICC_DIR / "sRGB.icc"))
        cmyk_profile_path = _ICC_DIR / "ISOcoated_v2_300_eci.icc"
        cmyk = ImageCms.getOpenProfile(str(cmyk_profile_path))
        transform = ImageCms.buildTransform(
            srgb, cmyk, "RGB", "CMYK",
            renderingIntent=ImageCms.Intent.RELATIVE_COLORIMETRIC,
            flags=ImageCms.Flags.BLACKPOINTCOMPENSATION,
        )
        canvas_cmyk = ImageCms.applyTransform(canvas, transform)
        icc_bytes = cmyk_profile_path.read_bytes()
    except Exception as e:
        print(f"Warning: ICC conversion failed ({e}), using basic CMYK fallback")
        canvas_cmyk = canvas.convert("CMYK")
        icc_bytes = None

    path = _RENDERS / "print" / f"{name}.pdf"
    path.parent.mkdir(parents=True, exist_ok=True)
    save_kwargs = {"resolution": resolution}
    if icc_bytes:
        save_kwargs["icc_profile"] = icc_bytes
    canvas_cmyk.save(path, "PDF", **save_kwargs)
    print(f"Saved to {path}")


def _export_display(create_fn, name, display_bg):
    print("Rendering display version...")
    artwork = create_fn(bg=display_bg)
    width, height = artwork.size

    a2_height, pad_top, resolution = _a2_layout(width, height)
    canvas = Image.new("RGB", (width, a2_height), display_bg)
    canvas.paste(artwork, (0, pad_top))

    path = _RENDERS / "display" / f"{name}.png"
    path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(path, "PNG", dpi=(round(resolution), round(resolution)))
    print(f"Saved to {path}")


def _a2_layout(width, height):
    """Return (a2_height, pad_top, resolution) for an A2 canvas at given width."""
    a2_height = round(width * 594 / 420)
    pad_top = (a2_height - height) // 2
    resolution = width / (420 / 25.4)
    return a2_height, pad_top, resolution
