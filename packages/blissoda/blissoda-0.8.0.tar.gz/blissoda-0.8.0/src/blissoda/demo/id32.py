try:
    from bliss import setup_globals
except ImportError:
    setup_globals = None

from ..id32.processor import Id32SpecGenProcessor


class DemoId32Processor(Id32SpecGenProcessor):
    WORKER = None

    def __init__(self, **defaults) -> None:
        super().__init__(("difflab6",), **defaults)


if setup_globals is None:
    id32_processor = None
else:
    id32_processor = DemoId32Processor()
