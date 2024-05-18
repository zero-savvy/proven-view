use std::{collections::HashMap, env::current_dir, time::Instant, fs::File, io::{Write, Read}};
use clap::{App, Arg};

use nova_scotia::{
    circom::reader::load_r1cs, create_public_params, create_recursive_circuit, FileLocation, F, S,
};
use nova_snark::{CompressedSNARK, PublicParams};
use serde::Deserialize;
use serde_json::json;

#[derive(Deserialize)]
struct GeneralInput {
    frames: usize,
    prev_hash: [u64; 4],   // TODO: make it String
}

#[derive(Deserialize)]
struct PathInput {
    levels: usize,
    path_elements_start: Vec<String>,
    path_indices_start: Vec<u8>,
    leaf_start: [u64; 4],
    path_elements_end: Vec<String>,
    path_indices_end: Vec<u8>,
    leaf_end: [u64; 4],
}

#[derive(Deserialize)]
struct FrameInput {
    orig: Vec<Vec<Vec<String>>>,
}

fn fold_fold_fold(proof_type: String,
            selected_function: String,
            circuit_filepath: String,
            witness_gen_filepath: String,
            output_file_path: String,
            input_folder_path: String
        ) {
    type G1 = pasta_curves::pallas::Point;
    type G2 = pasta_curves::vesta::Point;

    println!(
        "Running NOVA with witness generator: {} and group: {}",
        witness_gen_filepath,
        std::any::type_name::<G1>()
    );
    
    let root = current_dir().unwrap();

    let circuit_file = root.join(circuit_filepath);
    let r1cs = load_r1cs::<G1, G2>(&FileLocation::PathBuf(circuit_file));
    let witness_generator_file = root.join(witness_gen_filepath);

    let mut private_inputs = Vec::new();
    let mut start_public_input: Vec<F::<G1>> = Vec::new();

    let mut input_file;

    if proof_type == "integrity" {
        input_file = File::open(input_folder_path.clone()+ ("/general.json")).expect("Failed to open the file");
    } else {
        input_file = File::open(input_folder_path.clone()+ ("/path.json")).expect("Failed to open the file");
    }
    let mut input_file_json_string = String::new();
    input_file.read_to_string(&mut input_file_json_string).expect("Unable to read from the file");

    let mut iteration_count = 0;
    

    if selected_function == "trim" {

        if proof_type == "integrity" {
            let input_data: GeneralInput = serde_json::from_str(&input_file_json_string).expect("Deserialization failed");
            iteration_count = input_data.frames;
            start_public_input.push(F::<G1>::from_raw(input_data.prev_hash));
            // start_public_input.push(F::<G1>::from(input_data.info));  // x|y|index
            for i in 0..iteration_count {
                let mut input_file = File::open(input_folder_path.clone() + "/frame_" + i.to_string().as_str() + ".json").expect("Failed to open the file");
                let mut input_file_json_string = String::new();
                input_file.read_to_string(&mut input_file_json_string).expect("Unable to read from the file");

                let input_data: FrameInput = serde_json::from_str(&input_file_json_string).expect("Deserialization failed");

                let mut private_input = HashMap::new();
                private_input.insert("orig".to_string(), json!(input_data.orig));
                private_inputs.push(private_input);
            }

        } else {
            let input_data: PathInput = serde_json::from_str(&input_file_json_string).expect("Deserialization failed");
            iteration_count = input_data.levels;
            start_public_input.push(F::<G1>::from_raw(input_data.leaf_start));
            start_public_input.push(F::<G1>::from_raw(input_data.leaf_end));
            // start_public_input.push(F::<G1>::from(input_data.info));  // x|y|index
            for i in 0..iteration_count {
                let mut private_input = HashMap::new();
                private_input.insert("firstPathElement".to_string(), json!(input_data.path_elements_start[i]));
                private_input.insert("lastPathElement".to_string(), json!(input_data.path_elements_end[i]));
                private_input.insert("firstPathSel".to_string(), json!(input_data.path_indices_start[i]));
                private_input.insert("lastPathSel".to_string(), json!(input_data.path_indices_end[i]));
                private_inputs.push(private_input);
            }
        }    
       
        
    } else {
        // Err("given function is not implemented yet :)");
        println!(
            "given function is not implemented yet :)"
        );
    }
    
    // let reader = BufReader::new(file);

    // Deserialize the JSON data into the defined structure
    // let data: Data = serde_json::from_reader(reader).expect("Failed to parse JSON");

    

    let start = Instant::now();
    let pp: PublicParams<G1, G2, _, _> = create_public_params(r1cs.clone());
    println!(
        "Creating keys from R1CS took {:?}",
        start.elapsed()
    );

    println!(
        "Number of constraints per step (primary circuit): {}",
        pp.num_constraints().0
    );
    println!(
        "Number of constraints per step (secondary circuit): {}",
        pp.num_constraints().1
    );

    println!(
        "Number of variables per step (primary circuit): {}",
        pp.num_variables().0
    );
    println!(
        "Number of variables per step (secondary circuit): {}",
        pp.num_variables().1
    );

    println!("Creating a RecursiveSNARK...");
    let start = Instant::now();
    let recursive_snark = create_recursive_circuit(
        FileLocation::PathBuf(witness_generator_file),
        r1cs,
        private_inputs,
        start_public_input.to_vec(),
        &pp,
    )
    .unwrap();
    println!("RecursiveSNARK creation took {:?}", start.elapsed());

    // TODO: empty?
    let z0_secondary = [F::<G2>::from(0)];

    // verify the recursive SNARK
    println!("Verifying a RecursiveSNARK...");
    let start = Instant::now();
    let res = recursive_snark.verify(&pp, iteration_count, &start_public_input, &z0_secondary);
    println!(
        "RecursiveSNARK::verify: {:?}, took {:?}",
        res,
        start.elapsed()
    );
    assert!(res.is_ok());

    // produce a compressed SNARK
    println!("Generating a CompressedSNARK using Spartan with IPA-PC...");
    let start = Instant::now();

    let (pk, vk) = CompressedSNARK::<_, _, _, _, S<G1>, S<G2>>::setup(&pp).unwrap();
    let res = CompressedSNARK::<_, _, _, _, S<G1>, S<G2>>::prove(&pp, &pk, &recursive_snark);
    println!(
        "CompressedSNARK::prove: {:?}, took {:?}",
        res.is_ok(),
        start.elapsed()
    );
    assert!(res.is_ok());
    let compressed_snark = res.unwrap();

    //--- dump data ---//
    // Create some data to serialize as JSON
    
    // Serialize the data to a JSON string
    let json_string = serde_json::to_string(&compressed_snark).unwrap();

    // Open a file for writing
    let mut file = File::create(output_file_path.clone()).expect("Unable to create the file");

    // Write the JSON string to the file
    file.write_all(json_string.as_bytes()).expect("Unable to write to the file");

    println!("Data has been written to output.json");

    println!("-------------- Load Data --------");
    let mut file = File::open(output_file_path.clone()).expect("Unable to open the file");
    let mut json_string = String::new();
    file.read_to_string(&mut json_string).expect("Unable to read from the file");
    
    let compressed_snark2: CompressedSNARK<_, _, _, _, _, _> = serde_json::from_str(&json_string).expect("Deserialization failed");

    // verify the compressed SNARK
    println!("Verifying a CompressedSNARK...");
    let start = Instant::now();
    let res = compressed_snark2.verify(
        &vk,
        iteration_count,
        start_public_input.to_vec(),
        z0_secondary.to_vec(),
    );
    println!(
        "CompressedSNARK::verify: {:?}, took {:?}",
        res.is_ok(),
        start.elapsed()
    );
    assert!(res.is_ok());
}

fn main() {
    let matches = App::new("provenview")
        .version("v0.1.0")
        .author("Zero-Savvy")
        .about("Prove the truthfulness of your media!")
        .arg(
            Arg::with_name("input")
            .required(true)
            .short("i")
            .long("input")
            .value_name("FILE")
            .help("The JSON file containing the original and the transformed image data to verify.")
            .takes_value(true)
        )
        .arg(
            Arg::with_name("proof")
            .required(true)
            .short("p")
            .long("proof")
            .value_name("PROOF")
            .help("Type of the proof to be generated.")
            .takes_value(true)
            .possible_values(&["integrity", "authenticity"])
        )
        .arg(
            Arg::with_name("output")
            .required(true)
            .short("o")
            .long("output")
            .value_name("FILE")
            .help("This file will contain the final Proof to be verified by others.")
            .takes_value(true)
        )
        .arg(
            Arg::with_name("circuit")
            .required(true)
            .short("c")
            .long("circuit")
            .value_name("R1CS FILE")
            .help("The R1CS file of the compiled Circom circuit.")
            .takes_value(true)
        )
        .arg(
            Arg::with_name("witnessgenerator")
            .required(true)
            .short("w")
            .long("witnessgenerator")
            .value_name("BINARY/WASM FILE")
            .help("Witness generator file of the circuit.")
            .takes_value(true)
        )
        .arg(
            Arg::with_name("function")
            .required(true)
            .short("f")
            .long("function")
            .value_name("FUNCTION")
            .help("The transformation function.")
            .takes_value(true)
            .possible_values(&["trim"])
        )
        .get_matches();

    let witness_gen_filepath = matches.value_of("witnessgenerator").unwrap();
    let circuit_filepath = matches.value_of("circuit").unwrap();
    let output_filepath = matches.value_of("output").unwrap();
    let input_filepath = matches.value_of("input").unwrap();
    let proof_type = matches.value_of("proof").unwrap();
    let selected_function = matches.value_of("function").unwrap();

    println!(" ________________________________________________________");
    println!(" ____                          __     ___               ");
    println!("|  _ \\ _ __ _____   _____ _ __ \\ \\   / (_) _____      __");
    println!("| |_) | '__/ _ \\ \\ / / _ \\ '_ \\ \\ \\ / /| |/ _ \\ \\ /\\ / /");
    println!("|  __/| | | (_) \\ V /  __/ | | | \\ V / | |  __/\\ V  V / ");
    println!("|_|   |_|  \\___/ \\_/ \\___|_| |_|  \\_/  |_|\\___| \\_/\\_/  ");
    println!(" ________________________________________________________");
    println!("| Proof Type: {}", proof_type);
    println!("| Input file: {}", input_filepath);
    println!("| Ouput file: {}", output_filepath);
    println!("| Selected function: {}", selected_function);
    println!("| Circuit file: {}", circuit_filepath);
    println!("| Witness generator: {}", witness_gen_filepath);
    println!(" ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾");


    fold_fold_fold(proof_type.to_string(),
                selected_function.to_string().clone(),
                circuit_filepath.to_string().clone(),
                witness_gen_filepath.to_string(),
                output_filepath.to_string(),
                input_filepath.to_string()
            );

}