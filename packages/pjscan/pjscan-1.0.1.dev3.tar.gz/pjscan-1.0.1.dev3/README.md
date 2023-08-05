# EnhancedPHPJoern Framework 

[![Documentation Status](https://readthedocs.com/projects/shaobaobaoer-enhanced-phpjoern-framework/badge/?version=latest&token=97bbf5e5fa066e2a191c91f88479cba63f0ea8a85e9bdbe57a58c0332ae52778)](https://shaobaobaoer-enhanced-phpjoern-framework.readthedocs-hosted.com/en/latest/?badge=latest)

## Introduction

This framework helps you discover security vulnerabilities by executing graph traversals on the Code Property Graph. 

## Installation

### install from pip (not public yet)

```Bash
pip3 install enhanced-phpjoern-framework
```


### install from source code

```Bash
git clone 
python setup.py install
```


## Usage

> For more usage information , you can visit the document page for the Enhanced PHPJoern Framework (TODO, NOT PUBLISHED YET)


#### AST APIs

**general apis**

- get_node_itself
- get_ast_ith_child_node
- find_ast_child_nodes
- find_ast_parent_nodes

**call node apis** 

> The given node should be a function\method call with AST node type AST_CALL \ AST_DYNAMIC_CALL \ AST_STATIC_CALL \ AST_NEW


- find_ast_funtion_args
- get_ast_ith_function_arg
- get_ast_function_arg_cnt
- ...

**callable node apis**

> The given node should be a function\method callable with AST node type AST_METHOD \ AST_FUNC_DECL


- get_ast_method_name
- get_ast_method_range
- ...

**conditional node apis**

> The given node should be conditional statements node with AST node type AST_IF \ AST_SWITCH \ AST_FOR \ AST_FOREACH \ AST_WHILE \ AST_DO_WHILE


- get_ast_condition_range
- get_ast_condition_nodes
- ...
- get_ast_root_node
- filter_ast_child_nodes
- get_ast_node_code
	Get the code of the current ast node. Note that this API will traversal the node's AST child node so as to get the full code for given node. This APIis a light but different implementation compared with `Symbolic Tracking Module`



### **CFG A**PIs

- get_cfg_predecessors
- get_cfg_successors
- get_cfg_flow_label
- find_cfg_all_predecessors
	Like the api in joern named  `dominated`
- find_cfg_all_successors
	Like the api in joern named  `dominatedBy`

### **PDG APIs**

- find_pdg_def_nodes
- find_pdg_use_nodes
- get_pdg_vars
- find_pdg_origination_nodes
	For given AST node , find all DEFINE nodes that obtain direct or indirect data-flow relationship to the node
- find_pdg_direction_nodes
	For given AST node ,find all USE nodes that obtain direct or indirect data-flow relationship to the node

### **CG **APIs

- find_cg_decl_nodes
- find_cg_call_nodes
- get_cg_caller
- find_cg_callees
	Return all calls in a given callable node. 
- find_cg_callins
	Return the call chains after a given call node. Note that to avoid path explosions. You should set up the depth or file filter for this function. 
- find_cg_incalls
	Return the call chains before a given call node. Note that to avoid path explosions. You should set up the depth or file filter for this function.

### **FIG **APIs

- get_fig_node_belong_file_name
- get_fig_file_name_belong_node
- find_fig_include_files
- get_fig_include_map

### **CHG **APIs

- find_chg_parent_class_nodes
- find_chg_child_class_nodes
- get_chg_parent_family
- get_chg_child_family



### Traversal Graph 

We provide an abstract class named GraphTraversal which used to traversal graph with user-defined rules.



#### How Graph Traversal Work?

The source or sink can be a List of filters or a List of nodes.

For initial , we get these nodes as origin or terminal.

- For each origin \ terminal pair , we firstly filter their reachability. 
- After that , we will traverse the orgin to reach the terminal.
	- The traverse step is an simple BFS step ,which means it will generate several `candidate` node.
	- The sanitizer step is a list of functions, which means it will filter these candidates.
- Finally , we will report these flows.



#### GraphTraversal

Referred from CodeQL implementation, we perform a GraphTraversal Class to support intraprocedural analysis.



The abstract class may set as follows.

```Python
class BaseGraphTraversal(object):      
    def __init__(self, neo4j_engine: Neo4jEngine,
                 origin: List[Node] = None,
                 terminal: List[Callable] = None,
                 sanitizer: List[Callable] = None,
                 recorder: Callable = None):
    @abstractmethod
    def traversal(self, current_node, *args, **kwargs):
        return self.neo4j_engine.find_cfg_successors(current_node)

class BaseRecorder(object):
    @abstractmethod
    def record(self, node: py2neo.Node, next_node: py2neo.Node) -> bool:
        return True

```


- origin :  The origin of graph traversal.
- terminal : The terminal of graph traversal.
- sanitizer : The sanitizer of graph traversal.
- recorder : The result recorder of graph traversal.
- traversal : traverse the graph



The process of graph traversal can be summarize as follows : 

```Perl
Input : origin,terminal_rule,sanitizer_rule,traversal_rule
Output : recorder

Queue = [origin]
while !Queue.empty()
  current = Queue.pop()
  candidate_next_nodes = traversal(current)
  next_nodes = ~isSanitized(candidate_next_nodes)
  recorder.result <-- isTerminal(next_nodes)
  recorder.flow <-- record(current_node,next_nodes)

```






## Changelog

See `[CHANGES.md](https://github.com/ninthDevilHAUNSTER/enhanced-phpjoern-framework/blob/master/CHANGES.md)`

## Authors

See `[AUTHORS.md](https://github.com/ninthDevilHAUNSTER/enhanced-phpjoern-framework/blob/master/AUTHORS.md)`

## License

See `[LICENSE.txt](https://github.com/ninthDevilHAUNSTER/enhanced-phpjoern-framework/blob/master/LICENSE.txt)`



