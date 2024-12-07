use quick_xml::events::Event;
use quick_xml::Reader;
use parser::Envelope;
use serde_json::Value;
use std::fs;


// read file from path
pub fn read_file(
    file_path: &str,
) -> Result<String, Box<dyn std::error::Error>> {
    let content = fs::read_to_string(file_path)?;
    Ok(content)
}

pub fn get_title_and_values_from_str(xml_str: &str) -> (Vec<String>, Vec<(String, String)>) {
    // Create a reader for the XML data
    let mut reader = Reader::from_str(xml_str);
    reader.config_mut().trim_text(true); // Optional: trims whitespace

    let mut buf = Vec::new(); // Buffer to hold the raw bytes of each XML element
    let mut titles = Vec::new(); // Stack to hold element names (titles)
    let mut titles_and_values = Vec::new(); // Stack to hold element names (titles) and values

    // Read the XML data as a stream of events
    loop {
        match reader.read_event_into(&mut buf) {
            Ok(Event::Start(ref e)) => {
                // Capture the element name (title) when a start tag is encountered
                let title = e.name().0.to_vec(); // Convert to Vec<u8> for later use
                titles.push(String::from_utf8(title).unwrap().replace("siri1:", "").replace("siri:", "").replace("soapenv:", "")); // Push the element name (title) to the stack
            }
            Ok(Event::Text(e)) => {
                // Capture the text value of the element when we encounter text
                let value = e.unescape().unwrap().into_owned(); // Decode the text
                let title = titles.pop().unwrap(); // Pop the last title from the stack
                titles_and_values.push((title, value)); // Push the title and value to the stack
            }
            Ok(Event::Eof) => break, // End of file
            Err(e) => panic!("Error at position {}: {:?}", reader.buffer_position(), e),
            _ => (), // Ignore other events
        }

        buf.clear(); // Clear the buffer to prepare for the next event
    }

    println!("{:?}", titles);

    (titles, titles_and_values)
}

pub fn remove_null_values(json_value: Value) -> Value {
    match json_value {
        Value::Object(obj) => {
            let obj = obj
                .into_iter()
                .filter(|(_, v)| !v.is_null())
                .map(|(k, v)| (k, remove_null_values(v)))
                .collect();
            Value::Object(obj)
        }
        Value::Array(arr) => {
            let arr = arr
                .into_iter()
                .filter(|v| !v.is_null())
                .map(remove_null_values)
                .collect();
            Value::Array(arr)
        }
        v => v,
    }
}

pub fn check_if_titles_are_in_value(titles: Vec<String>, json_value: Value) -> Result<(), String> {
    let mut titles = titles;
    let mut json_value = json_value;
    let mut title = titles.pop().unwrap();
    let mut value = json_value;
    while !titles.is_empty() {
        match value {
            Value::Object(obj) => {
                if obj.contains_key(&title) {
                    value = obj.get(&title).unwrap().clone();
                    title = titles.pop().unwrap();
                } else {
                    return Err(format!("Title {} not found in value", title));
                }
            }
            Value::Array(arr) => {
                if let Ok(index) = title.parse::<usize>() {
                    if index < arr.len() {
                        value = arr[index].clone();
                        title = titles.pop().unwrap();
                    } else {
                        return Err(format!("Index {} out of bounds", index));
                    }
                } else {
                    return Err(format!("Title {} is not an index", title));
                }
            }
            _ => return Err("Value is not an object or array".to_string()),
        }
    }
    Ok(())

}
