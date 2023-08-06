import yaml
import sys
from pyperseo.functions import milisec

class EMB():
    def __init__(self, config, prefixes, triplets):
        self.config = config
        self.prefixes = prefixes
        self.triplets = triplets

    def transform_YARRRML(self):
        self.main_dict = dict()
        self.reg = dict()
        self.tree = dict()


        # prefixes object:
        if self.config["configuration"] == "ejp":
            prefixes_dict = dict(prefixes=self.prefixes) # create prefixes object
            prefixes_dict["prefixes"]["this"] = str("|||BASE|||")
            self.main_dict.update(prefixes_dict) # append prefixes object into main
        elif self.config["configuration"] == "csv":
            prefixes_dict = dict(prefixes=self.prefixes) # create prefixes object
            self.main_dict.update(prefixes_dict) # append prefixes object into main
        else:
            sys.exit('You must provide a configuration parameter: use "ejp" for using this template for EJP-RDs workflow, or "csv" for defining CSV data source')


        # sources object:
        if self.config["configuration"] == "ejp":
            sources_dict = dict(sources= dict(
                                    source_prov=dict(
                                    access = str("|||DATA|||"),
                                    referenceFormulation= str("|||FORMULATION|||"),
                                    iterator = str("$"))))
            sources_dict["sources"][self.config["source_name"]] = sources_dict["sources"].pop("source_prov") # rename source_name using an unique name from config
            self.main_dict.update(sources_dict)
        elif self.config["configuration"] == "csv":
            if "csv_name" in self.config:
                sources_dict = dict(sources= dict(
                                    source_prov=dict(
                                        access = self.config["csv_name"]+ ".csv",
                                        referenceFormulation= "csv",
                                        iterator = str("$"))))
                sources_dict["sources"][self.config["source_name"]] = sources_dict["sources"].pop("source_prov") # rename source_name using an unique name from config
                self.main_dict.update(sources_dict)
            else:
                sys.exit('You must provide a csv_name parameter for defining the name of your CSV data source')

        else:
            sys.exit('You must provide a configuration parameter: use "ejp" for using this template for EJP-RDs workflow, or "csv" for defining CSV data source')

        # mapping object:

        
        mapping_dict = dict(mapping = dict())

        for e in self.triplets:
            if not e[0] in self.reg.keys():
                triplet_map = dict(name_node = dict(
                                        sources = [self.config["source_name"]], # SOURCE
                                        subjects = e[0], # SUBJECT
                                        predicateobject = [dict(
                                            predicate = e[1], # PREDICATE
                                            objects = dict(
                                                value = e[2], # OBJECT
                                                datatype = e[3]))]))  # DATATYPE

                stamp = milisec() + "_" + self.config["source_name"] # Creating a unique name for each object using timestamp and source_name 
                if e[3] == "iri":
                    triplet_map["name_node"]["predicateobject"][0]["objects"]["type"] = triplet_map["name_node"]["predicateobject"][0]["objects"].pop("datatype") # rename name_mode using an unique name per node
                triplet_map[stamp] = triplet_map.pop("name_node") # rename name_mode using an unique name per node
                mapping_dict["mapping"].update(triplet_map) # append dict into dict
                self.reg.update( {e[0] : stamp } )
            else:
                for k, v in self.reg.items():
                    if k == e[0]:
                        predicate_map = dict(
                                        predicate = e[1], # PREDICATE
                                        objects = dict(
                                            value = e[2], # OBJECT
                                            datatype = e[3])) # DATATYPE

                        if e[3] == "iri":
                            predicate_map["objects"]["type"] = predicate_map["objects"].pop("datatype") # rename name_mode using an unique name per node

                        mapping_dict["mapping"][v]["predicateobject"].append(predicate_map)

        self.main_dict.update(mapping_dict) # append mapping object into main

        # dump
        document = yaml.dump(self.main_dict)
        return document


    def transform_ShEx(self, basicURI):
        self.prefix_all = ""
        self.list = list()
        self.tree = dict()
        self.final = ""

        # Prefixes:
        prefix_all = ""
        for k,v in self.prefixes.items():
            prefix = "PREFIX " + k + ": <" + v + ">"
            prefix_all = prefix_all + prefix + "\n"

        # Triplets
        for quad in self.triplets:
            s,p,o,d = quad
            if s.startswith(basicURI + ":" ):
                c_element = s[::-1].split("_")[0]
                c_element = c_element[::-1]
                s_curated = c_element.lower() + "Shape"
            elif s.startswith("http"):
                s_curated = "<" + s + ">"
            else:
                s_curated = s

            if p == "rdf:type":
                p_curated = "a"
            else:
                p_curated = p

            if not str(d) == "iri":
                o_curated = d
            else:
                if o.startswith(basicURI + ":" ):
                    c_element = o[::-1].split("_")[0]
                    c_element = c_element[::-1]
                    o_curated = "@:" + c_element.lower() + "Shape"
                elif "$(" in o and d == "iri":
                    o_curated = "IRI"
                elif o.startswith("http"):
                    o_curated = "IRI"
                else:
                    o_curated = o
            
            triplet = [s_curated,p_curated,o_curated]
            self.list.append(triplet)

        for tri in self.list:
            s, p, o = tri
            if not s in self.tree.keys():
                map = dict()
                map.update({s:{p:o}}) 
                self.tree.update(map)
            else:
                po = {p:o} 
                self.tree[s].update(po)

        for s in self.tree:
            subj= "\n" + s + " IRI {"
            self.final = self.final + subj
            for p,o in self.tree[s].items():
                if o.startswith("@") or o.startswith("xsd"):
                    pred_obj = "\n" + "\t" + p + " " + o + " ;"
                elif o == "IRI":
                    pred_obj = "\n" + "\t" + p + " " + o + " ;"
                else:
                    pred_obj = "\n" + "\t" + p + " [" + o + "]" + " ;"
                self.final = self.final + pred_obj
            self.final = self.final[:-1]
            end = "\n" + "} ;" + "\n"
            self.final = self.final + end
        return self.final