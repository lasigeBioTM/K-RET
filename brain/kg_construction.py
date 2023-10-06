import sys
import obonet
import rdflib
from rdflib.namespace import RDFS


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


def get_ontology_owl(ontology_url, ontology_acronym, destination_path):
    """Creates .spo files from .owl files were each line is of type <subj\tpred\tobj>

    :param ontology_url: url to .owl ontology file
    :param ontology_acronym: ontology name
    :param destination_path: where to save
    :return: .spo file were each line is of type <subj\tpred\tobj>
    """

    g = rdflib.Graph()
    g.parse(ontology_url, format='xml')
    ontology_name = rdflib.Namespace(ontology_url)
    g.bind('ontology_name', ontology_name)

    id_to_name = {s: o for s, p, o in g.triples((None, RDFS.label, None))}

    triples = []

    for s, p, o in g.triples((None, RDFS.label, None)):
        for child, key, parent in g.triples((s, None, None)):
            if parent in id_to_name and child in id_to_name and 'w3' in key:  # w3 indicates rdf relation
                if [id_to_name[child], key, id_to_name[parent]] not in triples:
                    triples.append([id_to_name[child], key.split('#')[-1], id_to_name[parent]])

    spo_file = open(destination_path + ontology_acronym + '.spo', 'w', encoding='utf-8')

    for triple in triples:
        spo_file.write(triple[0].lower().strip() + '\t' + triple[1].lower() + '\t' + triple[2].lower().strip() + '\n')

    spo_file.close()

    return


def main():
    """Usage examples:

    python3 kg_construction.py "http://purl.obolibrary.org/obo/doid.obo" None kgs/
    python3 kg_construction.py "https://data.bioontology.org/ontologies/DOID/download?apikey=8b5b7825-538d-40e0-9e9e-5ab9274a9aeb&download_format=rdf" doid kgs/
    python3 kg_construction.py "bin/medic.obo" medic kgs/

    :return:
    """

    url = sys.argv[1]
    ontology_name = sys.argv[2]
    destination = sys.argv[3]

    if url[-1] == 'o':  # for .obo
        get_ontology(url, destination)
    else:  # for .owl
        get_ontology_owl(url, ontology_name, destination)

    return


if __name__ == '__main__':
    main()


# TEST 1

# get_ontology('http://purl.obolibrary.org/obo/chebi.obo', 'kgs/')  # chemical entities of biological interest
# get_ontology('http://purl.obolibrary.org/obo/hp.obo', 'kgs/')     # human phenotypes
# get_ontology('http://purl.obolibrary.org/obo/go.obo', 'kgs/')     # gene products/ function
# get_ontology('http://purl.obolibrary.org/obo/doid.obo', 'kgs/')   # human diseases
