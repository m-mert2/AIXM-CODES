import re
import xml.etree.ElementTree as ET

# Namespace map
NS = {
    "http://www.aixm.aero/schema/5.1.1":         "aixm",
    "http://www.aixm.aero/schema/5.1.1/message": "message",
    "http://www.opengis.net/gml/3.2":             "gml",
}

def _qname(tag):
    """'{uri}LocalName' → 'prefix:LocalName'"""
    if tag.startswith("{"):
        uri, local = tag[1:].split("}", 1)
        prefix = NS.get(uri, "ns")
        return f"{prefix}:{local}"
    return tag

# ── token extraction ────────────────────────────────────────────────────────

def xml_to_tokens(xml_string):
    tokens = []
    pattern = re.compile(
        r'<(/?)([a-zA-Z][a-zA-Z0-9_]*:[a-zA-Z][a-zA-Z0-9_]*)([^>]*?)(/?)>'
    )
    for m in pattern.finditer(xml_string):
        closing, tag, _, self_close = m.group(1), m.group(2), m.group(3), m.group(4)
        if closing:
            tokens.append("/" + tag)
        elif self_close:
            tokens.append(tag)
        else:
            tokens.append(tag)
    return tokens


def detect_feature(xml_string):
    """İlk aixm: tagından feature adını döndürür."""
    m = re.search(r'<aixm:([a-zA-Z][a-zA-Z0-9_]*)[^/]', xml_string)
    return m.group(1) if m else None


def xml_to_pda_tokens(xml_string):
    """
    PDA'nın beklediği üst-düzey token listesini döndürür.
    *TimeSlice, geometri ve boilerplate iç etiketleri filtreler.
    """
    all_tokens = xml_to_tokens(xml_string)
    feature = detect_feature(xml_string)
    if not feature:
        return all_tokens

    main_tag = "aixm:" + feature

    SKIP_EXACT = {
        "gml:validTime", "aixm:interpretation",
        "aixm:ElevatedPoint", "gml:ElevatedPoint",
        "gml:Envelope", "gml:Point", "gml:pos",
        "aixm:SurfaceCharacteristics", "aixm:VerticalStructurePart",
        "aixm:Note", "aixm:AircraftCharacteristics",
        "aixm:LinguisticNote",
    }
    SKIP_SUFFIXES = ("TimeSlice", "Point", "Geometry", "Curve", "Polygon")

    pda_tokens = []
    skip_depth = 0
    skip_tag = None

    for token in all_tokens:
        is_closing = token.startswith("/")
        bare = token[1:] if is_closing else token

        if skip_depth > 0:
            if not is_closing and bare == skip_tag:
                skip_depth += 1
            elif is_closing and bare == skip_tag:
                skip_depth -= 1
            continue

        if token == main_tag or token == "/" + main_tag:
            pda_tokens.append(token)
            continue

        if is_closing:
            continue

        if bare in SKIP_EXACT or any(bare.endswith(s) for s in SKIP_SUFFIXES):
            skip_tag = bare
            skip_depth = 1
            continue

        pda_tokens.append(token)

    return pda_tokens


# ── AIXMBasicMessage splitter ────────────────────────────────────────────────

def split_aixm_message(xml_string):
    """
    AIXMBasicMessage içindeki her message:hasMember bloğunu ayrı XML string'i
    olarak döndürür.

    Dönüş: list of str  (her biri tek bir feature'ın XML'i)
    """
    try:
        # namespace'leri koru
        root = ET.fromstring(xml_string)
    except ET.ParseError as e:
        line, col = e.position if hasattr(e, 'position') else (None, None)
        raise ValueError(f"XML parse hatası — satır {line}, sütun {col}: {e}") from e

    members = []
    for child in root:
        if _qname(child.tag) == "message:hasMember":
            for item in child:
                if _qname(item.tag).startswith("aixm:"):
                    # ET.tostring ile tekrar string'e çevir
                    # namespace declaration'ları ata
                    _register_namespaces()
                    members.append(ET.tostring(item, encoding="unicode"))
                    break
    return members


def is_aixm_basic_message(xml_string):
    """XML bir AIXMBasicMessage zarfı mı?"""
    return bool(re.search(r'<message:AIXMBasicMessage', xml_string) or
                re.search(r'AIXMBasicMessage', xml_string[:500]))


def _register_namespaces():
    for uri, prefix in NS.items():
        ET.register_namespace(prefix, uri)
    # diğer ns'ler için de kaydet
    ET.register_namespace("xlink",  "http://www.w3.org/1999/xlink")
    ET.register_namespace("gmd",    "http://www.isotc211.org/2005/gmd")
    ET.register_namespace("gco",    "http://www.isotc211.org/2005/gco")
    ET.register_namespace("xsi",    "http://www.w3.org/2001/XMLSchema-instance")
