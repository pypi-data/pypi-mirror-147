from typing import Dict, List
from hatchling.metadata.plugin.interface import MetadataHookInterface

class CustomMetadataHook(MetadataHookInterface):
    # combine all optional dependencies into one group called 'all'

    # name that defines all optional dependencies
    # SUB_GROUP_PREFIX = '$'
    # REMOVE_GROUP_PREFIX = '_'
    GROUP = 'all'

    def update(self, metadata: Dict):
        deps: Dict[str, List[str]] = metadata.setdefault('optional-dependencies', {})
        all = set()

        for v in deps.values():
            all.extend(v)

        deps[self.GROUP] = list(all)
        # group: str
        # deps: List[str]
        # for group, deps in opt_deps.copy().items():
        #     for i in deps:
        #         if i[0] == self.SUB_GROUP_PREFIX:
        #             target_group = opt_deps.get(i[1:], None)

        #             if target_group is not None:
        #                 opt_deps[group].remove(i)
        #                 opt_deps[group].extend(target_group)
        #             else:
        #                 raise Exception(f'Group {i[1:]} has not been found')

        # for group, _ in dict(opt_deps).items():
        #     if group[0] == self.REMOVE_GROUP_PREFIX:
        #         del opt_deps[group]

        # print(opt_deps)


        # dependencies = set()


        # if 'all' in opt_deps:
        #     for k, v in opt_deps:
        #         if k == 'all':
        #             continue

        #         opt_deps.setdefault('all', )

        # v: List
        # for _, v in metadata.get('optional-dependencies', {}).items():
        #     dependencies.add(v)

        # # metadata.setdefault
        # print('hello', type(metadata))
