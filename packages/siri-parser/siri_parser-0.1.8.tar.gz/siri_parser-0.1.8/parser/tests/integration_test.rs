mod common;

#[cfg(test)]
mod tests {

    use crate::common;
    use parser::{Envelope, SiriServiceType, SIRI};
    use serde_json::Value;
    use test_case::test_case;

    #[test_case("../src/fixtures/siri_et_xml_tn/trip_add.xml" ; "trip_add test")]
    fn test_siri_file(file_name: &str) {
        let siri = SIRI::from_file::<Envelope>(file_name);
        println!("{:?}", siri);
        assert!(siri.is_ok());
        let envelope = siri.unwrap();
        let json_value: Value = serde_json::to_value(&envelope).unwrap();
        let json_value_without_nulls = common::remove_null_values(json_value);
        println!(
            "{}",
            serde_json::to_string_pretty(&json_value_without_nulls).unwrap()
        );
        let file = common::read_file(file_name).unwrap();
        let (titles, titles_and_values) = common::get_title_and_values_from_str(&file);
        //let response = common::check_if_titles_are_in_value(titles, json_value_without_nulls);
        // println!("{:?}", response);

        //println!("envelope_str: {:?}", envelope_str);

        // common::get_title_and_values_from_str(xml_data);
    }
}
