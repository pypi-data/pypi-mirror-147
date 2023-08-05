/*
 * VegaFusion
 * Copyright (C) 2022 VegaFusion Technologies LLC
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
use crate::spec::transform::TransformSpecTrait;
use serde::{Deserialize, Serialize};
use serde_json::Value;
use std::collections::HashMap;

use crate::error::Result;

use crate::spec::values::NumberOrSignalSpec;
use crate::task_graph::task::InputVariable;

/// Struct that serializes to Vega spec for the lookup transform.
/// This is currently only needed to report the proper input dependencies
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct SequenceTransformSpec {
    pub start: NumberOrSignalSpec,
    pub stop: NumberOrSignalSpec,

    #[serde(skip_serializing_if = "Option::is_none")]
    pub step: Option<NumberOrSignalSpec>,

    #[serde(flatten)]
    pub extra: HashMap<String, Value>,
}

impl TransformSpecTrait for SequenceTransformSpec {
    fn supported(&self) -> bool {
        false
    }

    fn input_vars(&self) -> Result<Vec<InputVariable>> {
        let mut input_vars: Vec<InputVariable> = Vec::new();
        input_vars.extend(self.start.input_vars()?);
        input_vars.extend(self.stop.input_vars()?);
        if let Some(step) = &self.step {
            input_vars.extend(step.input_vars()?);
        }

        Ok(input_vars)
    }
}
