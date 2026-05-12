#!/usr/bin/env python3
"""
Harmonic Orbit - A visual expression of gravitational pull and elliptical paths
Created by Nick Twort
"""

from pathlib import Path
from PIL import Image, ImageCms, ImageDraw, ImageFont
import math

# Canvas dimensions (massive resolution for print quality)
WIDTH = 7200
HEIGHT = 9600
SCALE = 3  # Scale factor for all elements

# Colour palette - constrained, intentional (consistent with series)
DEEP_NAVY = (18, 32, 47)
WARM_CORAL = (204, 108, 92)
SOFT_CREAM = (248, 244, 236)
GOLDEN_OCHRE = (198, 156, 89)
MUTED_SAGE = (142, 159, 145)

def draw_circle_outline(draw, cx, cy, radius, color, width=3):
    """Draw a circle outline"""
    for w in range(width):
        r = radius - w
        if r > 0:
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color)

def draw_ellipse_outline(draw, cx, cy, rx, ry, color, width=3, rotation=0):
    """Draw a rotated ellipse outline using point sampling"""
    steps = 1440  # 0.25-degree steps — smooth at high resolution
    rot_rad = math.radians(rotation)
    cos_rot = math.cos(rot_rad)
    sin_rot = math.sin(rot_rad)
    points = []
    for i in range(steps):
        rad = 2 * math.pi * i / steps
        x = rx * math.cos(rad)
        y = ry * math.sin(rad)
        points.append((cx + x * cos_rot - y * sin_rot,
                       cy + x * sin_rot + y * cos_rot))

    for i in range(steps):
        draw.line([points[i], points[(i + 1) % steps]], fill=color, width=width)

def create_artwork():
    # Create canvas with cream background
    img = Image.new('RGB', (WIDTH, HEIGHT), SOFT_CREAM)
    draw = ImageDraw.Draw(img)
    
    # === GEOMETRIC COMPOSITION ===
    
    center_x = WIDTH // 2
    center_y = HEIGHT // 2 - 80 * SCALE
    
    # === PRIMARY GRAVITATIONAL CENTRE ===
    
    # Large filled circle - the "mass" at centre
    mass_cx = center_x - 60 * SCALE
    mass_cy = center_y + 40 * SCALE
    mass_r = 65 * SCALE
    draw.ellipse([mass_cx - mass_r, mass_cy - mass_r, 
                  mass_cx + mass_r, mass_cy + mass_r], fill=DEEP_NAVY)
    
    # === ORBITAL ELLIPSES - eccentric paths ===
    
    # Primary orbit - wide ellipse
    draw_ellipse_outline(draw, mass_cx, mass_cy, 
                        380 * SCALE, 520 * SCALE, DEEP_NAVY, 4 * SCALE, rotation=15)
    
    # Secondary orbit - tighter, different angle
    draw_ellipse_outline(draw, mass_cx, mass_cy,
                        280 * SCALE, 420 * SCALE, WARM_CORAL, 3 * SCALE, rotation=-25)
    
    # Tertiary orbit - highly eccentric
    draw_ellipse_outline(draw, mass_cx + 80 * SCALE, mass_cy - 60 * SCALE,
                        180 * SCALE, 580 * SCALE, GOLDEN_OCHRE, 3 * SCALE, rotation=70)
    
    # Outer orbit - vast, barely curved appearance
    draw_ellipse_outline(draw, mass_cx, mass_cy,
                        620 * SCALE, 720 * SCALE, MUTED_SAGE, 2 * SCALE, rotation=5)
    
    # === SECONDARY MASS - binary system suggestion ===
    
    mass2_cx = center_x + 420 * SCALE
    mass2_cy = center_y - 280 * SCALE
    mass2_r = 38 * SCALE
    draw.ellipse([mass2_cx - mass2_r, mass2_cy - mass2_r,
                  mass2_cx + mass2_r, mass2_cy + mass2_r], fill=WARM_CORAL)
    
    # Small orbits around secondary mass
    draw_circle_outline(draw, int(mass2_cx), int(mass2_cy), int(85 * SCALE), WARM_CORAL, 2 * SCALE)
    draw_circle_outline(draw, int(mass2_cx), int(mass2_cy), int(130 * SCALE), WARM_CORAL, 2 * SCALE)
    
    # === LAGRANGE POINTS - small markers at equilibrium ===
    
    lagrange_points = [
        (center_x - 480 * SCALE, center_y - 180 * SCALE, 14 * SCALE, GOLDEN_OCHRE),
        (center_x + 580 * SCALE, center_y + 120 * SCALE, 12 * SCALE, GOLDEN_OCHRE),
        (center_x - 120 * SCALE, center_y + 620 * SCALE, 16 * SCALE, GOLDEN_OCHRE),
        (center_x + 200 * SCALE, center_y - 580 * SCALE, 10 * SCALE, GOLDEN_OCHRE),
        (center_x - 380 * SCALE, center_y + 380 * SCALE, 11 * SCALE, GOLDEN_OCHRE),
    ]
    for lx, ly, lr, lc in lagrange_points:
        draw.ellipse([lx - lr, ly - lr, lx + lr, ly + lr], fill=lc)
    
    # === TRAJECTORY ARCS - partial paths ===
    
    # Incoming trajectory
    arc1_cx = center_x - 600 * SCALE
    arc1_cy = center_y - 400 * SCALE
    arc1_r = 450 * SCALE
    draw.arc([arc1_cx - arc1_r, arc1_cy - arc1_r, arc1_cx + arc1_r, arc1_cy + arc1_r],
             start=280, end=350, fill=DEEP_NAVY, width=4 * SCALE)
    
    # Escape trajectory
    arc2_cx = center_x + 500 * SCALE
    arc2_cy = center_y + 600 * SCALE
    arc2_r = 380 * SCALE
    draw.arc([arc2_cx - arc2_r, arc2_cy - arc2_r, arc2_cx + arc2_r, arc2_cy + arc2_r],
             start=80, end=160, fill=MUTED_SAGE, width=3 * SCALE)
    
    # === RADIAL LINES - gravitational field suggestion ===
    
    num_rays = 24
    inner_r = 90 * SCALE
    outer_r = 160 * SCALE
    
    for i in range(num_rays):
        angle = (360 / num_rays) * i
        # Skip some for asymmetry
        if i % 3 == 1:
            continue
        rad = math.radians(angle)
        x1 = mass_cx + inner_r * math.cos(rad)
        y1 = mass_cy + inner_r * math.sin(rad)
        x2 = mass_cx + outer_r * math.cos(rad)
        y2 = mass_cy + outer_r * math.sin(rad)
        draw.line([(x1, y1), (x2, y2)], fill=DEEP_NAVY, width=SCALE)
    
    # === VELOCITY VECTORS - directional marks ===
    
    # Arrow-like marks showing motion direction
    vectors = [
        (center_x - 320 * SCALE, center_y - 420 * SCALE, 45, 60 * SCALE, WARM_CORAL),
        (center_x + 380 * SCALE, center_y + 320 * SCALE, 225, 50 * SCALE, WARM_CORAL),
        (center_x - 180 * SCALE, center_y + 480 * SCALE, 135, 45 * SCALE, DEEP_NAVY),
    ]
    
    for vx, vy, angle, length, color in vectors:
        rad = math.radians(angle)
        x2 = vx + length * math.cos(rad)
        y2 = vy - length * math.sin(rad)
        draw.line([(vx, vy), (x2, y2)], fill=color, width=3 * SCALE)
        # Small arrowhead
        arrow_len = 15 * SCALE
        for offset in [25, -25]:
            arr_rad = math.radians(angle + 180 + offset)
            ax = x2 + arrow_len * math.cos(arr_rad)
            ay = y2 - arrow_len * math.sin(arr_rad)
            draw.line([(x2, y2), (ax, ay)], fill=color, width=2 * SCALE)
    
    # === PERIHELION/APHELION MARKERS ===
    
    # Small tick marks at orbital extremes
    peri_marks = [
        (center_x - 440 * SCALE, center_y + 180 * SCALE, 0),
        (center_x + 340 * SCALE, center_y - 120 * SCALE, 90),
        (center_x + 80 * SCALE, center_y + 540 * SCALE, 45),
    ]
    
    mark_len = 20 * SCALE
    for mx, my, angle in peri_marks:
        rad = math.radians(angle)
        x1 = mx - mark_len * math.cos(rad)
        y1 = my - mark_len * math.sin(rad)
        x2 = mx + mark_len * math.cos(rad)
        y2 = my + mark_len * math.sin(rad)
        draw.line([(x1, y1), (x2, y2)], fill=MUTED_SAGE, width=2 * SCALE)
    
    # === DISTANT BODIES - constellation ===
    
    distant = [
        (220 * SCALE, 380 * SCALE, 8 * SCALE, DEEP_NAVY),
        (260 * SCALE, 420 * SCALE, 6 * SCALE, DEEP_NAVY),
        (200 * SCALE, 450 * SCALE, 5 * SCALE, DEEP_NAVY),
        (2120 * SCALE, 2680 * SCALE, 9 * SCALE, MUTED_SAGE),
        (2180 * SCALE, 2720 * SCALE, 7 * SCALE, MUTED_SAGE),
        (2100 * SCALE, 2750 * SCALE, 5 * SCALE, MUTED_SAGE),
    ]
    for dx, dy, dr, dc in distant:
        draw.ellipse([dx - dr, dy - dr, dx + dr, dy + dr], fill=dc)
    
    # === ORBITAL PERIOD NOTATION - hash marks ===
    
    hash_cx = center_x + 620 * SCALE
    hash_cy = center_y - 480 * SCALE
    hash_spacing = 18 * SCALE
    
    for i in range(8):
        hx = hash_cx + i * hash_spacing
        draw.line([(hx, hash_cy - 12 * SCALE), (hx, hash_cy + 12 * SCALE)],
                  fill=GOLDEN_OCHRE, width=2 * SCALE)
    
    # === FOCUS POINTS - ellipse foci markers ===
    
    # Small circles marking where foci would be
    foci = [
        (mass_cx - 180 * SCALE, mass_cy + 40 * SCALE, 8 * SCALE, DEEP_NAVY),
        (mass_cx + 180 * SCALE, mass_cy - 40 * SCALE, 8 * SCALE, DEEP_NAVY),
    ]
    for fx, fy, fr, fc in foci:
        draw_circle_outline(draw, int(fx), int(fy), int(fr), fc, 2 * SCALE)
    
    # === TYPOGRAPHY ===
    
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
    
    # Title - centred bottom
    title_text = "HARMONIC ORBIT"
    draw.text((center_x, HEIGHT - 280 * SCALE), title_text,
              font=font_main, fill=DEEP_NAVY, anchor="mm")
    
    # Reference marks
    draw.text((WIDTH - 140 * SCALE, HEIGHT - 140 * SCALE), "iii", font=font_small, fill=MUTED_SAGE, anchor="rm")
    draw.text((WIDTH - 140 * SCALE, 180 * SCALE), "·", font=font_small, fill=MUTED_SAGE, anchor="rm")
    
    # Subtle phrase
    draw.text((180 * SCALE, 380 * SCALE), "perihelion",
              font=font_accent, fill=GOLDEN_OCHRE)
    
    # === DOT GRID ===
    
    grid_start_x = WIDTH - 380 * SCALE
    grid_start_y = HEIGHT - 620 * SCALE
    grid_spacing = 32 * SCALE
    dot_r = 2 * SCALE
    
    for row in range(5):
        for col in range(5):
            dx = grid_start_x + col * grid_spacing
            dy = grid_start_y + row * grid_spacing
            draw.ellipse([dx-dot_r, dy-dot_r, dx+dot_r, dy+dot_r], fill=MUTED_SAGE)
    
    # === CORNER FRAMES ===
    
    margin = 120 * SCALE
    corner_len = 160 * SCALE
    line_w = 2 * SCALE
    
    # Top right corner
    draw.line([(WIDTH - margin, margin), (WIDTH - margin - corner_len, margin)], 
              fill=DEEP_NAVY, width=line_w)
    draw.line([(WIDTH - margin, margin), (WIDTH - margin, margin + corner_len)], 
              fill=DEEP_NAVY, width=line_w)
    
    # Bottom left corner
    draw.line([(margin, HEIGHT - margin), (margin + corner_len, HEIGHT - margin)],
              fill=DEEP_NAVY, width=line_w)
    draw.line([(margin, HEIGHT - margin), (margin, HEIGHT - margin - corner_len)],
              fill=DEEP_NAVY, width=line_w)
    
    return img


if __name__ == "__main__":
    print("Creating Harmonic Orbit artwork...")
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

    output_path = Path(__file__).parent / "renders" / "harmonic-orbit.pdf"
    output_path.parent.mkdir(exist_ok=True)
    save_kwargs = {"resolution": 300}
    if icc_bytes:
        save_kwargs["icc_profile"] = icc_bytes
    artwork.save(output_path, "PDF", **save_kwargs)
    print(f"Saved to {output_path}")