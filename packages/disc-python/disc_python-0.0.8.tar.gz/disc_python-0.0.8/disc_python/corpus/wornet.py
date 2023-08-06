import sys
import networkx as nx
from nltk.corpus import wordnet as wn


class WordNet():
    """
    Clase para el corpus WordNet

    Contienen toda la logica para acceder a los synsets de WordNet

    Los metodos 'publicos' de la clase retornan siempre un grafo NetworkX
    para su manipulacion.

    Cada vertice en el grafo es un lemma_names() y cada arista es el tipo de relacion
    que los une.
    """

    def __init__(self):
        self.use_type = {
            "HYPERNYMS": True, "HYPONYMS": True,"INSTANCE_HYPERNYMS": True,
            "INSTANCE_HYPONYMS": True, "MEMBER_HOLONYMS": True,
            "MEMBER_MERONYMS": True, "PART_HOLONYMS": True, "PART_MERONYMS": True
        }

    def _get_synsets(self, word):
        """Obtiene todos los synsets relacionados con un terminos

        Parameters
        ----------
        word : string
            El termino al que le desea buscar sus synsets

        Returns
        -------
        synsets : list
            Una lista con todos los synsets
        """
        synsets = wn.synsets(word)
        return synsets

    def _get_relations(self, word):
        """Obtiene en un diccionario los terminos relacionados con un termino de entrada.
        Cada termino relacionado pertenece a un tipo de relacion descrita por una de
        las llaves del diccionario de retorno.

        Parameters
        ----------
        word : string
            El termino al que se le desea obtner sus relaciones

        Returns
        -------
        relaciones : dict
            Un diccionario que contiene todos los terminos relacionados a un termino
            separados por el tipo de relacion.

        Notes
        -----
        Los tipos de relaciones incluidas en el diccionario de salida son todos aquellos
        que se encuentran con la bandera True en el atributo de clase use_type
        """
        realaciones = {}
        synsets = self._get_synsets(word)
        for k,v in self.use_type.items():
            if(v):
                realaciones[k] = []
                for synset in synsets:
                    if(synset.pos() == wn.NOUN):
                        for tss in getattr(synset, k.casefold())():
                            lemmas_name = tss.lemma_names()
                            realaciones[k] = realaciones[k] + lemmas_name
        return realaciones

    def get_relations_like_graph(self, word):
        """Retorna las relaciones de un termino a manera de grafo

        Parameters
        ----------
        word : str
            Termino de entrada

        Returns
        -------
        graph : NetworkX graph
            Grafo con las relaciones de un termino. Cada vertice del grafo
            es un termino
        """
        relaciones = self._get_relations(word)
        graph = nx.DiGraph()
        if relaciones == {}:
            print("La palabra {} No existe en el Corpus".format(word))
            return graph
        for k,v in relaciones.items():
            for r in v:
                if graph.has_node(r) == False:
                    graph.add_edge(word, r, tipo=k)
        return graph

    def to_graph_from_list_words(self, words):
        """Intenta retornar un grafo conectado que contenga las palabras
        que se le pasen como parametro.

        Parameters
        ----------
        words : list
            Lista de terminos

        Returns
        -------
        graph : NetworkX graph
            Grafo que contiene los terminos relacionados con cada termino en la lista de entrada.

        Notes
        -----
        El grafo de retorno es conectado siempre y cuando la profundidad de la busqueda
        logre conectar en algun momento todos los terminos.

        See Also
        --------
        _to_graph
        """
        g = nx.DiGraph()
        for w in words:
            self._to_graph(g,None,w,None)
        return g

    def _to_graph(self, graph, from_word, to_word, type_relation, depth=1, max_depth=2):
        """Funcion recursiva que busca concetar dos terminos mediante sus relaciones

        Parameters
        ----------
        graph : NetworkX graph
            Grafo de entrada. Puede ser un grafo vacio o que ya contenga datos

        from_word : string
            Primer termino que se busca conectar con el segundo termino (to_word).
            Si se le proporciona como entrada el valor de None significa que no se
            intentara concetar dos terminos y solo se buscaran las relaciones del
            segundo termino.

        to_word : string
            Termino con el que se busca conectar el primer termino

        type_relation : string
            Tipo de relacion. Este parametro se utiliza en la funcion recursiva por lo cual
            no se debe proporcionar cuando se llame la funcion en primera instancia.

        depth : int, optional (default = 1)
            Profundidad a la que se encuentra la busqueda. Tener en cuenta que si se modifica
            el default se debe asegurar que max_depth tambien se modifique para que se cumpla depth <= max_depth

        max_depth : int, optional (default = 2)
            Profundidad maxima a la que se desea buscar las relaciones de los terminos

        Returns
        -------
        graph : NetworkX graph
            Grafo con todos los terminos relacionados

        Notes
        -----
        Que se conecten los terminos de entrada en un grafo depende de la profundidad
        maxima a la que se desea buscar, si en el nivel maximo de profundidad no encuentra el
        termino destino, entonces no se logro conctar los terminos. Cada nivel de profundidad
        son las relaciones conectadas a un termino. Ejemplo:

                O
               / \   <-- profundidad 1
               1  2
              / \ /\ <-- profundidad 2
                 .
                 .
                 .

        """
        to_exist = graph.has_node(to_word)
        if from_word is not None:
            graph.add_edge(from_word, to_word, tipo=type_relation)
        if depth <= max_depth and not to_exist:
            relaciones = self._get_relations(to_word)
            for k,v in relaciones.items():
                for element in v:
                    self._to_graph(graph, to_word, element, k, depth+1, max_depth)
        return graph

    def to_graph_connect_words(self, source, target, inter_word=None, max_depth=50):
        """Intenta retornar un grafo que conecta dos terminos,
        pasando por un termino intermedio, a traves de una busqueda en profundidad

        Parameters
        ----------
        source : str
            Termino fuente, donde se iniciara la busqueda

        target: str
            Termino destino, donde se intentara terminar la busqueda

        inter_word : str
            Termino intermedio, el termino que por el cual debe pasar la busqueda. Si no se
            proporciona ninguna palabra intermedia, entonces solo se intenta conectar el source
            con el target

        max_depth: int
            Profundidad maxima a la que se desea buscar las relaciones de los terminos

        Returns
        -------
        graph : NetworkX graph
            Grafo

        Notes
        -----
        El mecanismo logico detras de la funcion es concetar primero source con inter_word
        y despues target con inter_word, así source y target estaran concetados. Depende de la
        profundidad maxima de busqueda.

        See Also
        --------
        _dfs
        """
        graph = nx.DiGraph()
        if inter_word:
            self._dfs(graph, source, inter_word, max_depth=max_depth)
            self._dfs(graph, target, inter_word, max_depth=max_depth)
        else:
            self._dfs(graph, source, target, max_depth=max_depth)
        return graph
        #return self._dfs(graph, source, inter_word)

    def _dfs(self, graph, source, target, depth=1, max_depth=20):
        """Usa el algoritmo DFS para conectar dos terminos

        Parameters
        ----------
        graph : NetworkX graph
            Grafo

        source : str
            Termino fuente, de donde comenzara la busqueda

        target : str
            Termino destino, donde terminara la busqueda

        depth : int, optional (default = 1)
            Profundidad a la que se encuentra la busqueda. Tener en cuenta que si se modifica
            el default se debe asegurar que max_depth tambien se modifique para que se cumpla depth <= max_depth

        max_depth : int, optional (default = 20)
            Profundidad maxima a la que se desea buscar las relaciones de los terminos

        Notes
        -----
        Que se conecten los terminos de entrada en un grafo depende de la profundidad
        maxima a la que se desea buscar, si en el nivel maximo de profundidad no encuentra el
        termino destino, entonces no se logro conctar los terminos. Cada nivel de profundidad
        son las relaciones conectadas a un termino. Ejemplo:

                O
               / \   <-- profundidad 1
               1  2
              / \ /\ <-- profundidad 2
                 .
                 .
                 .
        """
        relaciones = self._get_relations(source)
        if relaciones == {}:
            print("La palabra {} No existe en el Corpus".format(source))
            return graph
        if depth > max_depth:
            return graph
        for k,v in relaciones.items():
            if target in v:
                graph.add_edge(source, target, tipo=k)
                print("Palabra encontrada")
                return graph
            #Buesqueda en profundidad del nodo target
            for element in v:
                if graph.has_node(element):
                    graph.add_edge(source, element, tipo=k)
                else:
                    graph.add_edge(source, element, tipo=k)
                    self._dfs(graph, element, target, depth=depth+1, max_depth=max_depth)
        return graph