use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};
use pyo3::pyclass;
use super::{dated_call::DatedCall, journey_pattern_info_group::JourneyPatternInfoGroup, service_info_group::ServiceInfoGroup};


#[pyclass]
#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct DatedVehicleJourney {
    pub vehicle_journey_name: Option<String>,
    pub destination_display: Option<String>,
    pub headway_service: Option<bool>,
    pub monitored: Option<bool>,
    pub dated_calls: Vec<DatedCall>,
    #[serde(flatten)]
    pub service_info_group: Option<ServiceInfoGroup>,
    #[serde(flatten)]
    pub journey_pattern_info: Option<JourneyPatternInfoGroup>
}