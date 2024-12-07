use super::{journey_part::JourneyPart, train_number::TrainNumber};
use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};
use pyo3::pyclass;

#[pyclass]
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct OperationalInfo {
    pub train_numbers: Vec<TrainNumber>,
    pub journey_parts: Vec<JourneyPart>,
}
