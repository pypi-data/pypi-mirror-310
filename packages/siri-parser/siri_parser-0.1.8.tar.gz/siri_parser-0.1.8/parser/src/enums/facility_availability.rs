use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Clone, Deserialize, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "camelCase")]
pub enum FacilityAvailability {
    Unknown,
    Available,
    NotAvailable,
    PartiallyAvailable,
    Added,
    Removed,
}
