# Icon Directory

Place your extension icon here as `icon.png`.

## Recommended Specifications:
- **Format**: PNG
- **Size**: 256x256 pixels
- **Style**: Simple, recognizable icon
- **Transparency**: Supported

## Icon Ideas:
- Magnifying glass (search symbol)
- AI/Brain icon
- Question mark
- Lightning bolt (for quick search)
- Combination of multiple symbols

## Creating an Icon:

### Option 1: Use an existing icon
Download a free icon from:
- https://www.flaticon.com/
- https://fontawesome.com/
- https://icons8.com/

### Option 2: Convert Font Awesome to PNG
```bash
# Install ImageMagick if needed
sudo apt install imagemagick

# Create a simple text-based icon (example)
convert -size 256x256 xc:transparent \
  -font DejaVu-Sans-Bold -pointsize 180 \
  -fill '#4A90E2' -gravity center \
  -annotate +0+0 'AI' \
  icon.png
```

### Option 3: Use GIMP or Inkscape
Design a custom icon with these free tools.

## Temporary Solution:
If you don't have an icon yet, Ulauncher will use a default placeholder.
The extension will still work perfectly without a custom icon!
