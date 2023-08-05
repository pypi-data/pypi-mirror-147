/*
 * VegaFusion
 * Copyright (C) 2022 Jon Mease
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public
 * License along with this program.
 * If not, see http://www.gnu.org/licenses/.
 */
#[macro_use]
extern crate lazy_static;

mod util;
use crate::util::vegajs_runtime::{vegajs_runtime, ExportImage, ExportImageFormat};

use datafusion::scalar::ScalarValue;
use serde_json::json;
use std::collections::HashMap;
use std::fs;

use vegafusion_core::arrow::datatypes::DataType;
use vegafusion_core::data::table::VegaFusionTable;
use vegafusion_core::planning::watch::{
    ExportUpdate, ExportUpdateBatch, ExportUpdateNamespace, Watch, WatchNamespace,
};
use vegafusion_core::spec::chart::ChartSpec;
use vegafusion_core::spec::transform::extent::ExtentTransformSpec;
use vegafusion_core::spec::transform::filter::FilterTransformSpec;
use vegafusion_core::spec::transform::TransformSpec;
use vegafusion_rt_datafusion::data::table::VegaFusionTableUtils;
use vegafusion_rt_datafusion::expression::compiler::config::CompilationConfig;

#[test]
fn test_vegajs_parse() {
    let vegajs_runtime = vegajs_runtime();
    let parsed = vegajs_runtime.parse_expression("(20 + 5) * 300").unwrap();

    let expected_estree: util::estree_expression::ESTreeExpression =
        serde_json::value::from_value(json!({
            "type":"BinaryExpression",
            "left":{
                "type":"BinaryExpression",
                "left":{"type":"Literal","value":20.0,"raw":"20"},
                "operator":"+",
                "right":{"type":"Literal","value":5.0,"raw":"5"}},
            "operator":"*",
            "right":{"type":"Literal","value":300.0,"raw":"300"}
        }))
        .unwrap();
    let expected = expected_estree.to_proto();

    println!("value: {}", parsed);
    assert_eq!(parsed, expected);
}

#[test]
fn test_vegajs_evaluate_scalar() {
    let vegajs_runtime = vegajs_runtime();
    let result = vegajs_runtime
        .eval_scalar_expression("20 + 300", &Default::default())
        .unwrap();
    println!("result: {}", result);
    assert_eq!(result, ScalarValue::from(320.0));
}

#[test]
fn test_vegajs_evaluate_scalar_scope() {
    let vegajs_runtime = vegajs_runtime();
    let scope: HashMap<_, _> = vec![("a".to_string(), ScalarValue::from(123.0))]
        .into_iter()
        .collect();

    let config = CompilationConfig {
        signal_scope: scope,
        ..Default::default()
    };

    let result = vegajs_runtime
        .eval_scalar_expression("20 + a", &config)
        .unwrap();
    println!("result: {}", result);
    assert_eq!(result, ScalarValue::from(143.0));
}

#[test]
fn try_local_timezone() {
    let vegajs_runtime = vegajs_runtime();
    let tz = vegajs_runtime.nodejs_runtime.local_timezone().unwrap();
    println!("tz: {}", tz)
}

#[test]
fn test_evaluate_filter_transform() {
    let vegajs_runtime = vegajs_runtime();
    let dataset = VegaFusionTable::from_json(
        &json!([
            {"colA": 2.0, "colB": false, "colC": "first"},
            {"colA": 4.0, "colB": true, "colC": "second"},
            {"colA": 6.0, "colB": false, "colC": "third"},
            {"colA": 8.0, "colB": true, "colC": "forth"},
            {"colA": 10.0, "colB": false, "colC": "fifth"},
        ]),
        1024,
    )
    .unwrap();

    let signal_scope: HashMap<_, _> = vec![("a".to_string(), ScalarValue::from(6.0))]
        .into_iter()
        .collect();
    let config = CompilationConfig {
        signal_scope,
        ..Default::default()
    };

    let transforms = vec![
        TransformSpec::Filter(FilterTransformSpec {
            expr: "datum.colA >= a".to_string(),
            extra: Default::default(),
        }),
        TransformSpec::Extent(ExtentTransformSpec {
            field: "colA".to_string(),
            signal: Some("extent_out".to_string()),
            extra: Default::default(),
        }),
    ];

    let (result_data, result_signals) = vegajs_runtime
        .eval_transform(&dataset, &transforms, &config)
        .unwrap();

    println!("{}\n", result_data.pretty_format(None).unwrap());
    println!("{:#?}\n", result_signals);

    // Check extent signal
    assert_eq!(
        result_signals,
        vec![ScalarValue::List(
            Some(Box::new(vec![
                ScalarValue::from(6.0),
                ScalarValue::from(10.0)
            ])),
            Box::new(DataType::Float64)
        )]
    );

    let expected_dataset = VegaFusionTable::from_json(
        &json!([
            {"colA": 6, "colB": false, "colC": "third"},
            {"colA": 8, "colB": true, "colC": "forth"},
            {"colA": 10, "colB": false, "colC": "fifth"},
        ]),
        1024,
    )
    .unwrap();

    assert_eq!(result_data.to_json(), expected_dataset.to_json());
}

#[test]
fn test_export_single_image() {
    let crate_dir = std::path::PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .display()
        .to_string();

    let spec_path = format!(
        "{}/tests/specs/custom/lets_make_a_bar_chart.json",
        crate_dir
    );
    let spec_str = fs::read_to_string(spec_path).expect("Failed to read spec");
    let chart_spec: ChartSpec =
        serde_json::from_str(&spec_str).expect("Failed to parse JSON as chart");

    let vegajs_runtime = vegajs_runtime();
    let res = vegajs_runtime
        .export_spec_single(&chart_spec, ExportImageFormat::Png)
        .expect("Failed to export single spec");

    res.save(
        &format!("{}/tests/output/lets_make_a_bar_chart.png", crate_dir),
        false,
    )
    .expect("Failed to save image");
}

#[test]
fn try_export_sequence_helper_crossfilter() {
    let crate_dir = std::path::PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .display()
        .to_string();
    let spec_path = format!(
        "{}/tests/specs/custom/flights_crossfilter_a.vg.json",
        crate_dir
    );

    let spec_str = fs::read_to_string(spec_path).unwrap();
    let chart_spec: ChartSpec = serde_json::from_str(&spec_str).unwrap();

    println!("{:?}", chart_spec);

    let init = Vec::new();
    let updates: Vec<ExportUpdateBatch> = vec![
        vec![
            ExportUpdate {
                namespace: ExportUpdateNamespace::Signal,
                name: "brush_x".to_string(),
                scope: vec![0],
                value: json!([70, 120]),
            },
            ExportUpdate {
                namespace: ExportUpdateNamespace::Signal,
                name: "brush_x".to_string(),
                scope: vec![1],
                value: json!([40, 80]),
            },
        ],
        vec![ExportUpdate {
            namespace: ExportUpdateNamespace::Signal,
            name: "brush_x".to_string(),
            scope: vec![0],
            value: json!([0, 0]),
        }],
        vec![ExportUpdate {
            namespace: ExportUpdateNamespace::Signal,
            name: "brush_x".to_string(),
            scope: vec![1],
            value: json!([0, 0]),
        }],
    ];

    let watches: Vec<Watch> = vec![
        Watch {
            namespace: WatchNamespace::Data,
            name: "brush_store".to_string(),
            scope: vec![],
        },
        Watch {
            namespace: WatchNamespace::Signal,
            name: "brush".to_string(),
            scope: vec![],
        },
    ];

    let vegajs_runtime = vegajs_runtime();
    let res = vegajs_runtime
        .export_spec_sequence(&chart_spec, ExportImageFormat::Svg, init, updates, watches)
        .unwrap();

    // Write out images
    for (i, (export_image, batch)) in res.iter().enumerate() {
        println!("watch: {}", serde_json::to_string(&batch).unwrap());
        match export_image {
            ExportImage::Svg(svg_str) => {
                let spec_path = format!("{}/tests/output/seq_res{}.svg", crate_dir, i);
                fs::write(spec_path, svg_str).expect("Failed to write temp file");
            }
            ExportImage::Png(_) => {}
        }
    }
}
