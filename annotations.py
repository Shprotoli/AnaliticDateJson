from typing import Dict, Tuple, List, Union, Generator
from datetime import datetime

# StartDateTime < EndDateTime
StartDateTime = datetime
EndDateTime = datetime

JsonNoParseDate = Dict[str, List[Dict[str, Union[int, str]]]]
JsonParseDays = Dict[int, List[Tuple[StartDateTime, EndDateTime]]]
ParserDayInfoJson = Generator[JsonParseDays, Dict[str, int]]
ParseTimeSlotInfoJson = Dict[int, Tuple[StartDateTime, EndDateTime]]