use std::fmt;

use quick_xml::de;
use serde::{
    de::{MapAccess, SeqAccess, Visitor},
    ser, Deserialize, Deserializer, Serialize,
};
use serde_json::Value;

use crate::structures::estimated_call::EstimatedCall;

#[derive(Debug, Serialize, Clone, PartialEq, Eq)]
#[serde(rename_all = "PascalCase")]
pub struct EstimatedCalls(pub Vec<EstimatedCall>);

impl<'de> Deserialize<'de> for EstimatedCalls {
    fn deserialize<D>(deserializer: D) -> Result<EstimatedCalls, D::Error>
    where
        D: Deserializer<'de>,
    {
        struct EstimatedCallsVisitor;

        impl<'de> Visitor<'de> for EstimatedCallsVisitor {
            type Value = EstimatedCalls;

            fn expecting(&self, formatter: &mut fmt::Formatter) -> fmt::Result {
                formatter.write_str("struct EstimatedCalls")
            }

            fn visit_seq<A>(self, mut seq: A) -> Result<EstimatedCalls, A::Error>
            where
                A: SeqAccess<'de>,
            {
                let mut estimated_calls = Vec::new();
                while let Some(value) = seq.next_element::<EstimatedCall>()? {
                    estimated_calls.push(value);
                }

                Ok(EstimatedCalls(estimated_calls))
            }
        }

        deserializer.deserialize_seq(EstimatedCallsVisitor)
    }
}
