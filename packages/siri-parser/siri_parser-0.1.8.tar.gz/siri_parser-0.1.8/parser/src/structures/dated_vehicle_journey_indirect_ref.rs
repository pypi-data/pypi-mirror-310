use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};
use pyo3::pyclass;


#[pyclass]
#[derive(Debug, Clone,  Serialize, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct DatedVehicleJourneyIndirectRef {
    pub origin_ref: String,
    pub aimed_departure_time: String,
    pub destination_ref: String,
    pub aimed_arrival_time: String,
}
