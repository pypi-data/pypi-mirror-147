__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2022, Vanessa Sochat"
__license__ = "MPL 2.0"

from pipelib.logger import logger


class Pipeline:
    """
    A pipeline holds or more steps to complete in a comparison process.
    """

    def __init__(self, steps=None):
        self.steps = []
        [self.add_step(s) for s in steps or []]

    def _validate_step(self, previous, step):
        """
        Validate that a step has the correct classes and can interact with
        the previous step.
        """
        for required in ["run", "_run"]:
            if not hasattr(step, required):
                logger.exit(f"Step {step} is missing required attribute {required}")

        # The new step must return something
        if not step.return_type:
            logger.error(f"Step {step} does not return anything.")
            return False

        return True

    def add_step(self, step):
        """
        Add a step to the pipeline, validating it first.

        We can also add an entire other pipeline to this pipeline, meaning
        we squash the steps.
        """
        # The final thing has to be a step!
        if "pipelib.main.steps" in step.__class__.__module__:
            self._add_step(step)

        # Add steps from other pipelines
        elif "pipelib.main.pipeline" in step.__class__.__module__:
            if not step.steps:
                return
            # Add the first step, must be compatible with list
            self._add_step(step.steps.pop(0))

            # Add the remainder of steps
            self.steps += step.steps
        else:
            logger.warning(f"Malformed step {step}, not adding to pipeline!")

    def _add_step(self, step):
        """
        Adding a step means checking that kwargs are provided
        """
        addstep = True
        if self.steps:
            addstep = self._validate_step(self.steps[-1], step)
        if addstep:
            logger.info(f"Adding step {step}")
            self.steps.append(step)

    def run(self, items):
        """
        Run the pipeline to parse the items.
        """
        for step in self.steps:
            if not items:
                break
            items = step.run(items=items)
        return items
