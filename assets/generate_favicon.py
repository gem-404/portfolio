import io
import os

import cairosvg
from PIL import Image

# The favicon SVG — just the mark, no text
favicon_svg = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <rect width="200" height="200" rx="40" fill="#020817"/>
  <polygon points="100,18 156,50 156,114 100,146 44,114 44,50"
           fill="#0f172a"/>
  <polygon points="100,18 156,50 156,114 100,146 44,114 44,50"
           fill="none" stroke="#63b3ed" stroke-width="3.5"/>
  <polygon points="100,34 144,58 144,106 100,130 56,106 56,58"
           fill="none" stroke="#7c3aed" stroke-width="2" opacity="0.5"/>

  <!-- E -->
  <line x1="62"  y1="72"  x2="62"  y2="128" stroke="#63b3ed" stroke-width="5" stroke-linecap="round"/>
  <line x1="62"  y1="72"  x2="88"  y2="72"  stroke="#63b3ed" stroke-width="5" stroke-linecap="round"/>
  <line x1="62"  y1="100" x2="84"  y2="100" stroke="#63b3ed" stroke-width="5" stroke-linecap="round"/>
  <line x1="62"  y1="128" x2="88"  y2="128" stroke="#63b3ed" stroke-width="5" stroke-linecap="round"/>

  <!-- M -->
  <line x1="96"  y1="128" x2="96"  y2="72"  stroke="#63b3ed" stroke-width="5" stroke-linecap="round"/>
  <line x1="96"  y1="72"  x2="114" y2="98"  stroke="#63b3ed" stroke-width="5" stroke-linecap="round"/>
  <line x1="114" y1="98"  x2="132" y2="72"  stroke="#63b3ed" stroke-width="5" stroke-linecap="round"/>
  <line x1="132" y1="72"  x2="132" y2="128" stroke="#63b3ed" stroke-width="5" stroke-linecap="round"/>

  <!-- vertex dots -->
  <circle cx="100" cy="18"  r="4" fill="#63b3ed"/>
  <circle cx="156" cy="50"  r="4" fill="#7c3aed"/>
  <circle cx="156" cy="114" r="4" fill="#63b3ed"/>
  <circle cx="100" cy="146" r="4" fill="#7c3aed"/>
  <circle cx="44"  cy="114" r="4" fill="#63b3ed"/>
  <circle cx="44"  cy="50"  r="4" fill="#7c3aed"/>
</svg>
"""

output_dir = os.path.dirname(os.path.abspath(__file__))

# Generate PNG sizes
sizes = [16, 32, 48, 64, 128, 256]
pngs = []

for size in sizes:
    png_data = cairosvg.svg2png(
        bytestring=favicon_svg.encode(), output_width=size, output_height=size
    )
    img = Image.open(io.BytesIO(png_data)).convert("RGBA")
    pngs.append(img)
    print(f"Generated {size}x{size}")

# Save as .ico (contains all sizes)
ico_path = os.path.join(output_dir, "favicon.ico")
pngs[0].save(
    ico_path, format="ICO", sizes=[(s, s) for s in sizes], append_images=pngs[1:]
)
print(f"Saved favicon.ico")

# Also save a 512x512 PNG for og:image / apple touch icon
png_512_data = cairosvg.svg2png(
    bytestring=favicon_svg.encode(), output_width=512, output_height=512
)
png_path = os.path.join(output_dir, "favicon-512.png")
with open(png_path, "wb") as f:
    f.write(png_512_data)
print(f"Saved favicon-512.png")
