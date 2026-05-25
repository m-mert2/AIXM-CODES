"""
AIXM XML Generator
Senaryo ve parametrelere göre geçerli AIXM XML üretir.
"""

from datetime import datetime

GENERATOR_SCENARIOS = [
    {
        "id": "gen_airspace",
        "baslik": "Hava Sahası (Airspace)",
        "aciklama": "FIR, CTR, TMA veya kısıtlı saha tanımı",
        "icon": "✈️",
        "feature": "Airspace",
        "params": [
            {"key": "uuid",        "label": "UUID",           "type": "text",   "default": "a1b2c3d4-0000-0000-0000-000000000001"},
            {"key": "type",        "label": "Tip",            "type": "select", "options": ["FIR","CTR","TMA","R","D","P"], "default": "CTR"},
            {"key": "name",        "label": "İsim",           "type": "text",   "default": "DONLON CTR"},
            {"key": "designator",  "label": "Designatör",     "type": "text",   "default": "LDDN"},
            {"key": "lower",       "label": "Alt Sınır (ft)", "type": "number", "default": "0"},
            {"key": "upper",       "label": "Üst Sınır (ft)", "type": "number", "default": "3500"},
            {"key": "lower_ref",   "label": "Alt Referans",   "type": "select", "options": ["SFC","MSL","STD"], "default": "SFC"},
            {"key": "upper_ref",   "label": "Üst Referans",   "type": "select", "options": ["MSL","STD","SFC"], "default": "MSL"},
        ]
    },
    {
        "id": "gen_runway",
        "baslik": "Pist (Runway)",
        "aciklama": "Havalimanı pist tanımı",
        "icon": "🛬",
        "feature": "Runway",
        "params": [
            {"key": "uuid",         "label": "UUID",            "type": "text",   "default": "b1b2c3d4-0000-0000-0000-000000000002"},
            {"key": "designator",   "label": "Designatör",      "type": "text",   "default": "09L/27R"},
            {"key": "type",         "label": "Tip",             "type": "select", "options": ["RWY","FATO","STOPWAY"], "default": "RWY"},
            {"key": "length",       "label": "Uzunluk (m)",     "type": "number", "default": "3200"},
            {"key": "width",        "label": "Genişlik (m)",    "type": "number", "default": "45"},
            {"key": "surface",      "label": "Zemin",           "type": "select", "options": ["ASPH","CONC","GRASS","GRAVEL","DIRT"], "default": "ASPH"},
            {"key": "airport_href", "label": "Havalimanı Ref",  "type": "text",   "default": "donlon-airport"},
        ]
    },
    {
        "id": "gen_navaid",
        "baslik": "Seyrüsefer Yardımcısı (Navaid)",
        "aciklama": "VOR, NDB veya DME tanımı",
        "icon": "📡",
        "feature": "Navaid",
        "params": [
            {"key": "uuid",       "label": "UUID",          "type": "text",   "default": "c1b2c3d4-0000-0000-0000-000000000003"},
            {"key": "designator", "label": "Designatör",    "type": "text",   "default": "DON"},
            {"key": "name",       "label": "İsim",          "type": "text",   "default": "DONLON VOR"},
            {"key": "type",       "label": "Tip",           "type": "select", "options": ["VOR","NDB","DME","VORDME","TACAN"], "default": "VOR"},
        ]
    },
    {
        "id": "gen_localizer",
        "baslik": "Localizer (ILS)",
        "aciklama": "ILS Localizer tanımı",
        "icon": "📻",
        "feature": "Localizer",
        "params": [
            {"key": "uuid",       "label": "UUID",           "type": "text",   "default": "d1b2c3d4-0000-0000-0000-000000000004"},
            {"key": "freq",       "label": "Frekans (MHz)",  "type": "number", "default": "110.10"},
            {"key": "course",     "label": "Yön (°)",        "type": "number", "default": "091"},
            {"key": "lat",        "label": "Enlem",          "type": "number", "default": "52.3721"},
            {"key": "lon",        "label": "Boylam",         "type": "number", "default": "-31.9310"},
            {"key": "rwy_href",   "label": "Pist Ref",       "type": "text",   "default": "donlon-rwy09L"},
        ]
    },
    {
        "id": "gen_airport",
        "baslik": "Havalimanı (AirportHeliport)",
        "aciklama": "Havalimanı veya heliport tanımı",
        "icon": "🏢",
        "feature": "AirportHeliport",
        "params": [
            {"key": "uuid",       "label": "UUID",           "type": "text",   "default": "e1b2c3d4-0000-0000-0000-000000000005"},
            {"key": "designator", "label": "ICAO Kodu",      "type": "text",   "default": "EDDN"},
            {"key": "name",       "label": "İsim",           "type": "text",   "default": "DONLON INTL"},
            {"key": "type",       "label": "Tip",            "type": "select", "options": ["AD","HP","AH"], "default": "AD"},
            {"key": "lat",        "label": "Enlem",          "type": "number", "default": "52.3721"},
            {"key": "lon",        "label": "Boylam",         "type": "number", "default": "-31.9310"},
            {"key": "elev",       "label": "Yükseklik (ft)", "type": "number", "default": "308"},
        ]
    },
    {
        "id": "gen_vertical",
        "baslik": "Dikey Engel (VerticalStructure)",
        "aciklama": "Bina, kule, anten vb. engel tanımı",
        "icon": "🏗️",
        "feature": "VerticalStructure",
        "params": [
            {"key": "uuid",    "label": "UUID",           "type": "text",   "default": "f1b2c3d4-0000-0000-0000-000000000006"},
            {"key": "name",    "label": "İsim",           "type": "text",   "default": "DONLON TOWER"},
            {"key": "type",    "label": "Tip",            "type": "select", "options": ["BLDG","TOWER","CRANE","ANTENNA","CHIMNEY","WINDTURBINE"], "default": "TOWER"},
            {"key": "lighted", "label": "Işıklı",         "type": "select", "options": ["YES","NO","UNKNOWN"], "default": "YES"},
            {"key": "height",  "label": "Yükseklik (m)",  "type": "number", "default": "150"},
        ]
    },
]


def _ns():
    return '''xmlns:aixm="http://www.aixm.aero/schema/5.1.1"
  xmlns:gml="http://www.opengis.net/gml/3.2"
  xmlns:xlink="http://www.w3.org/1999/xlink"'''

def _now():
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

def _timeslice_wrap(feature, ts_content, uuid):
    ts_name = f"aixm:{feature}TimeSlice"
    return f'''  <aixm:timeSlice>
    <{ts_name} gml:id="ts-{uuid}">
      <gml:validTime/>
      <aixm:interpretation>BASELINE</aixm:interpretation>
      {ts_content}
    </{ts_name}>
  </aixm:timeSlice>'''


def generate(scenario_id, params):
    """Ana üretici fonksiyon. XML string döndürür."""
    gen = {s["id"]: s for s in GENERATOR_SCENARIOS}
    if scenario_id not in gen:
        raise ValueError(f"Bilinmeyen senaryo: {scenario_id}")

    p = params  # kısa alias
    ns = _ns()
    now = _now()

    if scenario_id == "gen_airspace":
        uuid = p.get("uuid", "airspace-001")
        ts_body = f'''<aixm:type>{p.get("type","CTR")}</aixm:type>
      <aixm:designator>{p.get("designator","LDDN")}</aixm:designator>
      <aixm:name>{p.get("name","CTR")}</aixm:name>
      <aixm:upperlimit uom="FT">{p.get("upper","3500")}</aixm:upperlimit>
      <aixm:upperLimitReference>{p.get("upper_ref","MSL")}</aixm:upperLimitReference>
      <aixm:lowerLimit uom="FT">{p.get("lower","0")}</aixm:lowerLimit>
      <aixm:lowerLimitReference>{p.get("lower_ref","SFC")}</aixm:lowerLimitReference>'''
        ts = _timeslice_wrap("Airspace", ts_body, uuid)
        return f'''<aixm:Airspace gml:id="uuid.{uuid}" {ns}>
  <gml:identifier codeSpace="urn:uuid:">{uuid}</gml:identifier>
  <gml:boundedBy/>
{ts}
</aixm:Airspace>'''

    elif scenario_id == "gen_runway":
        uuid = p.get("uuid", "runway-001")
        ts_body = f'''<aixm:designator>{p.get("designator","09L/27R")}</aixm:designator>
      <aixm:type>{p.get("type","RWY")}</aixm:type>
      <aixm:nominalLength uom="M">{p.get("length","3200")}</aixm:nominalLength>
      <aixm:nominalWidth uom="M">{p.get("width","45")}</aixm:nominalWidth>
      <aixm:surfaceProperties>
        <aixm:SurfaceCharacteristics>
          <aixm:composition>{p.get("surface","ASPH")}</aixm:composition>
        </aixm:SurfaceCharacteristics>
      </aixm:surfaceProperties>
      <aixm:associatedAirportHeliport xlink:href="{p.get("airport_href","donlon-airport")}"/>'''
        ts = _timeslice_wrap("Runway", ts_body, uuid)
        return f'''<aixm:Runway gml:id="uuid.{uuid}" {ns}>
  <gml:identifier codeSpace="urn:uuid:">{uuid}</gml:identifier>
{ts}
</aixm:Runway>'''

    elif scenario_id == "gen_navaid":
        uuid = p.get("uuid", "navaid-001")
        ts_body = f'''<aixm:designator>{p.get("designator","DON")}</aixm:designator>
      <aixm:name>{p.get("name","DONLON VOR")}</aixm:name>
      <aixm:type>{p.get("type","VOR")}</aixm:type>'''
        ts = _timeslice_wrap("Navaid", ts_body, uuid)
        return f'''<aixm:Navaid gml:id="uuid.{uuid}" {ns}>
  <gml:identifier codeSpace="urn:uuid:">{uuid}</gml:identifier>
{ts}
</aixm:Navaid>'''

    elif scenario_id == "gen_localizer":
        uuid = p.get("uuid", "loc-001")
        ts_body = f'''<aixm:frequency uom="MHZ">{p.get("freq","110.10")}</aixm:frequency>
      <aixm:course uom="DEG">{p.get("course","091")}</aixm:course>
      <aixm:location>
        <aixm:ElevatedPoint srsName="urn:ogc:def:crs:EPSG::4326">
          <gml:pos>{p.get("lat","52.3721")} {p.get("lon","-31.9310")}</gml:pos>
        </aixm:ElevatedPoint>
      </aixm:location>
      <aixm:servedRunwayDirection xlink:href="{p.get("rwy_href","donlon-rwy09L")}"/>'''
        ts = _timeslice_wrap("Localizer", ts_body, uuid)
        return f'''<aixm:Localizer gml:id="uuid.{uuid}" {ns}>
  <gml:identifier codeSpace="urn:uuid:">{uuid}</gml:identifier>
{ts}
</aixm:Localizer>'''

    elif scenario_id == "gen_airport":
        uuid = p.get("uuid", "apt-001")
        ts_body = f'''<aixm:designator>{p.get("designator","EDDN")}</aixm:designator>
      <aixm:name>{p.get("name","DONLON INTL")}</aixm:name>
      <aixm:type>{p.get("type","AD")}</aixm:type>
      <aixm:fieldElevation uom="FT">{p.get("elev","308")}</aixm:fieldElevation>
      <aixm:ARP>
        <aixm:ElevatedPoint srsName="urn:ogc:def:crs:EPSG::4326">
          <gml:pos>{p.get("lat","52.3721")} {p.get("lon","-31.9310")}</gml:pos>
        </aixm:ElevatedPoint>
      </aixm:ARP>'''
        ts = _timeslice_wrap("AirportHeliport", ts_body, uuid)
        return f'''<aixm:AirportHeliport gml:id="uuid.{uuid}" {ns}>
  <gml:identifier codeSpace="urn:uuid:">{uuid}</gml:identifier>
{ts}
</aixm:AirportHeliport>'''

    elif scenario_id == "gen_vertical":
        uuid = p.get("uuid", "vs-001")
        ts_body = f'''<aixm:name>{p.get("name","DONLON TOWER")}</aixm:name>
      <aixm:type>{p.get("type","TOWER")}</aixm:type>
      <aixm:lighted>{p.get("lighted","YES")}</aixm:lighted>
      <aixm:height uom="M">{p.get("height","150")}</aixm:height>'''
        ts = _timeslice_wrap("VerticalStructure", ts_body, uuid)
        return f'''<aixm:VerticalStructure gml:id="uuid.{uuid}" {ns}>
  <gml:identifier codeSpace="urn:uuid:">{uuid}</gml:identifier>
{ts}
</aixm:VerticalStructure>'''

    raise ValueError(f"Üretici tanımlanmamış: {scenario_id}")
