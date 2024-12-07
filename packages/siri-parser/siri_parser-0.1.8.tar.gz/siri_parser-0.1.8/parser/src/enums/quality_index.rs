use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize, PartialEq, GoGenerate, Eq, Clone)]
#[serde(rename_all = "camelCase")]
pub enum QualityIndex {
    Certain,
    VeryReliable,
    Reliable,
    Unreliable,
    Unconfirmed,
}
