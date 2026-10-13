import math
import os
import subprocess
from PIL import Image, ImageDraw, ImageFilter

def create_recoreale_art(size=1024, is_mac=True):
    # Create high-res canvas (supersampled 2x for ultra smoothness)
    S = size * 2
    canvas = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)
    
    center = S / 2
    
    if is_mac:
        # macOS squircle container with drop shadow
        # Squircle bounds: standard macOS icon grid has padding
        pad = S * 0.11
        w = S - 2 * pad
        h = S - 2 * pad
        corner_r = S * 0.21
        
        # Soft drop shadow
        shadow = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow)
        shadow_draw.rounded_rectangle(
            [pad, pad + S * 0.03, pad + w, pad + h + S * 0.03],
            radius=corner_r,
            fill=(0, 0, 0, 110)
        )
        shadow = shadow.filter(ImageFilter.GaussianBlur(S * 0.035))
        canvas.alpha_composite(shadow)
        
        # Background Squircle base mask
        squircle_mask = Image.new("L", (S, S), 0)
        mask_draw = ImageDraw.Draw(squircle_mask)
        mask_draw.rounded_rectangle([pad, pad, pad + w, pad + h], radius=corner_r, fill=255)
        
        # Base Gradient: Deep luxury slate/indigo with subtle warm underglow
        base = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        for y in range(int(pad), int(pad + h)):
            t = (y - pad) / h
            # Deep obsidian indigo (#0D0D14 to #181829)
            r = int(14 * (1 - t) + 26 * t)
            g = int(14 * (1 - t) + 22 * t)
            b = int(22 * (1 - t) + 45 * t)
            line_img = Image.new("RGBA", (S, 1), (r, g, b, 255))
            base.paste(line_img, (0, y))
            
        # Add subtle radial lighting from top
        light_overlay = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        light_draw = ImageDraw.Draw(light_overlay)
        light_draw.ellipse(
            [center - w*0.4, pad - h*0.2, center + w*0.4, pad + h*0.6],
            fill=(99, 102, 241, 60)
        )
        light_overlay = light_overlay.filter(ImageFilter.GaussianBlur(S * 0.08))
        base = Image.alpha_composite(base, light_overlay)

        # Composite base into squircle
        canvas.paste(base, (0, 0), squircle_mask)
        
        # Elegant inner border (1.5px at 1024)
        border_overlay = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        border_draw = ImageDraw.Draw(border_overlay)
        border_draw.rounded_rectangle(
            [pad, pad, pad + w, pad + h],
            radius=corner_r,
            outline=(255, 255, 255, 45),
            width=int(S * 0.003)
        )
        canvas = Image.alpha_composite(canvas, border_overlay)
    else:
        # Non-mac/universal: Circular or full rounded container
        pad = S * 0.06
        w = S - 2 * pad
        h = S - 2 * pad
        corner_r = S * 0.28
        
        mask = Image.new("L", (S, S), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle([pad, pad, pad + w, pad + h], radius=corner_r, fill=255)
        
        base = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        for y in range(int(pad), int(pad + h)):
            t = (y - pad) / h
            r = int(15 * (1 - t) + 28 * t)
            g = int(15 * (1 - t) + 24 * t)
            b = int(24 * (1 - t) + 48 * t)
            line_img = Image.new("RGBA", (S, 1), (r, g, b, 255))
            base.paste(line_img, (0, y))
            
        canvas.paste(base, (0, 0), mask)
        
        border_overlay = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        border_draw = ImageDraw.Draw(border_overlay)
        border_draw.rounded_rectangle(
            [pad, pad, pad + w, pad + h],
            radius=corner_r,
            outline=(255, 255, 255, 40),
            width=int(S * 0.003)
        )
        canvas = Image.alpha_composite(canvas, border_overlay)

    # Now draw the iconic RecoreAle emblem:
    # 1. Outer recording wave / viewfinder arcs (subtle, high-tech)
    emblem_layer = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    emblem_draw = ImageDraw.Draw(emblem_layer)
    
    radius_outer = S * 0.26
    emblem_draw.ellipse(
        [center - radius_outer, center - radius_outer, center + radius_outer, center + radius_outer],
        outline=(140, 150, 255, 50),
        width=int(S * 0.008)
    )
    
    # Outer glowing pulse ring
    glow_ring = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_ring)
    glow_draw.ellipse(
        [center - radius_outer, center - radius_outer, center + radius_outer, center + radius_outer],
        outline=(239, 68, 68, 120),
        width=int(S * 0.015)
    )
    glow_ring = glow_ring.filter(ImageFilter.GaussianBlur(S * 0.02))
    emblem_layer = Image.alpha_composite(emblem_layer, glow_ring)

    # 2. Modern Recording Aperture / Lens core
    radius_mid = S * 0.20
    # Gradient filled inner ring
    for r in range(int(radius_mid), int(radius_mid - S * 0.04), -1):
        alpha = int(200 * ((r - (radius_mid - S*0.04)) / (S*0.04)))
        emblem_draw.ellipse(
            [center - r, center - r, center + r, center + r],
            outline=(30, 27, 75, alpha),
            width=2
        )
    
    # 3. Viewfinder Focus Brackets (representing video capture / framing)
    bracket_len = S * 0.07
    bracket_rad = S * 0.22
    bracket_w = int(S * 0.016)
    bracket_color = (255, 255, 255, 220)
    
    # Top-Left Bracket
    emblem_draw.line([center - bracket_rad, center - bracket_rad + bracket_len, center - bracket_rad, center - bracket_rad], fill=bracket_color, width=bracket_w)
    emblem_draw.line([center - bracket_rad, center - bracket_rad, center - bracket_rad + bracket_len, center - bracket_rad], fill=bracket_color, width=bracket_w)
    
    # Top-Right Bracket
    emblem_draw.line([center + bracket_rad, center - bracket_rad + bracket_len, center + bracket_rad, center - bracket_rad], fill=bracket_color, width=bracket_w)
    emblem_draw.line([center + bracket_rad, center - bracket_rad, center + bracket_rad - bracket_len, center - bracket_rad], fill=bracket_color, width=bracket_w)
    
    # Bottom-Left Bracket
    emblem_draw.line([center - bracket_rad, center + bracket_rad - bracket_len, center - bracket_rad, center + bracket_rad], fill=bracket_color, width=bracket_w)
    emblem_draw.line([center - bracket_rad, center + bracket_rad, center - bracket_rad + bracket_len, center + bracket_rad], fill=bracket_color, width=bracket_w)
    
    # Bottom-Right Bracket
    emblem_draw.line([center + bracket_rad, center + bracket_rad - bracket_len, center + bracket_rad, center + bracket_rad], fill=bracket_color, width=bracket_w)
    emblem_draw.line([center + bracket_rad, center + bracket_rad, center + bracket_rad - bracket_len, center + bracket_rad], fill=bracket_color, width=bracket_w)
    
    # 4. Central Glowing "Record Core" (Vibrant Crimson & Coral Pulse)
    core_rad = S * 0.12
    
    # Core drop glow
    core_glow = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    core_glow_draw = ImageDraw.Draw(core_glow)
    core_glow_draw.ellipse(
        [center - core_rad * 1.5, center - core_rad * 1.5, center + core_rad * 1.5, center + core_rad * 1.5],
        fill=(244, 63, 94, 180)
    )
    core_glow = core_glow.filter(ImageFilter.GaussianBlur(S * 0.035))
    emblem_layer = Image.alpha_composite(emblem_layer, core_glow)
    
    # Core disc: radial gradient crimson (#FF1E56 -> #E11D48 -> #BE123C)
    core_img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    core_draw = ImageDraw.Draw(core_img)
    for r in range(int(core_rad), 0, -2):
        t = r / core_rad
        cr = int(255 * t + 225 * (1 - t))
        cg = int(70 * t + 20 * (1 - t))
        cb = int(90 * t + 60 * (1 - t))
        core_draw.ellipse(
            [center - r, center - r, center + r, center + r],
            fill=(cr, cg, cb, 255)
        )
    
    # Gloss highlight on top edge of core
    highlight = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    hl_draw = ImageDraw.Draw(highlight)
    hl_draw.ellipse(
        [center - core_rad * 0.75, center - core_rad * 0.85, center + core_rad * 0.75, center - core_rad * 0.1],
        fill=(255, 255, 255, 120)
    )
    highlight = highlight.filter(ImageFilter.GaussianBlur(S * 0.012))
    core_img = Image.alpha_composite(core_img, highlight)
    
    # Central Stylized Play/Record Precision Core Dot or Crisp Play Arrow
    # A sleek rightward triangle (play / record fusion)
    tri_s = S * 0.048
    tri_pts = [
        (center - tri_s * 0.6 + tri_s * 0.1, center - tri_s),
        (center + tri_s * 1.0 + tri_s * 0.1, center),
        (center - tri_s * 0.6 + tri_s * 0.1, center + tri_s)
    ]
    core_draw.polygon(tri_pts, fill=(255, 255, 255, 245))
    
    emblem_layer = Image.alpha_composite(emblem_layer, core_img)
    canvas = Image.alpha_composite(canvas, emblem_layer)
    
    # Downsample cleanly with LANCZOS to target size
    final_img = canvas.resize((size, size), Image.Resampling.LANCZOS)
    return final_img

def main():
    os.makedirs("public/app-icons", exist_ok=True)
    os.makedirs("icons/icons/mac", exist_ok=True)
    os.makedirs("icons/icons/png", exist_ok=True)
    os.makedirs("icons/icons/win", exist_ok=True)
    
    sizes = [16, 32, 64, 128, 256, 512, 1024]
    
    print("Generating RecoreAle master icons...")
    mac_1024 = create_recoreale_art(1024, is_mac=True)
    univ_1024 = create_recoreale_art(1024, is_mac=False)
    
    # Save public/app-icons
    for sz in sizes:
        mac_img = mac_1024.resize((sz, sz), Image.Resampling.LANCZOS)
        univ_img = univ_1024.resize((sz, sz), Image.Resampling.LANCZOS)
        
        mac_img.save(f"public/app-icons/recorealemac-{sz}.png", "PNG")
        univ_img.save(f"public/app-icons/recoreale-{sz}.png", "PNG")
        print(f"Generated public/app-icons/recoreale*-{sz}.png")
        
    # Save icons/icons/png
    png_sizes = [16, 24, 32, 48, 64, 128, 256, 512, 1024]
    for sz in png_sizes:
        p_img = univ_1024.resize((sz, sz), Image.Resampling.LANCZOS)
        p_img.save(f"icons/icons/png/{sz}x{sz}.png", "PNG")
    print("Generated icons/icons/png/...")
    
    # Save Windows ICO
    ico_sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    univ_1024.save("icons/icons/win/icon.ico", format="ICO", sizes=ico_sizes)
    print("Generated icons/icons/win/icon.ico")
    
    # Generate macOS ICNS via iconutil
    iconset_dir = "icons/icons/mac/icon.iconset"
    os.makedirs(iconset_dir, exist_ok=True)
    
    mac_icon_map = {
        "icon_16x16.png": 16,
        "icon_16x16@2x.png": 32,
        "icon_32x32.png": 32,
        "icon_32x32@2x.png": 64,
        "icon_128x128.png": 128,
        "icon_128x128@2x.png": 256,
        "icon_256x256.png": 256,
        "icon_256x256@2x.png": 512,
        "icon_512x512.png": 512,
        "icon_512x512@2x.png": 1024,
    }
    
    for filename, sz in mac_icon_map.items():
        m_img = mac_1024.resize((sz, sz), Image.Resampling.LANCZOS)
        m_img.save(os.path.join(iconset_dir, filename), "PNG")
        
    subprocess.run(["iconutil", "-c", "icns", iconset_dir, "-o", "icons/icons/mac/icon.icns"], check=True)
    # Clean up iconset
    import shutil
    shutil.rmtree(iconset_dir)
    print("Generated icons/icons/mac/icon.icns successfully!")

if __name__ == "__main__":
    main()
