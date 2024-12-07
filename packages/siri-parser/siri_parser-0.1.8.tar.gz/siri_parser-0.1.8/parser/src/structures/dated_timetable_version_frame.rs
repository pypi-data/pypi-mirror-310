use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};
use pyo3::pyclass;
use super::dated_vehicle_journey::DatedVehicleJourney;


#[pyclass]
#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct DatedTimetableVersionFrame{
    pub recorded_at_time: String,
    pub line_ref: String,
    pub direction_ref: String,
    pub dated_vehicle_journey: DatedVehicleJourney
}