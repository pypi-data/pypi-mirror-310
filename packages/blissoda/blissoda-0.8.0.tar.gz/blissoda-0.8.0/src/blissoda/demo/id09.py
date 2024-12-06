from ..id09.txs_processor import TxsProcessor


class DemoTxsProcessor(TxsProcessor):
    def __init__(self, **defaults) -> None:
        super().__init__(**defaults)
        self.detector = "difflab6"
        self.pixel = (10e-3, 10e-3)
        self.energy = 10


txs_processor = DemoTxsProcessor()
