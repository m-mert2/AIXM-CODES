"""
Donlon.xml'den harita için GeoJSON benzeri feature listesi çıkarır.
"""
import xml.etree.ElementTree as ET
import re, json
from collections import defaultdict

NS = {
    "http://www.aixm.aero/schema/5.1.1": "aixm",
    "http://www.aixm.aero/schema/5.1.1/message": "message",
    "http://www.opengis.net/gml/3.2": "gml",
    "http://www.w3.org/1999/xlink": "xlink",
}
def qn(tag):
    if not isinstance(tag, str): return ""
    if tag.startswith("{"):
        uri, local = tag[1:].split("}", 1)
        return NS.get(uri, "ns") + ":" + local
    return tag

def _text(elem, path):
    """Basit tag arama."""
    for child in elem.iter():
        if qn(child.tag) == path and child.text and child.text.strip():
            return child.text.strip()
    return None

def _parse_pos(text):
    """'lat lon' → [lon, lat] (GeoJSON order)"""
    nums = text.split()
    if len(nums) >= 2:
        try:
            lat, lon = float(nums[0]), float(nums[1])
            return [lon, lat]
        except: pass
    return None

def _parse_poslist(text):
    """'lat1 lon1 lat2 lon2 ...' → [[lon1,lat1], [lon2,lat2], ...]"""
    nums = [x for x in text.split() if re.match(r'-?\d+\.?\d*', x)]
    coords = []
    for i in range(0, len(nums)-1, 2):
        try:
            lat, lon = float(nums[i]), float(nums[i+1])
            coords.append([lon, lat])
        except: pass
    return coords if len(coords) >= 2 else []

# Kategoriler ve renkleri
CATEGORIES = {
    "Airspace":              {"color": "#4a9eff", "icon": "✈️",  "label": "Hava Sahası"},
    "AirportHeliport":       {"color": "#ffd700", "icon": "🏢",  "label": "Havalimanı"},
    "Runway":                {"color": "#ff9a3c", "icon": "🛬",  "label": "Pist"},
    "RunwayElement":         {"color": "#ff9a3c", "icon": "🛬",  "label": "Pist Elemanı"},
    "RunwayCentrelinePoint": {"color": "#ffcc44", "icon": "📍",  "label": "Pist Merkez Noktası"},
    "GuidanceLine":          {"color": "#44ddaa", "icon": "〰️", "label": "Yönlendirme Çizgisi"},
    "GuidanceLineMarking":   {"color": "#33bb88", "icon": "〰️", "label": "Yönlendirme İşareti"},
    "TaxiwayElement":        {"color": "#88aaff", "icon": "🛣️",  "label": "Taksi Yolu"},
    "TaxiHoldingPosition":   {"color": "#ff6677", "icon": "✋",  "label": "Bekleme Noktası"},
    "TaxiHoldingPositionMarking": {"color": "#ff4455", "icon": "🚫", "label": "Bekleme İşareti"},
    "ApronElement":          {"color": "#aabb55", "icon": "🅿️",  "label": "Apron"},
    "AircraftStand":         {"color": "#ccaa33", "icon": "🅿️",  "label": "Uçak Parkı"},
    "Navaid":                {"color": "#ff77ff", "icon": "📡",  "label": "Navaid"},
    "VOR":                   {"color": "#ff55cc", "icon": "📡",  "label": "VOR"},
    "NDB":                   {"color": "#cc55ff", "icon": "📡",  "label": "NDB"},
    "DME":                   {"color": "#aa55ff", "icon": "📡",  "label": "DME"},
    "TACAN":                 {"color": "#8855ff", "icon": "📡",  "label": "TACAN"},
    "Localizer":             {"color": "#ff4444", "icon": "📻",  "label": "Localizer"},
    "Glidepath":             {"color": "#ff6644", "icon": "📐",  "label": "Glidepath"},
    "MarkerBeacon":          {"color": "#ff88aa", "icon": "📻",  "label": "Marker"},
    "DesignatedPoint":       {"color": "#44ffff", "icon": "🔹",  "label": "DP"},
    "HoldingPattern":        {"color": "#44aaff", "icon": "🔄",  "label": "Bekleme Patterni"},
    "VerticalStructure":     {"color": "#ff5555", "icon": "🏗️",  "label": "Engel"},
    "RunwayDirectionLightSystem": {"color": "#ffeeaa", "icon": "💡", "label": "Işık Sistemi"},
    "RunwayMarking":         {"color": "#eeddaa", "icon": "〰️", "label": "Pist İşareti"},
    "ApproachLightingSystem":{"color": "#ffddaa", "icon": "💡",  "label": "Yaklaşma Işıkları"},
    "VisualGlideSlopeIndicator": {"color": "#ffbb77", "icon": "🔆", "label": "VGSI"},
    "AeronauticalGroundLight": {"color": "#ffff55", "icon": "💡", "label": "Saha Işığı"},
    "GeoBorder":             {"color": "#aaaaaa", "icon": "🗺️",  "label": "Coğrafi Sınır"},
    "ObstacleArea":          {"color": "#ff3333", "icon": "⚠️",  "label": "Engel Alanı"},
    "RouteSegment":          {"color": "#55aaff", "icon": "✈️",  "label": "Rota Segmenti"},
    "TouchDownLiftOff":      {"color": "#77ffaa", "icon": "🚁",  "label": "TLOF"},
}

def extract_features(xml_path):
    with open(xml_path, encoding='utf-8') as f:
        root = ET.fromstring(f.read())

    features = []

    for member in root:
        if qn(member.tag) != "message:hasMember": continue
        for feat in member:
            feat_type = qn(feat.tag).replace("aixm:", "")
            cat = CATEGORIES.get(feat_type, {"color":"#888888","icon":"❓","label": feat_type})

            # İsim / designator
            name = (_text(feat, "aixm:name") or
                    _text(feat, "aixm:designator") or
                    _text(feat, "gml:identifier") or feat_type)

            # Tüm pos ve poslist'leri topla
            points = []
            lines  = []

            for elem in feat.iter():
                t = qn(elem.tag)
                if t == "gml:pos" and elem.text:
                    c = _parse_pos(elem.text.strip())
                    if c: points.append(c)
                elif t == "gml:posList" and elem.text:
                    coords = _parse_poslist(elem.text.strip())
                    if coords: lines.append(coords)

            if not points and not lines:
                continue

            geo = None
            geom_type = "point"
            if lines:
                if len(lines) == 1:
                    geo = {"type": "LineString", "coordinates": lines[0]}
                    geom_type = "line"
                else:
                    geo = {"type": "MultiLineString", "coordinates": lines}
                    geom_type = "multiline"
            
            if geo is None and points:
                if len(points) == 1:
                    geo = {"type": "Point", "coordinates": points[0]}
                    geom_type = "point"
                else:
                    geo = {"type": "MultiPoint", "coordinates": points}
                    geom_type = "multipoint"

            features.append({
                "type": feat_type,
                "name": name[:60],
                "color": cat["color"],
                "icon":  cat["icon"],
                "label": cat["label"],
                "geom_type": geom_type,
                "geometry": geo,
            })

    return [f for f in features if f["geometry"] is not None]
