import xml.etree.ElementTree as ET
from collections import defaultdict, Counter
from pathlib import Path
import re
import csv


XML_FILE = "Donlon.xml"
OUT_DIR = Path("cfg_output")
OUT_DIR.mkdir(exist_ok=True)


NS_PREFIX = {
    "http://www.aixm.aero/schema/5.1.1": "aixm",
    "http://www.aixm.aero/schema/5.1.1/message": "message",
    "http://www.opengis.net/gml/3.2": "gml",
    "http://www.w3.org/1999/xlink": "xlink",
    "http://www.w3.org/2001/XMLSchema-instance": "xsi",
    "http://www.isotc211.org/2005/gmd": "gmd",
    "http://www.isotc211.org/2005/gco": "gco",
}


def split_tag(tag):
    """
    XML tagını namespace ve local name olarak ayırır.
    Örnek:
    {http://www.aixm.aero/schema/5.1.1}Airspace
    ->
    aixm, Airspace
    """
    if not isinstance(tag, str):
        return "", ""

    if tag.startswith("{"):
        uri, local = tag[1:].split("}", 1)
        prefix = NS_PREFIX.get(uri, "ns")
        return prefix, local

    return "", tag


def qname(elem):
    """
    Element adını prefix:localName formatına çevirir.
    """
    prefix, local = split_tag(elem.tag)
    if prefix:
        return f"{prefix}:{local}"
    return local


def local_name(elem):
    return split_tag(elem.tag)[1]


def nonterminal(name):
    """
    CFG non-terminal adı üretir.
    aixm:Airspace -> <aixm_Airspace>
    """
    clean = name.replace(":", "_").replace("-", "_")
    return f"<{clean}>"


def literal_start(elem):
    """
    CFG içinde başlangıç tagını temsil eder.
    Attribute detayını basitleştiriyoruz.
    """
    return f'"<{qname(elem)}>"'


def literal_end(elem):
    return f'"</{qname(elem)}>"'


def get_children(elem):
    return [child for child in elem if isinstance(child.tag, str)]


def text_value(elem):
    if elem.text is None:
        return ""
    return elem.text.strip()


def is_has_member(elem):
    return qname(elem) == "message:hasMember"


def is_aixm(elem):
    prefix, _ = split_tag(elem.tag)
    return prefix == "aixm"


def get_top_level_features(root):
    """
    message:hasMember altındaki AIXM featureları çıkarır.
    """
    features = []

    for child in get_children(root):
        if is_has_member(child):
            member_children = get_children(child)

            for item in member_children:
                if is_aixm(item):
                    features.append(item)
                    break

    return features


def find_timeslices(feature):
    """
    Bir feature içindeki aixm:timeSlice bloklarını bulur.
    """
    result = []

    for child in get_children(feature):
        if qname(child) == "aixm:timeSlice":
            ts_children = get_children(child)
            if ts_children:
                result.append(ts_children[0])

    return result


def sequence_of_children(elem):
    """
    Bir elementin direkt çocuklarının tag sırasını verir.
    """
    return [qname(child) for child in get_children(elem)]


def make_rule(lhs, rhs):
    if not rhs:
        return f"{lhs} -> ε"
    return f"{lhs} -> {' '.join(rhs)}"


def make_alternative_rule(lhs, alternatives):
    lines = []
    alternatives = sorted(alternatives)

    for i, alt in enumerate(alternatives):
        if not alt:
            rhs = "ε"
        else:
            rhs = " ".join(alt)

        if i == 0:
            lines.append(f"{lhs} -> {rhs}")
        else:
            lines.append(f"{' ' * len(lhs)} | {rhs}")

    return "\n".join(lines)


def collect_leaf_values(elements):
    """
    Leaf elementlerin text değerlerini toplar.
    Örnek:
    aixm:type -> FIR | CTR | TMA
    """
    values = defaultdict(set)

    def visit(elem):
        children = get_children(elem)

        if not children:
            val = text_value(elem)
            if val:
                values[qname(elem)].add(val)
            return

        for child in children:
            visit(child)

    for elem in elements:
        visit(elem)

    return values


def value_to_token(value):
    """
    CFG değerlerini güvenli hale getirir.
    """
    value = value.replace('"', "'")
    return f'"{value}"'


def guess_value_rule(tag_name, values):
    """
    Bazı terminal değerleri için otomatik kural üretir.
    Çok fazla değer varsa genel tip kullanır.
    """
    vals = sorted(values)

    if len(vals) == 0:
        return None

    if len(vals) <= 20:
        rhs = " | ".join(value_to_token(v) for v in vals)
        return f"{nonterminal(tag_name + '_Value')} -> {rhs}"

    # Çok fazla farklı değer varsa tipe göre genelleştir
    if all(re.fullmatch(r"-?\d+", v) for v in vals):
        return f"{nonterminal(tag_name + '_Value')} -> <Integer>"

    if all(re.fullmatch(r"-?\d+(\.\d+)?", v) for v in vals):
        return f"{nonterminal(tag_name + '_Value')} -> <Decimal>"

    if all(re.fullmatch(r"[A-Z]{4}", v) for v in vals):
        return f"{nonterminal(tag_name + '_Value')} -> <ICAOCode>"

    return f"{nonterminal(tag_name + '_Value')} -> <Text>"


def generate_feature_cfg(features):
    """
    Fotodaki gibi feature bazlı CFG üretir.
    """
    by_feature = defaultdict(list)

    for feature in features:
        by_feature[qname(feature)].append(feature)

    output = []

    for feature_name in sorted(by_feature.keys()):
        feature_list = by_feature[feature_name]
        feature_local = feature_name.split(":")[-1]

        output.append(f"G_{feature_local}:")
        output.append("")

        feature_nt = nonterminal(feature_name)
        body_nt = nonterminal(feature_local + "_Body")
        timeslice_list_nt = nonterminal(feature_local + "_TimeSliceList")
        timeslice_block_nt = nonterminal(feature_local + "_TimeSliceBlock")

        output.append(f"  S -> {feature_nt}")
        output.append(
            f"  {feature_nt} -> \"<{feature_name}>\" {body_nt} \"</{feature_name}>\""
        )

        # Feature gövdesindeki direkt çocuk sıraları
        body_sequences = set()

        for feature in feature_list:
            seq = tuple(nonterminal(qname(child)) for child in get_children(feature))
            body_sequences.add(seq)

        output.append("  " + make_alternative_rule(body_nt, body_sequences).replace("\n", "\n  "))

        # TimeSlice yapıları
        timeslices = []

        for feature in feature_list:
            timeslices.extend(find_timeslices(feature))

        if timeslices:
            ts_names = sorted(set(qname(ts) for ts in timeslices))

            output.append("")
            output.append(f"  {timeslice_list_nt} -> {timeslice_block_nt} {timeslice_list_nt}")
            output.append(f"  {timeslice_list_nt} -> ε")

            for ts_name in ts_names:
                ts_local = ts_name.split(":")[-1]
                ts_nt = nonterminal(ts_name)
                ts_body_nt = nonterminal(ts_local + "_Body")

                output.append("")
                output.append(
                    f"  {timeslice_block_nt} -> \"<aixm:timeSlice>\" {ts_nt} \"</aixm:timeSlice>\""
                )
                output.append(
                    f"  {ts_nt} -> \"<{ts_name}>\" {ts_body_nt} \"</{ts_name}>\""
                )

                ts_sequences = set()

                for ts in timeslices:
                    if qname(ts) == ts_name:
                        seq = tuple(nonterminal(qname(child)) for child in get_children(ts))
                        ts_sequences.add(seq)

                output.append("  " + make_alternative_rule(ts_body_nt, ts_sequences).replace("\n", "\n  "))

        # Leaf değer kuralları
        leaf_values = collect_leaf_values(feature_list)

        value_rules = []

        for tag, values in sorted(leaf_values.items()):
            rule = guess_value_rule(tag, values)
            if rule:
                value_rules.append(rule)

        if value_rules:
            output.append("")
            output.append("  # Terminal value rules")
            for rule in value_rules:
                output.append("  " + rule)

        output.append("")
        output.append("-" * 80)
        output.append("")

    return "\n".join(output)


def generate_recursive_cfg(root):
    """
    XML'deki bütün taglar için gözlenen çocuk dizilerine göre CFG üretir.
    Bu daha detaylı ama daha uzun çıktı verir.
    """
    productions = defaultdict(set)

    def visit(elem):
        name = qname(elem)
        lhs = nonterminal(name)

        children = get_children(elem)

        if children:
            rhs = tuple(nonterminal(qname(child)) for child in children)
            productions[lhs].add(rhs)

            for child in children:
                visit(child)
        else:
            txt = text_value(elem)

            if txt:
                productions[lhs].add(("<Text>",))
            else:
                productions[lhs].add(("ε",))

    visit(root)

    lines = []
    lines.append("G_FULL_XML:")
    lines.append("")
    lines.append(f"S -> {nonterminal(qname(root))}")
    lines.append("")

    for lhs in sorted(productions.keys()):
        alternatives = productions[lhs]
        lines.append(make_alternative_rule(lhs, alternatives))
        lines.append("")

    lines.append("<Text> -> string")
    lines.append("<Integer> -> digit+")
    lines.append("<Decimal> -> digit+ '.' digit+")
    lines.append("<ICAOCode> -> [A-Z][A-Z][A-Z][A-Z]")

    return "\n".join(lines)


def write_feature_counts(features):
    counter = Counter(qname(feature) for feature in features)

    out_file = OUT_DIR / "feature_counts.csv"

    with out_file.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Feature", "Count"])

        for feature, count in sorted(counter.items()):
            writer.writerow([feature, count])


def main():
    tree = ET.parse(XML_FILE)
    root = tree.getroot()

    features = get_top_level_features(root)

    print(f"Top-level feature instance count: {len(features)}")
    print(f"Different feature type count: {len(set(qname(f) for f in features))}")

    write_feature_counts(features)

    feature_cfg = generate_feature_cfg(features)
    recursive_cfg = generate_recursive_cfg(root)

    (OUT_DIR / "cfg_by_feature.txt").write_text(feature_cfg, encoding="utf-8")
    (OUT_DIR / "full_recursive_cfg.txt").write_text(recursive_cfg, encoding="utf-8")

    print("Generated:")
    print(f"- {OUT_DIR / 'feature_counts.csv'}")
    print(f"- {OUT_DIR / 'cfg_by_feature.txt'}")
    print(f"- {OUT_DIR / 'full_recursive_cfg.txt'}")


if __name__ == "__main__":
    main()