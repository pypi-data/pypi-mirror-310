use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};
use pyo3::pyclass;



#[pyclass]
#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct ProgressBetweenStops {
    pub link_distance: Option<i32>,
    pub percentage: Option<i32>,
}
