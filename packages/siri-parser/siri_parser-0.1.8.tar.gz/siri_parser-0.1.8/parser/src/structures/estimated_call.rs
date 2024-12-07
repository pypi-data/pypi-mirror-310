use go_generation_derive::GoGenerate;
use serde::{Deserialize, Serialize};
use serde_json::Value;

use crate::enums::{
    arrival_status::ArrivalStatus, boarding_activity::BoardingActivity,
    departure_status::DepartureStatus, occupancy::Occupancy,
};

use serde::de::{self, Deserializer};
use pyo3::pyclass;


#[pyclass]
#[derive(Debug, Serialize, Clone, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct EstimatedCall {
    stop_point_ref: Option<String>,  // StopPointRef
    order: Option<u32>,              // positiveInteger
    stop_point_name: Option<String>, // NLString
    extra_call: Option<bool>,
    cancellation: Option<bool>,       // boolean
    occupancy: Option<Occupancy>,     // occupancy levels
    platform_traversal: Option<bool>, // boolean
    destination_display: Option<String>,
    aimed_arrival_time: Option<String>,          // dateTime
    expected_arrival_time: Option<String>,       // dateTime
    arrival_status: Option<ArrivalStatus>,       // onTime, missed, delayed, etc.
    arrival_proximity_text: Option<Vec<String>>, // NLString
    arrival_platform_name: Option<String>,       // NLString
    arrival_stop_assignment: Option<String>,     // structure
    aimed_quay_name: Option<String>,             // NLString
    aimed_departure_time: Option<String>,        // dateTime
    expected_departure_time: Option<String>,     // dateTime
    departure_status: Option<DepartureStatus>,   // onTime, early, delayed, etc.
    departure_platform_name: Option<String>,     // NLString
    departure_boarding_activity: Option<BoardingActivity>, // boarding, noBoarding, etc.
}

impl<'de> Deserialize<'de> for EstimatedCall {
    fn deserialize<D>(deserializer: D) -> Result<EstimatedCall, D::Error>
    where
        D: Deserializer<'de>,
    {
        struct EstimatedCallVisitor;

        impl<'de> serde::de::Visitor<'de> for EstimatedCallVisitor {
            type Value = EstimatedCall;

            fn expecting(&self, formatter: &mut std::fmt::Formatter) -> std::fmt::Result {
                formatter.write_str("an XML element representing XxxDelivery")
            }

            fn visit_seq<A>(self, seq: A) -> Result<Self::Value, A::Error>
            where
                A: de::SeqAccess<'de>,
            {
                let estimated_call: EstimatedCall = serde::de::Deserialize::deserialize(
                    de::value::SeqAccessDeserializer::new(seq),
                )?;
                println!("yapppp{:?}", estimated_call);
                Ok(estimated_call)
            }

            fn visit_map<V>(self, mut map: V) -> Result<Self::Value, V::Error>
            where
                V: serde::de::MapAccess<'de>,
            {
                let mut stop_point_ref = None;
                let mut order = None;
                let mut stop_point_name = None;
                let mut extra_call = None;
                let mut cancellation = None;
                let mut occupancy = None;
                let mut platform_traversal = None;
                let mut destination_display = None;
                let mut aimed_arrival_time = None;
                let mut expected_arrival_time = None;
                let mut arrival_status = None;
                let mut arrival_proximity_text = None;
                let mut arrival_platform_name = None;
                let mut arrival_stop_assignment = None;
                let mut aimed_quay_name = None;
                let mut aimed_departure_time = None;
                let mut expected_departure_time = None;
                let mut departure_status = None;
                let mut departure_platform_name = None;
                let mut departure_boarding_activity = None;

                while let Some(key) = map.next_key()? {
                    match key {
                        "EstimatedCall" => {
                            let value: EstimatedCall = map.next_value()?;
                            return Ok(value);
                        }
                        "StopPointRef" => {
                            stop_point_ref = Some(map.next_value()?);
                        }
                        "Order" => {
                            order = Some(map.next_value()?);
                        }
                        "StopPointName" => {
                            stop_point_name = Some(map.next_value()?);
                        }
                        "ExtraCall" => {
                            extra_call = Some(map.next_value()?);
                        }
                        "Cancellation" => {
                            cancellation = Some(map.next_value()?);
                        }
                        "Occupancy" => {
                            occupancy = Some(map.next_value()?);
                        }
                        "PlatformTraversal" => {
                            platform_traversal = Some(map.next_value()?);
                        }
                        "DestinationDisplay" => {
                            destination_display = Some(map.next_value()?);
                        }
                        "AimedArrivalTime" => {
                            aimed_arrival_time = Some(map.next_value()?);
                        }
                        "ExpectedArrivalTime" => {
                            expected_arrival_time = Some(map.next_value()?);
                        }
                        "ArrivalStatus" => {
                            arrival_status = Some(map.next_value()?);
                        }
                        "ArrivalProximityText" => {
                            arrival_proximity_text = Some(map.next_value()?);
                        }
                        "ArrivalPlatformName" => {
                            arrival_platform_name = Some(map.next_value()?);
                        }
                        "ArrivalStopAssignment" => {
                            arrival_stop_assignment = Some(map.next_value()?);
                        }
                        "AimedQuayName" => {
                            aimed_quay_name = Some(map.next_value()?);
                        }
                        "AimedDepartureTime" => {
                            aimed_departure_time = Some(map.next_value()?);
                        }
                        "ExpectedDepartureTime" => {
                            expected_departure_time = Some(map.next_value()?);
                        }

                        "DepartureStatus" => {
                            departure_status = Some(map.next_value()?);
                        }

                        "DeparturePlatformName" => {
                            departure_platform_name = Some(map.next_value()?);
                        }

                        "DepartureBoardingActivity" => {
                            departure_boarding_activity = Some(map.next_value()?);
                        }

                        _ => {
                            let _: serde_json::Value = map.next_value()?;
                        }
                    }
                }
                Ok(EstimatedCall {
                    stop_point_ref,
                    order,
                    stop_point_name,
                    extra_call,
                    cancellation,
                    occupancy,
                    platform_traversal,
                    destination_display,
                    aimed_arrival_time,
                    expected_arrival_time,
                    arrival_status,
                    arrival_proximity_text,
                    arrival_platform_name,
                    arrival_stop_assignment,
                    aimed_quay_name,
                    aimed_departure_time,
                    expected_departure_time,
                    departure_status,
                    departure_platform_name,
                    departure_boarding_activity,
                })
            }
        }

        deserializer.deserialize_map(EstimatedCallVisitor)
    }
}
