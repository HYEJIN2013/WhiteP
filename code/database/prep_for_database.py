if element.tag == 'node':
        for field in node_attr_fields:
            node_attribs[field] = element.attrib[field]

        for child in element:
            key = child.attrib['k']
            if problem_chars.search(key):
                continue
            node_tags = {}
            node_tags['id'] = element.attrib['id']
            node_tags['value'] = child.attrib['v']
            if LOWER_COLON.search(key):
                c = key.find(':')
                node_tags['key'] = key[c+1:]
                node_tags['type'] = key[:c+1]
                tags.append(node_tags)
                continue
            else:
                node_tags['key'] = key
                node_tags['type'] = default_tag_type
                tags.append(node_tags)
                continue

        return {'node': node_attribs, 'node_tags': tags}

    elif element.tag == 'way':
        for field in way_attr_fields:
            way_attribs[field] = element.attrib[field]
        for child in enumerate(element):
            elem = child[1]
            if node.tag == 'nd':
                nd = {}
                nd['id'] = element.attrib['id']
                nd['position'] = child[0]
                nd['node_id'] = elem.attrib['ref']
                way_nodes.append(nd)
            if node.tag == 'tag':
                key = child[1].attrib['k']
                if problem_chars.search(key):
                    continue
                way_tags = {}
                way_tags['id'] = element.attrib['id']
                way_tags['value'] = child[1].attrib['v']
                c = key.find(':')
                if LOWER_COLON.search(key):
                    way_tags['key'] = key[c+1:]
                    way_tags['type'] = key[:c+1]
                    tags.append(way_tags)
                    continue
                else:
                    way_tags['key'] = key
                    way_tags['type'] = default_tag_type
                    tags.append(way_tags)

        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}
