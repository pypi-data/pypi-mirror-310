use go_generation_derive::GoGenerate;
use serde::de::{self, Deserializer};
use serde::{Deserialize, Serialize};

use crate::structures::{
    estimated_call::EstimatedCall, journey_identifier::JourneyIdentifier,
    journey_pattern_info::JourneyPatternInfo, recorded_call::RecordedCall,
};

use super::{
    estimated_calls::EstimatedCalls, framed_vehicle_journey_ref::FramedVehicleJourneyRef,
    recorded_calls::RecordedCalls, train_numbers::TrainNumbers,
};

#[derive(Debug, Serialize, Clone, PartialEq, Eq, GoGenerate)]
#[serde(rename_all = "PascalCase")]
pub struct EstimatedVehicleJourney {
    pub line_ref: String,
    pub published_line_name: Option<String>,
    pub direction_ref: Option<String>,
    pub journey_identifier: Option<JourneyIdentifier>,
    pub dated_vehicule_journey_ref: Option<String>,
    pub cancellation: Option<String>,
    pub extra_journey: Option<bool>,
    pub journey_pattern_name: Option<String>,
    pub journey_pattern_info: Option<JourneyPatternInfo>,
    pub vehicle_mode: Option<String>,
    pub origin_ref: Option<String>,
    pub origin_name: Option<String>,
    pub destination_ref: Option<String>,
    pub destination_name: Option<String>,
    pub operator_ref: Option<String>,
    pub product_category_ref: Option<String>,
    pub train_numbers: Option<TrainNumbers>,
    pub vehicule_journey_name: Option<String>,
    pub origin_aimed_departure_time: Option<String>,
    pub destination_aimed_arrival_time: Option<String>,
    pub recorded_calls: Vec<RecordedCall>,
    pub estimated_calls: Vec<EstimatedCall>,
    pub framed_vehicle_journey_ref: Option<FramedVehicleJourneyRef>,
    pub data_source: Option<String>,
    pub vehicle_ref: Option<String>,
    pub aimed_departure_time: Option<String>,
    pub aimed_arrival_time: Option<String>,
    pub journey_note: Option<String>,
    pub headway_service: Option<String>,
    pub first_or_last_journey: Option<String>, // (firstServiceOfDay | lastServiceOfDay | otherService | unspecified).
    pub disruption_group: Option<String>,      // Voir Disruption­Group.
    pub journey_progress_info: Option<String>, // Voir JourneyProgressInfo.
}

impl<'de> Deserialize<'de> for EstimatedVehicleJourney {
    fn deserialize<D>(deserializer: D) -> Result<EstimatedVehicleJourney, D::Error>
    where
        D: Deserializer<'de>,
    {
        struct EstimatedVehicleJourneyVisitor;

        impl<'de> serde::de::Visitor<'de> for EstimatedVehicleJourneyVisitor {
            type Value = EstimatedVehicleJourney;

            fn expecting(&self, formatter: &mut std::fmt::Formatter) -> std::fmt::Result {
                formatter.write_str("an XML element representing XxxDelivery")
            }

            fn visit_map<V>(self, mut map: V) -> Result<Self::Value, V::Error>
            where
                V: serde::de::MapAccess<'de>,
            {
                let mut line_ref = None;
                let mut published_line_name = None;
                let mut direction_ref = None;
                let mut journey_identifier = None;
                let mut dated_vehicule_journey_ref = None;
                let mut cancellation = None;
                let mut extra_journey = None;
                let mut journey_pattern_name = None;
                let mut journey_pattern_info = None;
                let mut vehicle_mode = None;
                let mut origin_ref = None;
                let mut origin_name = None;
                let mut destination_ref = None;
                let mut destination_name = None;
                let mut operator_ref = None;
                let mut product_category_ref = None;
                let mut train_numbers = None;
                let mut vehicule_journey_name = None;
                let mut origin_aimed_departure_time = None;
                let mut destination_aimed_arrival_time = None;
                let mut recorded_calls = None;
                let mut estimated_calls = Vec::new();
                let mut framed_vehicle_journey_ref = None;
                let mut data_source = None;
                let mut vehicle_ref = None;
                let mut aimed_departure_time = None;
                let mut aimed_arrival_time = None;
                let mut journey_note = None;
                let mut headway_service = None;
                let mut first_or_last_journey = None;
                let mut disruption_group = None;
                let mut journey_progress_info = None;

                while let Some(key) = map.next_key()? {
                    println!("{:?} yip", key);
                    match key {
                        "LineRef" => {
                            line_ref = Some(map.next_value()?);
                        }
                        "PublishedLineName" => {
                            published_line_name = Some(map.next_value()?);
                        }
                        "DirectionRef" => {
                            direction_ref = Some(map.next_value()?);
                        }
                        "JourneyIdentifier" => {
                            journey_identifier = Some(map.next_value()?);
                        }

                        "DatedVehiculeJourneyRef" => {
                            dated_vehicule_journey_ref = Some(map.next_value()?);
                        }

                        "Cancellation" => {
                            cancellation = Some(map.next_value()?);
                        }

                        "ExtraJourney" => {
                            extra_journey = Some(map.next_value()?);
                        }

                        "JourneyPatternName" => {
                            journey_pattern_name = Some(map.next_value()?);
                        }

                        "JourneyPatternInfo" => {
                            journey_pattern_info = Some(map.next_value()?);
                        }

                        "VehicleMode" => {
                            vehicle_mode = Some(map.next_value()?);
                        }

                        "OriginRef" => {
                            origin_ref = Some(map.next_value()?);
                        }

                        "OriginName" => {
                            origin_name = Some(map.next_value()?);
                        }

                        "DestinationRef" => {
                            destination_ref = Some(map.next_value()?);
                        }

                        "DestinationName" => {
                            destination_name = Some(map.next_value()?);
                        }

                        "OperatorRef" => {
                            operator_ref = Some(map.next_value()?);
                        }

                        "ProductCategoryRef" => {
                            product_category_ref = Some(map.next_value()?);
                        }

                        "TrainNumbers" => {
                            train_numbers = Some(map.next_value()?);
                        }

                        "VehiculeJourneyName" => {
                            vehicule_journey_name = Some(map.next_value()?);
                        }

                        "OriginAimedDepartureTime" => {
                            origin_aimed_departure_time = Some(map.next_value()?);
                        }

                        "DestinationAimedArrivalTime" => {
                            destination_aimed_arrival_time = Some(map.next_value()?);
                        }

                        "RecordedCalls" => {
                            recorded_calls = Some(map.next_value()?);
                        }

                        "EstimatedCalls" => {
                            estimated_calls = map.next_value()?;
                        }

                        "FramedVehicleJourneyRef" => {
                            framed_vehicle_journey_ref = Some(map.next_value()?);
                        }

                        "DataSource" => {
                            data_source = Some(map.next_value()?);
                        }

                        "VehicleRef" => {
                            vehicle_ref = Some(map.next_value()?);
                        }

                        "AimedDepartureTime" => {
                            aimed_departure_time = Some(map.next_value()?);
                        }

                        "AimedArrivalTime" => {
                            aimed_arrival_time = Some(map.next_value()?);
                        }

                        "JourneyNote" => {
                            journey_note = Some(map.next_value()?);
                        }

                        "HeadwayService" => {
                            headway_service = Some(map.next_value()?);
                        }

                        "FirstOrLastJourney" => {
                            first_or_last_journey = Some(map.next_value()?);
                        }

                        "DisruptionGroup" => {
                            disruption_group = Some(map.next_value()?);
                        }

                        "JourneyProgressInfo" => {
                            journey_progress_info = Some(map.next_value()?);
                        }
                        "EstimatedVehicleJourneyCode" => {
                            let _ = map.next_value::<String>()?;
                        }

                        "VehicleJourneyName" => {
                            let _ = map.next_value::<String>()?;
                        }

                        "EstimatedCall" => {
                            let estimated_call = map.next_value::<EstimatedCall>()?;
                            estimated_calls.push(estimated_call);
                        }

                        _ => {}
                    }
                }

                todo!()
            }
        }

        deserializer.deserialize_map(EstimatedVehicleJourneyVisitor)
    }
}
