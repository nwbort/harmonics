#!/usr/bin/env python3
"""
Harmonic Tension - A visual expression of equilibrium and balanced forces
"""

from pathlib import Path
from PIL import Image, ImageCms, ImageDraw, ImageFont
import math

# Canvas dimensions (massive resolution for print quality)
WIDTH = 7200
HEIGHT = 9600
SCALE = 3  # Scale factor for all elements

# Colour palette - constrained, intentional
DEEP_NAVY = (18, 32, 47)
WARM_CORAL = (204, 108, 92)
SOFT_CREAM = (248, 244, 236)
GOLDEN_OCHRE = (198, 156, 89)
MUTED_SAGE = (142, 159, 145)

def draw_circle_outline(draw, cx, cy, radius, color, width=3):
    """Draw a circle outline with anti-aliasing approximation"""
    for w in range(width):
        r = radius - w
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color)

def create_artwork():
    # Create canvas with cream background
    img = Image.new('RGB', (WIDTH, HEIGHT), SOFT_CREAM)
    draw = ImageDraw.Draw(img)
    
    # === GEOMETRIC COMPOSITION ===
    
    # Central focal area
    center_x = WIDTH // 2
    center_y = HEIGHT // 2 - 100 * SCALE
    
    # Large primary circle - navy, positioned slightly off-center for tension
    primary_cx = center_x - 150 * SCALE
    primary_cy = center_y - 80 * SCALE
    primary_r = 520 * SCALE
    draw_circle_outline(draw, primary_cx, primary_cy, primary_r, DEEP_NAVY, 6 * SCALE)
    
    # Secondary circle - coral, intersecting with primary
    secondary_cx = center_x + 280 * SCALE
    secondary_cy = center_y + 50 * SCALE
    secondary_r = 420 * SCALE
    draw_circle_outline(draw, secondary_cx, secondary_cy, secondary_r, WARM_CORAL, 5 * SCALE)
    
    # Tertiary circle - golden, smaller, creating triangulation
    tertiary_cx = center_x + 60 * SCALE
    tertiary_cy = center_y + 380 * SCALE
    tertiary_r = 280 * SCALE
    draw_circle_outline(draw, tertiary_cx, tertiary_cy, tertiary_r, GOLDEN_OCHRE, 4 * SCALE)
    
    # Small accent circles - creating rhythm and scale variation
    accent_positions = [
        (center_x - 420 * SCALE, center_y - 350 * SCALE, 85 * SCALE, MUTED_SAGE),
        (center_x + 480 * SCALE, center_y - 280 * SCALE, 65 * SCALE, DEEP_NAVY),
        (center_x - 280 * SCALE, center_y + 520 * SCALE, 55 * SCALE, WARM_CORAL),
    ]
    for ax, ay, ar, col in accent_positions:
        draw_circle_outline(draw, int(ax), int(ay), int(ar), col, 3 * SCALE)
    
    # === ANGULAR ELEMENTS - creating tension with curves ===
    
    # Diagonal line - thin, precise, crossing the composition
    line_width = 3 * SCALE
    for w in range(line_width):
        draw.line([(180 * SCALE, 650 * SCALE + w), (2100 * SCALE, 1850 * SCALE + w)], fill=DEEP_NAVY, width=1)
    
    # Shorter intersecting line
    for w in range(2 * SCALE):
        draw.line([(1600 * SCALE, 400 * SCALE + w), (800 * SCALE, 2400 * SCALE + w)], fill=GOLDEN_OCHRE, width=1)
    
    # === FILLED GEOMETRIC ACCENTS ===
    
    # Small filled circle - focal point weight
    accent_fill_x = center_x + 350 * SCALE
    accent_fill_y = center_y - 380 * SCALE
    r = 35 * SCALE
    draw.ellipse([accent_fill_x - r, accent_fill_y - r, 
                  accent_fill_x + r, accent_fill_y + r], fill=WARM_CORAL)
    
    # Smaller filled circles creating constellation
    small_fills = [
        (center_x - 480 * SCALE, center_y + 100 * SCALE, 18 * SCALE, DEEP_NAVY),
        (center_x + 500 * SCALE, center_y + 340 * SCALE, 14 * SCALE, GOLDEN_OCHRE),
        (center_x - 120 * SCALE, center_y - 480 * SCALE, 22 * SCALE, MUTED_SAGE),
        (center_x + 180 * SCALE, center_y + 580 * SCALE, 12 * SCALE, WARM_CORAL),
    ]
    for sx, sy, sr, sc in small_fills:
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=sc)
    
    # === ARC SEGMENTS - partial circles for sophistication ===
    
    # Large arc in upper region
    arc_cx = center_x - 400 * SCALE
    arc_cy = center_y - 600 * SCALE
    arc_r = 380 * SCALE
    draw.arc([arc_cx - arc_r, arc_cy - arc_r, arc_cx + arc_r, arc_cy + arc_r],
             start=30, end=120, fill=GOLDEN_OCHRE, width=4 * SCALE)
    
    # Lower arc
    arc2_cx = center_x + 300 * SCALE
    arc2_cy = center_y + 700 * SCALE
    arc2_r = 320 * SCALE
    draw.arc([arc2_cx - arc2_r, arc2_cy - arc2_r, arc2_cx + arc2_r, arc2_cy + arc2_r],
             start=200, end=300, fill=MUTED_SAGE, width=4 * SCALE)
    
    # === CONCENTRIC RIPPLES - visual rhythm ===
    
    ripple_cx = center_x + 100 * SCALE
    ripple_cy = center_y - 50 * SCALE
    for i, r in enumerate([650 * SCALE, 680 * SCALE, 710 * SCALE]):
        opacity_adjust = (3 - i) * SCALE
        draw_circle_outline(draw, int(ripple_cx), int(ripple_cy), int(r), MUTED_SAGE, opacity_adjust)
    
    # === FINE DETAIL MARKS - suggests measurement/precision ===
    
    # Small tick marks along an invisible arc
    tick_center_x = center_x
    tick_center_y = center_y + 200 * SCALE
    tick_radius = 580 * SCALE
    for angle in range(0, 360, 15):
        if angle % 45 == 0:  # Skip some for asymmetry
            continue
        rad = math.radians(angle)
        inner_r = tick_radius - 8 * SCALE
        outer_r = tick_radius + 8 * SCALE
        x1 = tick_center_x + inner_r * math.cos(rad)
        y1 = tick_center_y + inner_r * math.sin(rad)
        x2 = tick_center_x + outer_r * math.cos(rad)
        y2 = tick_center_y + outer_r * math.sin(rad)
        draw.line([(x1, y1), (x2, y2)], fill=DEEP_NAVY, width=SCALE)
    
    # === TYPOGRAPHY - minimal, integrated ===
    
    # Load fonts
    font_path = str(Path(__file__).parent / "fonts") + "/"
    try:
        font_main = ImageFont.truetype(font_path + "Jura-Light.ttf", 42 * SCALE)
        font_small = ImageFont.truetype(font_path + "DMMono-Regular.ttf", 16 * SCALE)
        font_accent = ImageFont.truetype(font_path + "Italiana-Regular.ttf", 28 * SCALE)
    except OSError as e:
        print(f"Warning: could not load fonts from {font_path}: {e}. Falling back to default.")
        font_main = ImageFont.load_default()
        font_small = font_main
        font_accent = font_main
    
    # Title - positioned as design element, not label
    title_text = "HARMONIC TENSION"
    draw.text((WIDTH - 180 * SCALE, HEIGHT - 280 * SCALE), title_text, 
              font=font_main, fill=DEEP_NAVY, anchor="rm")
    
    # Small reference marks - like a diagram notation
    draw.text((140 * SCALE, 180 * SCALE), "i", font=font_small, fill=MUTED_SAGE)
    
    # Subtle phrase - whispered
    draw.text((180 * SCALE, HEIGHT - 120 * SCALE), "equilibrium", 
              font=font_accent, fill=GOLDEN_OCHRE)
    
    # === FINAL REFINEMENT PASS ===
    
    # Additional fine circles for depth
    fine_circles = [
        (center_x - 50 * SCALE, center_y + 150 * SCALE, 180 * SCALE, DEEP_NAVY, 2 * SCALE),
        (center_x + 200 * SCALE, center_y - 200 * SCALE, 140 * SCALE, WARM_CORAL, 2 * SCALE),
    ]
    for fcx, fcy, fr, fc, fw in fine_circles:
        draw_circle_outline(draw, int(fcx), int(fcy), int(fr), fc, fw)
    
    # Dot grid pattern - sparse, suggesting measurement field
    grid_start_x = 1800 * SCALE
    grid_start_y = 400 * SCALE
    grid_spacing = 40 * SCALE
    dot_r = 2 * SCALE
    for row in range(5):
        for col in range(4):
            dx = grid_start_x + col * grid_spacing
            dy = grid_start_y + row * grid_spacing
            draw.ellipse([dx-dot_r, dy-dot_r, dx+dot_r, dy+dot_r], fill=MUTED_SAGE)
    
    return img


if __name__ == "__main__":
    print("Creating Harmonic Tension artwork...")
    artwork = create_artwork()
    print("Converting to CMYK...")

    icc_dir = Path(__file__).parent / "icc"
    try:
        srgb = ImageCms.getOpenProfile(str(icc_dir / "sRGB.icc"))
        cmyk_profile_path = icc_dir / "ISOcoated_v2_300_eci.icc"
        cmyk = ImageCms.getOpenProfile(str(cmyk_profile_path))
        transform = ImageCms.buildTransform(
            srgb, cmyk, "RGB", "CMYK",
            renderingIntent=ImageCms.Intent.RELATIVE_COLORIMETRIC,
            flags=ImageCms.Flags.BLACKPOINTCOMPENSATION,
        )
        artwork = ImageCms.applyTransform(artwork, transform)
        icc_bytes = cmyk_profile_path.read_bytes()
    except Exception as e:
        print(f"Warning: ICC conversion failed ({e}), using basic CMYK fallback")
        artwork = artwork.convert("CMYK")
        icc_bytes = None

    output_path = Path(__file__).parent / "renders" / "harmonic-tension.pdf"
    output_path.parent.mkdir(exist_ok=True)
    save_kwargs = {"resolution": 300}
    if icc_bytes:
        save_kwargs["icc_profile"] = icc_bytes
    artwork.save(output_path, "PDF", **save_kwargs)
    print(f"Saved to {output_path}")