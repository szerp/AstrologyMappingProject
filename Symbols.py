import xml.etree.ElementTree as ET

def extract_symbol_ids(svg_path):
    """Extracts symbol IDs from an SVG file, ignoring malformed sections."""
    symbol_ids = []
    try:
        # Parse the file incrementally
        for event, elem in ET.iterparse(svg_path, events=("start", "end")):
            if event == "start" and elem.tag.endswith("symbol"):
                symbol_id = elem.attrib.get("id")
                if symbol_id:
                    symbol_ids.append(symbol_id)
            elem.clear()  # Free memory
    except ET.ParseError as e:
        print(f"Warning: Parse error encountered - {e}")
    return symbol_ids

# Example usage
svg_file_path = r"C:\Users\Nyahmii\Documents\AstrologyMappingProject\generated_charts\A and B - Synastry Chart.SVG"
symbol_ids = extract_symbol_ids(svg_file_path)

print("Extracted Symbol IDs:")
for symbol_id in symbol_ids:
    print(symbol_id)
