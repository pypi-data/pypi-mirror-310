use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};
use pyo3::pyclass;
use crate::models::service_delivery_info::ServiceDeliveryInfo;


#[pyclass]
#[derive(Debug, Deserialize, Clone, PartialEq, Serialize, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct NotifyMonitoring {
    #[serde(alias = "ServiceDeliveryInfo", alias = "ns2:ServiceDeliveryInfo")]
    pub service_delivery_info: ServiceDeliveryInfo,
}
