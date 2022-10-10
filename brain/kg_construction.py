import sys
import obonet


def get_ontology(ontology_url, destination_path):
    """Creates .spo files from .obo files were each line is of type <subj\tpred\tobj>

    :param ontology_url: url to .obo ontology file
    :param destination_path: where to save
    :return: .spo file were each line is of type <subj\tpred\tobj>
    """

    ontology = ontology_url.split('/')[-1].split('.')[0]
    spo_file = open(destination_path + ontology + '.spo', 'w', encoding='utf-8')

    graph = obonet.read_obo(ontology_url)

    # Number of nodes, edges
    # print(len(graph), graph.number_of_edges())

    id_to_name = {id_: data.get('name') for id_, data in graph.nodes(data=True)}

    triples = []

    for id_, data in graph.nodes(data=True):

        for child, parent, key in graph.out_edges(id_, keys=True):
            if [id_to_name[child], key, id_to_name[parent]] not in triples:
                triples.append([id_to_name[child], key, id_to_name[parent]])

        for parent, child, key in graph.in_edges(id_, keys=True):
            if [id_to_name[parent], key, id_to_name[child]] not in triples:
                triples.append([id_to_name[parent], key, id_to_name[child]])

    for triple in triples:
        spo_file.write(triple[0].lower() + '\t' + triple[1].lower() + '\t' + triple[2].lower() + '\n')

    spo_file.close()

    return


# TEST

# get_ontology('http://purl.obolibrary.org/obo/chebi.obo', 'kgs/')  # chemical entities of biological interest
# get_ontology('http://purl.obolibrary.org/obo/hp.obo', 'kgs/')     # human phenotypes
# get_ontology('http://purl.obolibrary.org/obo/go.obo', 'kgs/')     # gene products/ function
# get_ontology('http://purl.obolibrary.org/obo/doid.obo', 'kgs/')   # human diseases


def main():
    """Usage example: python3 kg_construction.py http://purl.obolibrary.org/obo/doid.obo kgs/

    :return:
    """

    url = sys.argv[1]
    destination = sys.argv[2]

    get_ontology(url, destination)

    return


if __name__ == '__main__':
    main()
