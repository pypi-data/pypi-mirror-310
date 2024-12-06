from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, List

from chat2edit_image.cv.base import Predictor
from chat2edit_image.cv.manage.predictor_init import PredictorInit
from chat2edit_image.cv.manage.predictor_manager import PredictorManager

manager = None


def init_predictors(inits: List[PredictorInit]) -> None:
    global manager

    if manager is None:
        manager = PredictorManager(inits)
        manager.init()


@asynccontextmanager
async def get_predictor(name: str) -> AsyncGenerator[Predictor, Any]:
    global manager
    predictor = await manager.get(name)

    try:
        yield predictor
    finally:
        manager.claim(predictor)
