use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};
use pyo3::pyclass;


#[pyclass]
#[derive(Debug, Default, Clone, Serialize, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct JourneyPartInfo {
    journey_part_ref: String,         // JourneyPart-Code
    train_number_ref: Option<String>, // TrainNumber
}
