import pathlib
from import_deps import ModuleSet
from agent.agent_utils import get_target_edit_files
from pathlib import Path
from graphlib import TopologicalSorter, CycleError

from datasets import load_dataset

datasets = load_dataset("wentingzhao/commit0_combined", split="test")
a = datasets[5]
for a in datasets:
    if "statsmodels" in a["repo"]:
        break
print(a)
files = get_target_edit_files("repos/statsmodels", a["src_dir"], a['test']["test_dir"])

pkg_paths = ["repos/statsmodels/" + i for i in files]
module_set = ModuleSet([str(p) for p in pkg_paths])

all_modules_path = list(module_set.by_path.keys())


import_dependencies = {}
for path in sorted(module_set.by_path.keys()):
    module_name ='.'.join(module_set.by_path[path].fqn)
    mod = module_set.by_name[module_name]
    imports = module_set.get_imports(mod)
    import_dependencies[path] = [str(x) for x in imports]

for path, imports in import_dependencies.items():
    print(f"File: {path}")
    print("Imports:")
    for imp in imports:
        print(f"  - {imp}")
    print()

def ignore_cycles(graph):
    ts = TopologicalSorter(graph)
    try:
        return list(ts.static_order())
    except CycleError as e:
        print(f"Cycle detected: {e.args[1]}")
        # You can either break the cycle by modifying the graph or handle it as needed.
        # For now, let's just remove the first node in the cycle and try again.
        cycle_nodes = e.args[1]
        node_to_remove = cycle_nodes[0]
        print(f"Removing node {node_to_remove} to resolve cycle.")
        graph.pop(node_to_remove, None)
        return ignore_cycles(graph)


import_dependencies = ignore_cycles(import_dependencies)
print(import_dependencies)
