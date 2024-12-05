from edc_consent.consent_definition import ConsentDefinition
from edc_constants.constants import FEMALE, MALE
from edc_protocol.research_protocol_config import ResearchProtocolConfig

consent_v1 = ConsentDefinition(
    "edc_pharmacy.subjectconsentv1",
    version="1",
    start=ResearchProtocolConfig().study_open_datetime,
    end=ResearchProtocolConfig().study_close_datetime,
    age_min=18,
    age_is_adult=18,
    age_max=64,
    gender=[MALE, FEMALE],
)
