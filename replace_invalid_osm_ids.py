import argparse
from xml.dom.minidom import parseString


def replace_invalid_osm_ids(in_file, out_file):
    with open(in_file, 'r') as file:
        file_content = file.read()

    dom = parseString(file_content)

    nodes = dom.getElementsByTagName("node")
    ways = dom.getElementsByTagName("way")
    relations = dom.getElementsByTagName("relation")

    nodes_id_map = update_ids(nodes)
    ways_id_map = update_ids(ways)
    _ = update_ids(relations)

    update_node_refs_in_ways(ways, nodes_id_map)
    update_member_refs_in_relations(relations, nodes_id_map, ways_id_map)

    with open(out_file, 'w') as file:
        dom.writexml(file)


def update_ids(element_list):
    ids = [element.getAttribute("id") for element in element_list]
    id_map = get_id_map(ids)
    for element in element_list:
        update_element_id(element, id_map)
    return id_map


def get_id_map(ids):
    """
    Returns a dict with
    invalid ids as keys +
    a valid replacement as value"""
    valid_ids = [int(i) for i in ids if int(i) >= 1]
    invalid_ids = [int(i) for i in ids if int(i) < 1]

    new_id = 1
    id_map = {}

    for invalid_id in invalid_ids:
        while new_id in valid_ids:
            new_id += 1
        id_map[invalid_id] = new_id
        valid_ids.append(new_id)

    return id_map


def update_element_id(element, id_map, attr="id"):
    id = int(element.getAttribute(attr))
    if id_map.get(id) is not None:
        element.setAttribute(attr, str(id_map.get(id)))


def update_node_refs_in_ways(way_elements, nodes_id_map):
    for way in way_elements:
        ref_nodes = way.getElementsByTagName("nd")
        for ref_node in ref_nodes:
            update_element_id(ref_node, nodes_id_map, "ref")


def update_member_refs_in_relations(relation_elements,
                                    nodes_id_map,
                                    ways_id_map):
    for relation in relation_elements:
        members = relation.getElementsByTagName("member")
        for member in members:
            type = member.getAttribute("type")
            if type == "node":
                update_element_id(member, nodes_id_map, "ref")
            elif type == "way":
                update_element_id(member, ways_id_map, "ref")


parser = argparse.ArgumentParser(prog="Replace Invalid OSM Ids")
parser.add_argument("in_file", help="The OSM file with invalid Ids")
parser.add_argument("out_file", help="The OSM file with valid Ids",
                    nargs='?', default="valid.osm")


if __name__ == "__main__":
    args = parser.parse_args()
    replace_invalid_osm_ids(args.in_file, args.out_file)
