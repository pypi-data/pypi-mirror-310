use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};
use pyo3::pyclass;

#[pyclass]
#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct FramedVehicleJourneyRef {
    pub data_frame_ref: Option<String>,
    pub dated_vehicle_journey_ref: Option<String>,
}
