
use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};
use pyo3::pyclass;
use crate::enums::scope_type::ScopeType;
use super::affect::Affect;



#[pyclass]
#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct PublishAtScope {
    pub scope_type: Option<ScopeType>,
    pub affects: Vec<Affect>,
}



