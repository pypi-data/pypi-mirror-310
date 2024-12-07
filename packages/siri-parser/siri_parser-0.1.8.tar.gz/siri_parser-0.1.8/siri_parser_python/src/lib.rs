use parser::models::body::Body as BodyParser;
use parser::services::connection_monitoring::NotifyConnectionMonitoring;
use parser::services::estimated_table::NotifyEstimatedTimetable;
use parser::services::facility_monitoring::NotifyFacilityMonitoring;
use parser::services::general_message::NotifyGeneralMessage;
use parser::services::production_timetable::NotifyProductionTimetable;
use parser::services::situation_exchange::NotifySituationExchange;
use parser::services::stop_monitoring::NotifyStopMonitoring;
use parser::services::vehicle_monitoring::NotifyVechicleMonitoring;
use parser::structures::action_data::ActionData;
use parser::structures::affected_stop_point::AffectedStopPoint;
use parser::structures::direction::Direction;
use parser::structures::monitored_feeder_arrival::MonitoredFeederArrival;
use parser::structures::monitored_feeder_arrival_cancellation::MonitoredFeederArrivalCancellation;
use parser::structures::wait_prolonged_departure::WaitProlongedDeparture;
use parser::structures::stopping_position_change_departure::StoppingPositionChangeDeparture;
use parser::structures::distributor_departure_cancellation::DistributorDepartureCancellation;
use parser::structures::distribuor_info::DistributorInfo;
use parser::structures::connecting_journey::ConnectingJourney;
use parser::structures::feeder_journey::FeederJourney;
use parser::structures::journey_info::JourneyInfo;
use parser::structures::pt_structure_element::PtSituationElement;
use parser::structures::situation_based_identity_group::SituationBasedIdentityGroup;
use parser::structures::situation_source::SituationSource;
use parser::structures::pt_situation_body_group::PtSituationBodyGroup;
use parser::structures::reason_group::ReasonGroup;
use parser::structures::pt_advice::PtAdvice;
use parser::structures::pt_consequence::PtConsequence;
use parser::structures::blocking::Blocking;
use parser::structures::boarding::Boarding;
use parser::structures::publishing_actions::PublishingActions;
use parser::structures::notify_by_sms_action::NotifyBySmsAction;
use parser::structures::notify_by_email_action::NotifyByEmailAction;
use parser::structures::publish_to_web_action::PublishToWebAction;
use parser::structures::publish_to_mobile_action::PublishToMobileAction;
use parser::structures::publish_to_display_action::PublishToDisplayAction;
use parser::structures::parametised_action::ParameterisedAction;
use parser::structures::affect::Affect;
use parser::structures::publish_at_scope::PublishAtScope;
use parser::structures::before_notice::BeforeNotice;
use parser::structures::network::Network;
use parser::structures::affected_network::AffectedNetwork;
use parser::structures::zone::Zone;
use parser::structures::affected_line::AffectedLine;
use parser::structures::affected_operator::AffectedOperator;
use parser::structures::affected_vehicle_journey::AffectedVehicleJourney;
use parser::structures::affected_place::AffectedPlace;
use parser::structures::affected_mode::AffectedMode;
use parser::structures::dated_timetable_version_frame::DatedTimetableVersionFrame;
use parser::structures::dated_vehicle_journey::DatedVehicleJourney;
use parser::structures::dated_call::DatedCall;
use parser::structures::targeted_interchange::TargetedInterchange;
use parser::structures::distributor_connection_link::DistributorConnectionLink;
use parser::structures::service_info_group::ServiceInfoGroup;
use parser::structures::journey_end_names::JourneyEndNames;
use parser::structures::journey_identifier::JourneyIdentifier;
use parser::structures::journey_pattern_info::JourneyPatternInfo;
use parser::structures::service_info::ServiceInfo;
use parser::structures::vehicle_journey_info::VehicleJourneyInfo;
use parser::structures::estimated_info::EstimatedInfo;
use parser::structures::journey_progress_info::JourneyProgressInfo;
use parser::structures::operational_info::OperationalInfo;
use parser::structures::dated_vehicle_journey_indirect_ref::DatedVehicleJourneyIndirectRef;
use parser::structures::estimated_vehicle_journey::EstimatedVehicleJourney;
use parser::structures::fist_or_last_journey_enum::FirstOrLastJourneyEnum;
use parser::structures::calls::Calls;
use parser::structures::recorded_call::RecordedCall;
use parser::structures::estimated_call::EstimatedCall;
use parser::structures::distribution_group::DisruptionGroup;
use parser::structures::train_number::TrainNumber;
use parser::structures::journey_part::JourneyPart;
use parser::structures::stop_assigment::StopAssignment;
use parser::structures::expected_departure_capacity::ExpectedDepartureCapacity;
use parser::structures::expected_departure_occupancy::ExpectedDepartureOccupancy;
use parser::structures::departure_info::DepartureInfo;
use parser::structures::arrival_info::ArrivalInfo;
use parser::structures::arrival::Arrival;
use parser::structures::departure::Departure;
use parser::structures::expected_capacity::ExpectedCapacity;
use parser::structures::expected_occupancy::ExpectedOccupancy;
use parser::structures::group_reservation::GroupReservation;
use parser::structures::monitored_stop_visit::MonitoredStopVisit;
use parser::structures::monitored_stop_visit_cancellation::MonitoredStopVisitCancellation;
use parser::structures::monitored_vehicle_journey::MonitoredVehicleJourney;
use parser::structures::journey_part_info::JourneyPartInfo;
use parser::structures::monitored_call::MonitoredCall;
use parser::structures::stop_identity::StopIdentity;
use parser::structures::onward_call::OnwardCall;
use parser::structures::vehicle_journey_info_group::VehicleJourneyInfoGroup;
use parser::structures::journey_end_names_group::JourneyEndNamesGroup;
use parser::structures::journey_pattern_info_group::JourneyPatternInfoGroup;
use parser::structures::via::Via;
use parser::structures::journey_progress_info_group::JourneyProgressInfoGroup;
use parser::structures::location_structure::LocationStructure;
use parser::structures::notifity_monitoring::NotifyMonitoring;
use parser::structures::vehicle_activity_cancellation::VehicleActivityCancellation;
use parser::structures::vehicle_activity::VehicleActivity;
use parser::structures::progress_between_stops::ProgressBetweenStops;
use parser::structures::framed_vehicle_journey_ref::FramedVehicleJourneyRef;
use parser::structures::facility_condition::FacilityCondition;
use parser::structures::facility::Facility;
use parser::structures::facility_location::FacilityLocation;
use parser::structures::facility_status::FacilityStatus;
use parser::structures::accessibility_assesment::AccessibilityAssessment;
use parser::structures::validity_period::ValidityPeriod;
use parser::structures::line::Line;
use parser::structures::validity_condition::ValidityCondition;
use parser::structures::info_message::InfoMessage;
use parser::structures::info_message_cancellation::InfoMessageCancellation;
use parser::SiriServiceType;
use parser::{Envelope as EnvelopeParser, SIRI as SIRIParser};
use pyo3::prelude::*;

#[pyclass]
pub struct SIRI {}

#[pyclass]
pub struct Body(BodyParser);

#[pymethods]
impl Body {
    #[new]
    fn new(service_type: BodyParser) -> Self {
        Body(service_type)
    }

    /// Method to get string representation of the Body
    pub fn __str__(&self) -> String {
        format!("{:?}", self.0) // Assuming Body implements Display
    }

    /// Method to get NotifyProductionTimetable from Body in Python
    ///
    /// # Returns
    /// * `PyResult<Option<NotifyProductionTimetable>>`
    ///
    pub fn notify_production_timetable(&self) -> PyResult<Option<NotifyProductionTimetable>> {
        if let BodyParser(SiriServiceType::ProductionTimetable(ref production_timetable)) =
            self.0.clone()
        {
            Ok(Some(production_timetable.clone()))
        } else {
            Ok(None)
        }
    }

    /// Method to get NotifyEstimatedTimetable from Body in Python
    ///
    /// # Returns
    /// * `PyResult<Option<NotifyEstimatedTimetable>>`
    pub fn notify_estimated_timetable(&self) -> PyResult<Option<NotifyEstimatedTimetable>> {
        if let BodyParser(SiriServiceType::EstimatedTimetable(ref estimated_timetable)) =
            self.0.clone()
        {
            Ok(Some(estimated_timetable.clone()))
        } else {
            Ok(None)
        }
    }

    /// Method to get NotifyStopMonitoring from Body in Python
    ///
    /// # Returns
    /// * `PyResult<Option<NotifyStopMonitoring>>`
    pub fn notify_stop_monitoring(&self) -> PyResult<Option<NotifyStopMonitoring>> {
        if let BodyParser(SiriServiceType::StopMonitoring(ref stop_monitoring)) = self.0.clone() {
            Ok(Some(stop_monitoring.clone()))
        } else {
            Ok(None)
        }
    }

    /// Method to get NotifySituationExchange from Body in Python
    ///
    /// # Returns
    /// * `PyResult<Option<NotifySituationExchange>>`
    pub fn notify_vehicle_monitoring(&self) -> PyResult<Option<NotifyVechicleMonitoring>> {
        if let BodyParser(SiriServiceType::VehicleMonitoring(ref vehicle_monitoring)) =
            self.0.clone()
        {
            Ok(Some(vehicle_monitoring.clone()))
        } else {
            Ok(None)
        }
    }

    /// Method to get NotifyConnectionMonitoring from Body in Python
    ///
    /// # Returns
    /// * `PyResult<Option<NotifyConnectionMonitoring>>`
    pub fn notify_connection_monitoring(&self) -> PyResult<Option<NotifyConnectionMonitoring>> {
        if let BodyParser(SiriServiceType::ConnectionMonitoring(ref connection_monitoring)) =
            self.0.clone()
        {
            Ok(Some(connection_monitoring.clone()))
        } else {
            Ok(None)
        }
    }

    /// Method to get NotifyGeneralMessage from Body in Python
    ///
    /// # Returns
    /// * `PyResult<Option<NotifyGeneralMessage>>`
    pub fn notify_general_message(&self) -> PyResult<Option<NotifyGeneralMessage>> {
        if let BodyParser(SiriServiceType::GeneralMessage(ref general_message)) = self.0.clone() {
            Ok(Some(general_message.clone()))
        } else {
            Ok(None)
        }
    }

    /// Method to get NotifyFacilityMonitoring from Body in Python
    ///
    /// # Returns
    /// * `PyResult<Option<NotifyFacilityMonitoring>>`
    pub fn notify_facility_monitoring(&self) -> PyResult<Option<NotifyFacilityMonitoring>> {
        if let BodyParser(SiriServiceType::FacilityMonitoring(ref facility_monitoring)) =
            self.0.clone()
        {
            Ok(Some(facility_monitoring.clone()))
        } else {
            Ok(None)
        }
    }
}

#[pyclass]
pub struct Envelope(EnvelopeParser); // Wrapper for the Envelope type

#[pymethods]
impl Envelope {
    // Method to get string representation
    pub fn __str__(&self) -> String {
        format!("{:?}", self.0) // Assuming Envelope implements Display
    }

    pub fn body(&self) -> PyResult<Body> {
        return Ok(Body(self.0.body.clone()));
    }
}

#[pymethods]
impl SIRI {
    #[new]
    pub fn new() -> Self {
        SIRI {}
    }

    // Method to parse SIRI XML string to Envelope
    pub fn parse(&self, s: &str) -> PyResult<Envelope> {
        Python::with_gil(|_py| {
            match SIRIParser::from_str::<EnvelopeParser>(s) {
                Ok(envelope) => Ok(Envelope(envelope)), // Wrap Envelope
                Err(e) => Err(PyErr::new::<pyo3::exceptions::PyValueError, _>(
                    e.to_string(),
                )),
            }
        })
    }
}

#[pymodule]
fn siri_parser(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<SIRI>()?;
    m.add_class::<Envelope>()?; // Add PyEnvelope class
    m.add_class::<Body>()?;
    m.add_class::<NotifyProductionTimetable>()?;
    m.add_class::<NotifyStopMonitoring>()?;
    m.add_class::<NotifySituationExchange>()?;
    m.add_class::<NotifyGeneralMessage>()?;
    m.add_class::<NotifyFacilityMonitoring>()?;
    m.add_class::<NotifyVechicleMonitoring>()?;
    m.add_class::<NotifyConnectionMonitoring>()?;
    m.add_class::<NotifyEstimatedTimetable>()?;
    m.add_class::<AffectedStopPoint>()?;
    m.add_class::<Zone>()?;
    m.add_class::<AffectedLine>()?;
    m.add_class::<AffectedOperator>()?;
    m.add_class::<AffectedVehicleJourney>()?;
    m.add_class::<AffectedPlace>()?;
    m.add_class::<AffectedMode>()?;
    m.add_class::<DatedTimetableVersionFrame>()?;
    m.add_class::<DatedVehicleJourney>()?;
    m.add_class::<DatedCall>()?;
    m.add_class::<TargetedInterchange>()?;
    m.add_class::<DistributorConnectionLink>()?;
    m.add_class::<ServiceInfoGroup>()?;
    m.add_class::<JourneyEndNames>()?;
    m.add_class::<JourneyPatternInfo>()?;
    m.add_class::<ServiceInfo>()?;
    m.add_class::<VehicleJourneyInfo>()?;
    m.add_class::<EstimatedInfo>()?;
    m.add_class::<JourneyProgressInfo>()?;
    m.add_class::<OperationalInfo>()?;
    m.add_class::<DatedVehicleJourneyIndirectRef>()?;
    m.add_class::<EstimatedVehicleJourney>()?;
    m.add_class::<FirstOrLastJourneyEnum>()?;
    m.add_class::<Calls>()?;
    m.add_class::<RecordedCall>()?;
    m.add_class::<EstimatedCall>()?;
    m.add_class::<DisruptionGroup>()?;
    m.add_class::<TrainNumber>()?;
    m.add_class::<JourneyPart>()?;
    m.add_class::<StopAssignment>()?;
    m.add_class::<ExpectedDepartureCapacity>()?;
    m.add_class::<ExpectedDepartureOccupancy>()?;
    m.add_class::<DepartureInfo>()?;
    m.add_class::<ArrivalInfo>()?;
    m.add_class::<Arrival>()?;
    m.add_class::<Departure>()?;
    m.add_class::<ExpectedCapacity>()?;
    m.add_class::<ExpectedOccupancy>()?;
    m.add_class::<GroupReservation>()?;
    m.add_class::<MonitoredStopVisit>()?;
    m.add_class::<MonitoredStopVisitCancellation>()?;
    m.add_class::<MonitoredVehicleJourney>()?;
    m.add_class::<JourneyPartInfo>()?;
    m.add_class::<MonitoredCall>()?;
    m.add_class::<StopIdentity>()?;
    m.add_class::<OnwardCall>()?;
    m.add_class::<VehicleJourneyInfoGroup>()?;
    m.add_class::<JourneyEndNamesGroup>()?;
    m.add_class::<JourneyPatternInfoGroup>()?;
    m.add_class::<Via>()?;
    m.add_class::<JourneyProgressInfoGroup>()?;
    m.add_class::<LocationStructure>()?;
    m.add_class::<NotifyMonitoring>()?;
    m.add_class::<VehicleActivityCancellation>()?;
    m.add_class::<VehicleActivity>()?;
    m.add_class::<ProgressBetweenStops>()?;
    m.add_class::<FramedVehicleJourneyRef>()?;
    m.add_class::<FacilityCondition>()?;
    m.add_class::<Facility>()?;
    m.add_class::<FacilityLocation>()?;
    m.add_class::<FacilityStatus>()?;
    m.add_class::<AccessibilityAssessment>()?;
    m.add_class::<ValidityPeriod>()?;
    m.add_class::<Line>()?;
    m.add_class::<ValidityCondition>()?;
    m.add_class::<InfoMessage>()?;
    m.add_class::<InfoMessageCancellation>()?;
    m.add_class::<ActionData>()?;
    m.add_class::<AffectedStopPoint>()?;
    m.add_class::<Direction>()?;
    m.add_class::<MonitoredFeederArrival>()?;
    m.add_class::<MonitoredFeederArrivalCancellation>()?;
    m.add_class::<WaitProlongedDeparture>()?;
    m.add_class::<StoppingPositionChangeDeparture>()?;
    m.add_class::<DistributorDepartureCancellation>()?;
    m.add_class::<DistributorInfo>()?;
    m.add_class::<ConnectingJourney>()?;
    m.add_class::<FeederJourney>()?;
    m.add_class::<JourneyInfo>()?;
    m.add_class::<PtSituationElement>()?;
    m.add_class::<SituationBasedIdentityGroup>()?;
    m.add_class::<SituationSource>()?;
    m.add_class::<PtSituationBodyGroup>()?;
    m.add_class::<ReasonGroup>()?;
    m.add_class::<PtAdvice>()?;
    m.add_class::<PtConsequence>()?;
    m.add_class::<Blocking>()?;
    m.add_class::<Boarding>()?;
    m.add_class::<PublishingActions>()?;
    m.add_class::<NotifyBySmsAction>()?;
    m.add_class::<NotifyByEmailAction>()?;
    m.add_class::<PublishToWebAction>()?;
    m.add_class::<PublishToMobileAction>()?;
    m.add_class::<PublishToDisplayAction>()?;
    m.add_class::<ParameterisedAction>()?;
    m.add_class::<Affect>()?;
    m.add_class::<PublishAtScope>()?;
    m.add_class::<BeforeNotice>()?;
    m.add_class::<Network>()?;
    m.add_class::<AffectedNetwork>()?;
    Ok(())
}
