use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};
use pyo3::pyclass;
use super::parametised_action::ParameterisedAction;



#[pyclass]
#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct PublishToMobileAction {
    pub parameterized_action: Option<ParameterisedAction>,
    pub incidents: Option<bool>,       // Defaults to true
    pub home_page: Option<bool>,       // Defaults to false
}