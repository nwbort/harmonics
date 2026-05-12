#!/usr/bin/env python3
"""
Created by Nick Twort
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
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
    """Draw a circle outline with anti-aliasing approximation"""
    for w in range(width):
        r = radius - w
        if r > 0:
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color)

def create_artwork():
    # Create canvas with cream background
    img = Image.new('RGB', (WIDTH, HEIGHT), SOFT_CREAM)
    draw = ImageDraw.Draw(img)
    
    # === GEOMETRIC COMPOSITION ===
    
    # Central focal area - shifted right for this piece (counterpoint to first)
    center_x = WIDTH // 2
    center_y = HEIGHT // 2
    
    # === RESONANCE RINGS - concentric but offset ===
    
    # Primary resonance point - upper left quadrant
    res1_cx = center_x - 280 * SCALE
    res1_cy = center_y - 320 * SCALE
    
    # Expanding rings from first resonance point
    for i, r in enumerate([120, 200, 300, 420, 560]):
        thickness = max(2, (5 - i)) * SCALE
        draw_circle_outline(draw, int(res1_cx), int(res1_cy), int(r * SCALE), DEEP_NAVY, thickness)
    
    # Secondary resonance point - lower right, creating dialogue
    res2_cx = center_x + 320 * SCALE
    res2_cy = center_y + 280 * SCALE
    
    for i, r in enumerate([100, 180, 280, 400]):
        thickness = max(2, (4 - i)) * SCALE
        draw_circle_outline(draw, int(res2_cx), int(res2_cy), int(r * SCALE), WARM_CORAL, thickness)
    
    # === INTERFERENCE PATTERN - where waves meet ===
    
    # Single large circle suggesting the interference zone
    interference_cx = center_x + 40 * SCALE
    interference_cy = center_y - 40 * SCALE
    draw_circle_outline(draw, int(interference_cx), int(interference_cy), 
                       int(480 * SCALE), GOLDEN_OCHRE, 4 * SCALE)
    
    # === VERTICAL EMPHASIS - contrast to circular motion ===
    
    # Thin vertical lines - like standing waves
    line_positions = [
        (center_x - 520 * SCALE, 380 * SCALE, center_x - 520 * SCALE, 2200 * SCALE, DEEP_NAVY),
        (center_x - 480 * SCALE, 450 * SCALE, center_x - 480 * SCALE, 2100 * SCALE, MUTED_SAGE),
        (center_x + 560 * SCALE, 600 * SCALE, center_x + 560 * SCALE, 2600 * SCALE, GOLDEN_OCHRE),
    ]
    
    for x1, y1, x2, y2, col in line_positions:
        for w in range(2 * SCALE):
            draw.line([(x1 + w, y1), (x2 + w, y2)], fill=col, width=1)
    
    # === NODAL POINTS - filled circles at intersections ===
    
    # Large filled accent
    node1_x = center_x - 280 * SCALE
    node1_y = center_y + 140 * SCALE
    r = 42 * SCALE
    draw.ellipse([node1_x - r, node1_y - r, node1_x + r, node1_y + r], fill=WARM_CORAL)
    
    # Medium nodes
    nodes = [
        (center_x + 180 * SCALE, center_y - 450 * SCALE, 28 * SCALE, DEEP_NAVY),
        (center_x - 480 * SCALE, center_y - 120 * SCALE, 24 * SCALE, GOLDEN_OCHRE),
        (center_x + 420 * SCALE, center_y + 80 * SCALE, 20 * SCALE, MUTED_SAGE),
    ]
    for nx, ny, nr, nc in nodes:
        draw.ellipse([nx - nr, ny - nr, nx + nr, ny + nr], fill=nc)
    
    # Small constellation of dots
    small_dots = [
        (center_x - 100 * SCALE, center_y - 580 * SCALE, 10 * SCALE, WARM_CORAL),
        (center_x - 60 * SCALE, center_y - 620 * SCALE, 8 * SCALE, WARM_CORAL),
        (center_x - 140 * SCALE, center_y - 550 * SCALE, 6 * SCALE, WARM_CORAL),
        (center_x + 480 * SCALE, center_y - 180 * SCALE, 12 * SCALE, DEEP_NAVY),
        (center_x + 520 * SCALE, center_y - 140 * SCALE, 8 * SCALE, DEEP_NAVY),
        (center_x - 380 * SCALE, center_y + 480 * SCALE, 10 * SCALE, GOLDEN_OCHRE),
    ]
    for dx, dy, dr, dc in small_dots:
        draw.ellipse([dx - dr, dy - dr, dx + dr, dy + dr], fill=dc)
    
    # === ARC FRAGMENTS - broken circles suggesting decay ===
    
    # Upper arc
    arc1_cx = center_x + 200 * SCALE
    arc1_cy = center_y - 600 * SCALE
    arc1_r = 340 * SCALE
    draw.arc([arc1_cx - arc1_r, arc1_cy - arc1_r, arc1_cx + arc1_r, arc1_cy + arc1_r],
             start=45, end=160, fill=MUTED_SAGE, width=5 * SCALE)
    
    # Lower arc
    arc2_cx = center_x - 180 * SCALE
    arc2_cy = center_y + 680 * SCALE
    arc2_r = 280 * SCALE
    draw.arc([arc2_cx - arc2_r, arc2_cy - arc2_r, arc2_cx + arc2_r, arc2_cy + arc2_r],
             start=220, end=320, fill=DEEP_NAVY, width=4 * SCALE)
    
    # Side arc
    arc3_cx = center_x + 680 * SCALE
    arc3_cy = center_y + 100 * SCALE
    arc3_r = 220 * SCALE
    draw.arc([arc3_cx - arc3_r, arc3_cy - arc3_r, arc3_cx + arc3_r, arc3_cy + arc3_r],
             start=120, end=240, fill=GOLDEN_OCHRE, width=3 * SCALE)
    
    # === WAVE NOTATION - horizontal tick marks ===
    
    wave_y = center_y + 520 * SCALE
    wave_start = center_x - 400 * SCALE
    wave_spacing = 24 * SCALE
    
    for i in range(20):
        # Varying heights like a waveform
        height = int((12 + 8 * math.sin(i * 0.6)) * SCALE)
        x = wave_start + i * wave_spacing
        draw.line([(x, wave_y - height), (x, wave_y + height)], 
                  fill=MUTED_SAGE, width=2 * SCALE)
    
    # === DIAGONAL ACCENT - single line for dynamic tension ===
    
    for w in range(3 * SCALE):
        draw.line([(2000 * SCALE, 280 * SCALE + w), (600 * SCALE, 1600 * SCALE + w)], 
                  fill=WARM_CORAL, width=1)
    
    # === FINE CONCENTRIC DETAIL ===
    
    # Tight concentric circles in corner - like a tuning reference
    tune_cx = 380 * SCALE
    tune_cy = 2680 * SCALE
    for r in range(40, 120, 16):
        draw_circle_outline(draw, int(tune_cx), int(tune_cy), int(r * SCALE), DEEP_NAVY, SCALE)
    
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
    
    # Title - positioned bottom left (mirroring first piece)
    title_text = "HARMONIC RESONANCE"
    draw.text((180 * SCALE, HEIGHT - 280 * SCALE), title_text, 
              font=font_main, fill=DEEP_NAVY, anchor="lm")
    
    # Reference marks
    draw.text((WIDTH - 140 * SCALE, 180 * SCALE), "ii", font=font_small, fill=MUTED_SAGE, anchor="rm")
    
    # Subtle phrase - upper region this time
    draw.text((WIDTH - 180 * SCALE, 420 * SCALE), "sympathetic", 
              font=font_accent, fill=GOLDEN_OCHRE, anchor="rm")
    
    # === DOT GRID - different position ===
    
    grid_start_x = 280 * SCALE
    grid_start_y = 520 * SCALE
    grid_spacing = 36 * SCALE
    dot_r = 2 * SCALE
    for row in range(6):
        for col in range(3):
            dx = grid_start_x + col * grid_spacing
            dy = grid_start_y + row * grid_spacing
            draw.ellipse([dx-dot_r, dy-dot_r, dx+dot_r, dy+dot_r], fill=MUTED_SAGE)
    
    # === OUTER FRAME ELEMENT - subtle boundary ===
    
    # Partial rectangle suggesting containment
    margin = 120 * SCALE
    corner_len = 180 * SCALE
    line_w = 2 * SCALE
    
    # Top left corner
    draw.line([(margin, margin), (margin + corner_len, margin)], fill=DEEP_NAVY, width=line_w)
    draw.line([(margin, margin), (margin, margin + corner_len)], fill=DEEP_NAVY, width=line_w)
    
    # Bottom right corner
    draw.line([(WIDTH - margin, HEIGHT - margin), (WIDTH - margin - corner_len, HEIGHT - margin)], 
              fill=DEEP_NAVY, width=line_w)
    draw.line([(WIDTH - margin, HEIGHT - margin), (WIDTH - margin, HEIGHT - margin - corner_len)], 
              fill=DEEP_NAVY, width=line_w)
    
    return img


if __name__ == "__main__":
    print("Creating Harmonic Resonance artwork...")
    artwork = create_artwork()
    
    print("Refining composition...")
    
    # Save the artwork
    output_path = Path(__file__).parent / "renders" / "harmonic-resonance.png"
    output_path.parent.mkdir(exist_ok=True)
    artwork.save(output_path, "PNG", dpi=(300, 300))
    print(f"Saved to {output_path}")