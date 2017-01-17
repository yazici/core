import pyblish.api


class ValidateMindbenderID(pyblish.api.InstancePlugin):
    """All models must have an ID attribute"""

    label = "Mindbender ID"
    order = pyblish.api.ValidatorOrder
    hosts = ["maya"]
    families = ["mindbender.model"]

    def process(self, instance):
        from maya import cmds

        missing = list()
        for node in cmds.listRelatives(instance, allDescendents=True):

            # Only check transforms with a shape
            if not cmds.listRelatives(node, shapes=True):
                continue

            try:
                self.log.info("Checking '%s'" % node)
                cmds.getAttr(node + ".mbID")
            except ValueError:
                missing.append(node)

        assert not missing, ("Missing ID attribute on: %s"
                             % ", ".join(missing))