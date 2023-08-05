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
use crate::error::Result;
use crate::expression::parser::parse;
use crate::proto::gen::transforms::Formula;
use crate::spec::transform::formula::FormulaTransformSpec;
use crate::transform::TransformDependencies;

use crate::task_graph::task::InputVariable;

impl Formula {
    pub fn try_new(spec: &FormulaTransformSpec) -> Result<Self> {
        let expr = parse(&spec.expr)?;
        Ok(Self {
            expr: Some(expr),
            r#as: spec.as_.clone(),
        })
    }
}

impl TransformDependencies for Formula {
    fn input_vars(&self) -> Vec<InputVariable> {
        self.expr.as_ref().unwrap().input_vars()
    }
}
