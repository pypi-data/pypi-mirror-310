

use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};
use pyo3::pyclass;
use super::affected_stop_point::AffectedStopPoint;


#[pyclass]
#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct AffectedLine {
    pub line_ref: String,
    pub destinations: Vec<AffectedStopPoint>,

}