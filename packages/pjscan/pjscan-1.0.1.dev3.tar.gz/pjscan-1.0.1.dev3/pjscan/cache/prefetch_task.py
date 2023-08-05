import networkx as nx
import py2neo
from typing import List
from abc import ABC, abstractmethod
from pjscan.const import *

class AbstractPrefetchTask(ABC):
    def __init__(self,cache_graph):
        if cache_graph is None:
            raise "Task Wrong!Graph is not definited!!"
        self.cache_graph = cache_graph
    @abstractmethod
    def do_task(self):
        return None

class AstPrefetchTask(AbstractPrefetchTask):
    def __init__(self,**kwargs):
        super(AstPrefetchTask, self).__init__()
        self.node = kwargs.get("node",None)
    def do_task(self):
        self.cache_graph.add_node(self.node)
        if self.cache_graph.get_ast_inflow(self.node) is None:
            rels = self.graph.relationships.match(nodes=[None, self.node], r_type=AST_EDGE, ).all()
            self.cache_graph.add_ast_inflow(self.node, rels)
        if self.cache_graph.get_ast_outflow(self.node) is None:
            rels = self.graph.relationships.match(nodes=[self.node, None], r_type=AST_EDGE, ).all()
            self.cache_graph.add_ast_outflow(self.node, rels)

class CfgPrefetchTask(AbstractPrefetchTask):
    def __init__(self,**kwargs):
        super(CfgPrefetchTask, self).__init__()
        self.node = kwargs.get("node",None)
    def do_task(self):
        self.cache_graph.add_node(self.node)
        if self.cache_graph.get_cfg_inflow(self.node) is None:
            rels = self.graph.relationships.match(nodes=[None, self.node], r_type=CFG_EDGE, ).all()
            self.cache_graph.add_cfg_inflow(self.node, rels)
        if self.cache_graph.get_cfg_outflow(self.node) is None:
            rels = self.graph.relationships.match(nodes=[self.node, None], r_type=CFG_EDGE, ).all()
            self.cache_graph.add_cfg_outflow(self.node, rels)


class PdgPrefetchTask(AbstractPrefetchTask):
    def __init__(self,**kwargs):
        super(PdgPrefetchTask, self).__init__()
        self.node = kwargs.get("node",None)
    def do_task(self):
        if self.node[NODE_TYPE] in AST_ROOT:
            self.cache_graph.add_node(self.node)
            if self.cache_graph.get_pdg_inflow(self.node) is None:
                # TODO I NEED TO LABEL WHICH IS AST_ROOT.
                rels = self.graph.relationships.match(nodes=[None, self.node], r_type=DATA_FLOW_EDGE, ).all()
                self.cache_graph.add_pdg_inflow(self.node, rels)
            if self.cache_graph.get_pdg_outflow(self.node) is None:
                rels = self.graph.relationships.match(nodes=[self.node, None], r_type=DATA_FLOW_EDGE, ).all()
                self.cache_graph.add_pdg_outflow(self.node, rels)

class CgPrefetchTask(AbstractPrefetchTask):
    def __init__(self,**kwargs):
        super(CgPrefetchTask, self).__init__()
        self.node = kwargs.get("node",None)
    def do_task(self):
        self.cache_graph.add_node(self.node)
        if self.cache_graph.get_cg_inflow(self.node) is None:
            rels = self.graph.relationships.match(nodes=[None, self.node], r_type=CALLS_EDGE, ).all()
            self.cache_graph.add_cg_inflow(self.node, rels)
        if self.cache_graph.get_cg_outflow(self.node) is None:
            rels = self.graph.relationships.match(nodes=[self.node, None], r_type=CALLS_EDGE, ).all()
            self.cache_graph.add_cg_outflow(self.node, rels)